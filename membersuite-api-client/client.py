import os
import hmac
from hashlib import sha1
import base64
from datetime import datetime
from zeep import Client
from lxml import etree

import logging.config

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})


_MS_ACCESS_KEY = os.environ.get('MS_ACCESS_KEY', None)
_MS_SECRET_KEY = os.environ.get('MS_SECRET_KEY', None)
_MS_ASSOCIATION_ID = os.environ.get('MS_ASSOCIATION_ID', None)
_MS_PORTAL_USER_ID = os.environ.get('MS_PORTAL_USER_ID', None)
_MS_PORTAL_USER_PASS = os.environ.get('MS_PORTAL_PASSWORD', None)

XHTML_NAMESPACE = "http://membersuite.com/schemas"


class ConciergeClient:

    def __init__(self):
        """
        Initializes Client object by pulling in authentication credentials and
        establishing a session ID with the MemberSuite Concierge API.
        """
        if not _MS_ACCESS_KEY:
            raise Exception('No MemberSuite Access Key provided.')
        if not _MS_SECRET_KEY:
            raise Exception('No MemberSuite Secret Key provided.')
        if not _MS_ASSOCIATION_ID:
            raise Exception('No MemberSuite Association ID provided.')
        self.access_key = _MS_ACCESS_KEY
        self.secret_key = _MS_SECRET_KEY
        self.association_id = _MS_ASSOCIATION_ID

        self.url = "http://membersuite.com/contracts/IConciergeAPIService/LoginToPortal"
        self.session_id = None
        self.hashed_signature = self.get_hashed_signature()
        self.session_id = self.request_session()
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
        client = Client('https://soap.membersuite.com/mex')

        concierge_request_header = \
            etree.Element(etree.QName(XHTML_NAMESPACE, "ConciergeRequestHeader"),
                          nsmap={'sch': XHTML_NAMESPACE})

        access_key = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "AccessKeyId"))

        association_id = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "AssociationId"))

        signature = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "Signature"))

        access_key.text = _MS_ACCESS_KEY
        association_id.text = _MS_ASSOCIATION_ID
        signature.text = self.hashed_signature

        client.service.LoginToPortal(portalUserName=_MS_PORTAL_USER_ID,
                                     portalPassword=_MS_PORTAL_USER_PASS,
                                     _soapheaders=[concierge_request_header])

        return None

    def _get(self, params, request_body):
        """
        Performs HTTP GET request with credentials
        :param params: HTTP GET parameters.
        :param request_body: Body of request to be put into the SOAP envelope.
        :return: Returns API response.
        """
        # - call soap package to construct envelope (maybe make this its own sub-method)
        # - send request to concierge
        # - check status code
        #     - if 200 return response_object
        #     - else
        #         - so many exceptions!
