"""
    The service for connecting to MemberSuite for OrganizationService

    http://api.docs.membersuite.com/#References/Objects/Organization.htm

"""

from .models import Organization
from ..utils import convert_ms_object
from zeep.exceptions import TransportError


class OrganizationService(object):

    def __init__(self, client):
        """
        Accepts a ConciergeClient to connect with MemberSuite
        """
        self.client = client

    def query_orgs(self, parameters=None, since_when=None, get_all=False,
                   results=None, start_record=0):
        """
        Constructs request to MemberSuite to query organization objects
        based on parameters provided.
        Must loop over 400 indexes at a time. Recursively calls itself until
        a non-full queryset is received, returning a joined set each time.
        """
        print("STARTING INDEX: ", start_record)
        concierge_request_header = self.construct_concierge_header(
            url="http://membersuite.com/contracts/"
                "IConciergeAPIService/ExecuteMSQL")

        query = "SELECT Objects() FROM Organization "
        if parameters and not get_all:
            query += "WHERE"
            for key in parameters:
                query += " %s = '%s' AND" % (key, parameters[key])
            query = query[:-4]

            if since_when:
                query += " AND LastModifiedDate > '{since_when} 00:00:00'" \
                    .format(since_when=since_when.isoformat())
        elif since_when and not get_all:
            query += "WHERE LastModifiedDate > '{since_when} 00:00:00'".format(
                since_when=since_when.isoformat())
        try:
            result = self.client.runSQL(
                query=query,
                start_record=start_record,
                limit_to=limit_to,
            )
            result = self.client.service.ExecuteMSQL(
                _soapheaders=[concierge_request_header],
                msqlStatement=query,
                startRecord=start_record,
                maximumNumberOfRecordsToReturn=400,
            )
        except TransportError:
            # API Intermittently fails and kicks a 504,
            # this is a way to retry if that happens.
            result = self.query_orgs(parameters=parameters,
                                     since_when=since_when,
                                     get_all=get_all,
                                     results=results,
                                     start_record=start_record)
            return result

        # Check that we don't have an empty set returned
        if (result["body"]["ExecuteMSQLResult"]["ResultValue"]
            ["ObjectSearchResult"]["TotalRowCount"] > 0):
            if results:
                new_results = (results.append(result["body"]
                                              ["ExecuteMSQLResult"]
                                              ["ResultValue"]
                                              ["ObjectSearchResult"]
                                              ["Objects"]
                                              ["MemberSuiteObject"]))
            else:
                new_results = result["body"]["ExecuteMSQLResult"]\
                    ["ResultValue"]["ObjectSearchResult"]["Objects"]\
                    ["MemberSuiteObject"]
        # If set was empty, just return the existing results
        # (empty list if first iteration)
        else:
            new_results = results

        # Check if the queryset was completely full. If so, there may be
        # More results we need to query
        if len(result["body"]["ExecuteMSQLResult"]["ResultValue"]
               ["ObjectSearchResult"]["Objects"]["MemberSuiteObject"]) == 400:
            # Call this function again recursively, passing the existing
            # results and the new index where to start
            new_results = self.query_orgs(parameters=parameters,
                                          since_when=since_when,
                                          get_all=get_all,
                                          results=new_results,
                                          start_record=start_record + 400)
        return self.package_organizations(new_results)

    def package_organizations(self, obj_list):
        """
        Loops through MS objects returned from queries to turn them into
        Organization objects and pack them into a list for later use.
        """
        org_list = []
        for obj in obj_list:
            sane_obj = convert_ms_object(
                obj['Fields']['KeyValueOfstringanyType']
            )
            org = Organization(sane_obj)
            org_list.append(org)
        return org_list
