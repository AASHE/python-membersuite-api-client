from .models import PortalUser
from ..exceptions import LoginToPortalError, LogoutError
from ..utils import get_session_id


def login_to_portal(username, password, client, retries=2):
    """Log `username` into the MemberSuite Portal.

    Returns a PortalUser object if successful, raises
    LoginToPortalError if not.

    Will retry logging in if a GeneralException occurs, up to `retries`.
    """
    if not client.session_id:
        client.request_session()

    concierge_request_header = client.construct_concierge_header(
        url=("http://membersuite.com/contracts/IConciergeAPIService/"
             "LoginToPortal"))

    attempts = 0
    while attempts < retries:
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
            attempts += 1

    raise LoginToPortalError(result=result)


def logout(client):
    """Log out the currently logged-in user.

    There's a really crappy side-effect here - the session_id
    attribute of the `client` passed in will be reset to None if the
    logout succeeds, which is going to be almost always, let's hope.

    """
    if not client.session_id:
        client.request_session()

    concierge_request_header = client.construct_concierge_header(
        url=("http://membersuite.com/contracts/IConciergeAPIService/"
             "Logout"))

    logout_result = client.client.service.Logout(
        _soapheaders=[concierge_request_header])

    result = logout_result["body"]["LogoutResult"]

    if result["SessionID"] is None:  # Success!
        client.session_id = None
    else:  # Failure . . .
        raise LogoutError(result=result)
