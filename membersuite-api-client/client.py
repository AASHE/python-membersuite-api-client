import os
import hmac
from hashlib import sha1
import base64
from datetime import datetime
from zeep import Client
from lxml import etree

_MS_ACCESS_KEY = os.environ.get('MS_ACCESS_KEY', None)
_MS_SECRET_KEY = os.environ.get('MS_SECRET_KEY', None)
_MS_ASSOCIATION_ID = os.environ.get('MS_ASSOCIATION_ID', None)
_MS_USER_ID = os.environ.get('MS_USER_ID', None)
_MS_USER_PASS = os.environ.get('MS_USER_PASS', None)

XHTML_NAMESPACE = "http://membersuite.com/schemas"


class ConciergeClient:

    def __init__(self):
        """
        Initializes Client object by pulling in authentication credentials.
        Altered to make "request_session" a manual call to facilitate testing.
        """
        if not _MS_ACCESS_KEY:
            raise Exception('No MemberSuite Access Key provided.')
        if not _MS_SECRET_KEY:
            raise Exception('No MemberSuite Secret Key provided.')
        if not _MS_ASSOCIATION_ID:
            raise Exception('No MemberSuite Association ID provided.')
        self.client = Client('https://soap.membersuite.com/mex')
        self.access_key = _MS_ACCESS_KEY
        self.secret_key = _MS_SECRET_KEY
        self.association_id = _MS_ASSOCIATION_ID

        self.url = \
            "http://membersuite.com/contracts/IConciergeAPIService/Login"
        self.session_id = None
        self.hashed_signature = self.get_hashed_signature()
        self.session_id = None
        self.session_start_time = datetime.now()

    def get_hashed_signature(self):
        """
        Process from Membersuite Docs: http://bit.ly/2eSIDxz

        Usage: Modify self.url attribute of class
               before calling method, if necessary
        """
        data = "%s%s" % (self.url, self.association_id)
        if self.session_id:
            data = "%s%s" % (data, self.session_id)
        data_b = bytearray(data, 'utf-8')
        secret_key = base64.b64decode(self.secret_key)
        secret_b = bytearray(secret_key)

        hashed = hmac.new(secret_b, data_b, sha1).digest()
        return base64.b64encode(hashed).decode("utf-8")

    def request_session(self):
        """
        Performs initial request to initialize session and get session id
        necessary to construct all future requests.
        :return: Session ID to be placed in header of all other requests.
        """

        concierge_request_header = self.construct_concierge_header()

        result = self.client.service.Login(
            _soapheaders=[concierge_request_header],
            userName=_MS_USER_ID,
            password=_MS_USER_PASS,
            loginDestination=_MS_ASSOCIATION_ID
        )

        try:
            self.session_id = result['header']['header']['SessionId']
        except:
            pass

        return self.session_id

    def construct_concierge_header(self):
        """
        Constructs the Concierge Request Header lxml object to be used as the
        '_soapheaders' argument for WSDL methods.
        """
        concierge_request_header = \
            etree.Element(
                etree.QName(XHTML_NAMESPACE, "ConciergeRequestHeader"),
                nsmap={'sch': XHTML_NAMESPACE})

        if self.session_id:
            session = \
                etree.SubElement(concierge_request_header,
                                 etree.QName(XHTML_NAMESPACE, "SessionId"))
            session.text = self.session_id

        access_key = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "AccessKeyId"))
        access_key.text = _MS_ACCESS_KEY

        association_id = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "AssociationId"))
        association_id.text = _MS_ASSOCIATION_ID

        signature = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "Signature"))
        signature.text = self.hashed_signature

        return concierge_request_header
