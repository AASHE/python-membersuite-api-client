import os
from datetime import datetime


_MS_ACCESS_KEY = os.environ.get('MS_API_ACCESS_KEY', None)
_MS_SECRET_KEY = os.environ.get('MS_SECRET_KEY', None)
_MS_ASSOCIATION_ID = os.environ.get('MS_ASSOCIATION_ID', None)


class ConciergeClient:

    def __init__(self):
        """
        Initializes Client object by pulling in authentication credentials and
        establishing a session ID with the MemberSuite Concierge API.
        """
        - insert checks to make sure everything is in order with credentials
            and add exceptions and error messages
        self.access_key = _MS_ACCESS_KEY
        self.secret_key = _MS_SECRET_KEY
        self.association_id = _MS_ASSOCIATION_ID
        self.session_id = self.request_session()
        self.session_start_time = datetime.now()

    def request_session(self):
        """
        Performs initial request to initialize session and get session id
        necessary to construct all future requests.
        :return: Session ID to be placed in header of all other requests.
        """
        - call soap package to construct envelope
        - potentially add retry and timeout checks, loop it until you have to give up? (see google api example)
        - send request to concierge
        - logic for processing the response
            - is it 200?
            - exceptions! messages! logging!

        return session_id

    def _get(self, params, request_body):
        """
        Performs HTTP GET request with credentials
        :param params: HTTP GET parameters.
        :param request_body: Body of request to be put into the SOAP envelope.
        :return: Returns API response.
        """
        - call soap package to construct envelope (maybe make this its own sub-method)
        - send request to concierge
        - check status code
            - if 200 return response_object
            - else
                - so many exceptions!
