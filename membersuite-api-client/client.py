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
_MS_PORTAL_USER_PASS = os.environ.get('MS_PORTAL_USER_PASS', None)

XHTML_NAMESPACE = "http://www.w3.org/2001/XMLSchema"


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

        self.url = "http://soap.membersuite.com"
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
        concierge_message_header = \
            etree.Element(etree.QName(XHTML_NAMESPACE, "complexType"),
                          name="ConciergeMessageHeader")

        message_header_sequence = \
            etree.SubElement(concierge_message_header,
                             etree.QName(XHTML_NAMESPACE, "sequence"))

        message_sequence_element = \
            etree.SubElement(message_header_sequence,
                             etree.QName(XHTML_NAMESPACE, "element"),
                             name="SessionId",
                             type="xs:string",
                             minOccurs="0",
                             maxOccurs="1")

        concierge_request_header = \
            etree.Element(etree.QName(XHTML_NAMESPACE, "complexType"),
                          name="ConciergeRequestHeader")

        concierge_content = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "complexContent"))

        extension = \
            etree.SubElement(concierge_content,
                             etree.QName(XHTML_NAMESPACE, "extension"),
                             base="ConciergeMessageHeader")

        extension_sequence = \
            etree.SubElement(extension,
                             etree.QName(XHTML_NAMESPACE, "sequence"),
                             )

        access_key = \
            etree.SubElement(extension_sequence,
                             etree.QName(XHTML_NAMESPACE, "element"),
                             name="AccessKeyId",
                             type="xs:string",
                             minOccurs="1",
                             maxOccurs="1")

        association_id = \
            etree.SubElement(extension_sequence,
                             etree.QName(XHTML_NAMESPACE, "element"),
                             name="AssociationId",
                             type="xs:string",
                             minOccurs="1",
                             maxOccurs="1")

        signature = \
            etree.SubElement(extension_sequence,
                             etree.QName(XHTML_NAMESPACE, "element"),
                             name="Signature",
                             type="xs:string",
                             minOccurs="1",
                             maxOccurs="1")

        access_key.text = _MS_ACCESS_KEY
        association_id.text = _MS_ASSOCIATION_ID
        signature = self.hashed_signature

        client.service.LoginToPortal(portalUserName=_MS_PORTAL_USER_ID,
                                     portalPassword=_MS_PORTAL_USER_PASS,
                                     _soapheaders=[concierge_message_header,
                                                   concierge_request_header])

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
