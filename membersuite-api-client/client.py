import os
import hmac
import hashlib
import base64
import requests
from string import Template
from datetime import datetime
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor


_MS_ACCESS_KEY = os.environ.get('MS_ACCESS_KEY', None)
_MS_SECRET_KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
_MS_ASSOCIATION_ID = '00000000-0000-0000-0000-000000000000'


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

        self.initial_request_url = 'http://membersuite.com/contracts/IConciergeAPIService/WhoAmI00000000-0000-0000-0000-00000000000011111111-1111-1111-1111-111111111111'

        self.hashed_signature = self.get_hashed_signature()
        self.session_id = self.request_session()
        self.session_start_time = datetime.now()

    def get_hashed_signature(self):
        signature = bytearray(self.initial_request_url)
        print "SIGNATURE: ", type(signature), signature
        print "SECRET KEY BEFORE: ", type(self.secret_key)
        secret_key = bytearray(self.secret_key)
        print "SECRET KEY: ", secret_key
        hashed_signature = hmac.new(secret_key,
                                    msg=signature,
                                    digestmod=hashlib.sha1).digest()
        hashed_signature = bytearray(base64.b64encode(hashed_signature))
        print hashed_signature
        return hashed_signature

    def request_session(self):
        """
        Performs initial request to initialize session and get session id
        necessary to construct all future requests.
        :return: Session ID to be placed in header of all other requests.
        """

        body = '<con:WhoAmI/>'

        infile = os.path.join(os.path.dirname(__file__),
                            'templates/initial_request.txt')
        template = open(infile)
        soap_initial_request = Template(template.read())

        headers = {'content-type': 'text/xml'}
        data = {
            'access_key': self.access_key,
            'association_id': self.association_id,
            'hashed_signature': self.hashed_signature,
            'body': body,
        }
        request = soap_initial_request.substitute(data)

        response = requests.post(self.initial_request_url,
                                 data=request,
                                 headers=headers)
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
