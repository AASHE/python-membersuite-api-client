from .models import PortalUser
from ..exceptions import LoginToPortalError
from ..utils import get_session_id


def login_to_portal(username, password, client):
    """Log `username` into the MemberSuite Portal.

    Returns a PortalUser object if successful, raises
    LoginToPortalError if not.

    """
    if not client.session_id:
        client.request_session()

    concierge_request_header = client.construct_concierge_header(
        url=("http://membersuite.com/contracts/IConciergeAPIService/"
             "LoginToPortal"))

    result = client.client.service.LoginToPortal(
        _soapheaders=[concierge_request_header],
        portalUserName=username,
        portalPassword=password)

    login_to_portal_result = result["body"]["LoginToPortalResult"]

    if login_to_portal_result["Success"]:
        portal_user = login_to_portal_result["ResultValue"]["PortalUser"]

        session_id = get_session_id(result=result)

        return PortalUser(membersuite_object_data=portal_user,
                          session_id=session_id)
    else:
        raise LoginToPortalError(result=result)
