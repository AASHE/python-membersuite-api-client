from hashlib import sha1
from lxml import etree
from zeep import Client
import base64
import hmac

from .utils import get_session_id


XHTML_NAMESPACE = "http://membersuite.com/schemas"


class MembersuiteLoginError(Exception):

    pass


class ConciergeClient(object):

    def __init__(self, access_key, secret_key, association_id):
        """
        Initializes Client object by pulling in authentication credentials.
        Altered to make "request_session" a manual call to facilitate testing.
        """
        self.access_key = access_key
        self.secret_key = secret_key
        self.association_id = association_id
        self.session_id = None
        self.client = Client('https://soap.membersuite.com/mex')

    def get_hashed_signature(self, url):
        """
        Process from Membersuite Docs: http://bit.ly/2eSIDxz
        """
        data = "%s%s" % (url, self.association_id)
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
        concierge_request_header = self.construct_concierge_header(
            url="http://membersuite.com/contracts/IConciergeAPIService/WhoAmI")

        result = self.client.service.WhoAmI(
            _soapheaders=[concierge_request_header])

        self.session_id = get_session_id(result=result)

        if not self.session_id:
            raise MembersuiteLoginError(
                result["body"]["WhoAmIResult"]["Errors"])

        return self.session_id

    def construct_concierge_header(self, url):
        """
        Constructs the Concierge Request Header lxml object to be used as the
        '_soapheaders' argument for WSDL methods.
        """
        concierge_request_header = (
            etree.Element(
                etree.QName(XHTML_NAMESPACE, "ConciergeRequestHeader"),
                nsmap={'sch': XHTML_NAMESPACE}))

        if self.session_id:
            session = (
                etree.SubElement(concierge_request_header,
                                 etree.QName(XHTML_NAMESPACE, "SessionId")))
            session.text = self.session_id

        access_key = (
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "AccessKeyId")))
        access_key.text = self.access_key

        association_id = (etree.SubElement(concierge_request_header,
                                           etree.QName(XHTML_NAMESPACE,
                                                       "AssociationId")))
        association_id.text = self.association_id

        signature = (
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "Signature")))
        signature.text = self.get_hashed_signature(url=url)

        return concierge_request_header

    def execute_object_query(self, object_query, start_record=0,
                             limit_to=400):
        concierge_request_header = self.construct_concierge_header(
            url="http://membersuite.com/contracts/"
                "IConciergeAPIService/ExecuteMSQL")
        result = self.client.service.ExecuteMSQL(
            _soapheaders=[concierge_request_header],
            msqlStatement=object_query,
            startRecord=start_record,
            maximumNumberOfRecordsToReturn=limit_to,
        )
        return result
