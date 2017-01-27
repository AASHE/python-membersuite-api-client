from hashlib import sha1
from lxml import etree
from zeep import Client
import base64
import hmac

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

    def get_session_id_from_login_result(self, login_result):
        try:
            return login_result["header"]["header"]["SessionId"]
        except TypeError:
            return None

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

        self.session_id = self.get_session_id_from_login_result(
            login_result=result)

        if not self.session_id:
            raise MembersuiteLoginError(
                result["body"]["LoginResult"]["Errors"])

        return self.session_id

    def construct_concierge_header(self, url):
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
        access_key.text = self.access_key

        association_id = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "AssociationId"))
        association_id.text = self.association_id

        signature = \
            etree.SubElement(concierge_request_header,
                             etree.QName(XHTML_NAMESPACE, "Signature"))
        signature.text = self.get_hashed_signature(url=url)

        return concierge_request_header

    def query_orgs(self, parameters=None, since_when=None):
        """
        Constructs request to MemberSuite to query organization objects
        based on parameters provided.

        parameters: A dictionary of key-value pairs (field name: value)
        """
        concierge_request_header = self.construct_concierge_header(
            url="http://membersuite.com/contracts/"
                "IConciergeAPIService/ExecuteMSQL")

        query = "SELECT Objects() FROM Organization "
        if parameters:
            query += "WHERE"
            for key in parameters:
                query += " %s = '%s' AND" % (key, parameters[key])
            query = query[:-4]

            if since_when:
                query += " AND LastModifiedDate > '{since_when} 00:00:00'"\
                    .format(since_when=since_when.isoformat())
        elif since_when:
            query += "WHERE LastModifiedDate > '{since_when} 00:00:00'".format(
                since_when=since_when.isoformat())

        result = self.client.service.ExecuteMSQL(
            _soapheaders=[concierge_request_header],
            msqlStatement=query,
            startRecord=0
        )

        if result["body"]["ExecuteMSQLResult"]["ResultValue"]["ObjectSearchResult"]["Objects"]:
            return(result["body"]["ExecuteMSQLResult"]["ResultValue"]
                   ["ObjectSearchResult"]["Objects"]["MemberSuiteObject"])
        else:
            return None

    def runSQL(self, query, start_record=0):
        concierge_request_header = self.construct_concierge_header(
            url="http://membersuite.com/contracts/"
                "IConciergeAPIService/ExecuteMSQL")
        result = self.client.service.ExecuteMSQL(
            _soapheaders=[concierge_request_header],
            msqlStatement=query,
            startRecord=start_record
        )
        return result
