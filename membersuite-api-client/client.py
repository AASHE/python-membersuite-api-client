import os
import hmac
import hashlib
import base64
from datetime import datetime
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement


_MS_ACCESS_KEY = os.environ.get('MS_ACCESS_KEY', None)
_MS_SECRET_KEY = os.environ.get('MS_SECRET_KEY', None)
_MS_ASSOCIATION_ID = os.environ.get('MS_ASSOCIATION_ID', None)


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

        self.initial_request_url = \
            "http://membersuite.com/contracts/IConciergeAPIService/WhoAmI" + \
            self.association_id

        self.hashed_signature = self.get_hashed_signature()
        self.session_id = self.request_session()
        self.session_start_time = datetime.now()

    def get_hashed_signature(self):
        signature = bytearray(self.initial_request_url)
        secret_key = bytearray(self.secret_key)
        hashed_signature = hmac.new(secret_key,
                                    msg=signature,
                                    digestmod=hashlib.sha1).digest()
        hashed_signature = bytearray(base64.b64encode(hashed_signature))
        return hashed_signature

    def request_session(self):
        """
        Performs initial request to initialize session and get session id
        necessary to construct all future requests.
        :return: Session ID to be placed in header of all other requests.
        """

        ns = 'sch'
        client = SoapClient(location="https://soap.membersuite.com",
                            trace=True, ns='soapenv')
        print client.http
        headers = SimpleXMLElement("<Header/>")
        concierge_header = headers.add_child("sch:ConciergeRequestHeader")
        concierge_header.marshall('AccessKeyID', self.access_key)
        concierge_header.marshall('AssociationID', self.association_id)
        concierge_header.marshall('Signature', self.hashed_signature)
        client['Header'] = headers
        response = client.call(self)
        # - call soap package to construct envelope
        # - potentially add retry and timeout checks, loop it until you have to give up? (see google api example)
        # - send request to concierge
        # - logic for processing the response
        #     - is it 200?
        #     - exceptions! messages! logging!
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
