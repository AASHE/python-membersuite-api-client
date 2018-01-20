import time

from django.contrib.auth.models import User

from .models import PortalUser, generate_username
from ..exceptions import LoginToPortalError, LogoutError
from ..utils import get_session_id


def login_to_portal(username, password, client, retries=2, delay=0):
    """Log `username` into the MemberSuite Portal.

    Returns a PortalUser object if successful, raises
    LoginToPortalError if not.

    Will retry logging in if a GeneralException occurs, up to `retries`.
    Will pause `delay` seconds between retries.
    """
    if not client.session_id:
        client.request_session()

    concierge_request_header = client.construct_concierge_header(
        url=("http://membersuite.com/contracts/IConciergeAPIService/"
             "LoginToPortal"))

    attempts = 0
    while attempts < retries:
        if attempts:
            time.sleep(delay)

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
            try:
                error_code = login_to_portal_result[
                    "Errors"]["ConciergeError"][0]["Code"]
            except IndexError:  # Not a ConciergeError
                continue
            else:
                if attempts < retries and error_code == "GeneralException":
                    continue

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


# get_user_for_membersuite_entity introduces a dependency on
# Django (django.contrib.auth.models, to be precise).  That's
# quite a drag.  Goes someplace else.  Need to drop dependency
# on Django.
def get_user_for_membersuite_entity(membersuite_entity):
    """Returns a User for `membersuite_entity`.

    membersuite_entity is any MemberSuite object that has the fields
    membersuite_id, email_address, first_name, and last_name, e.g.,
    PortalUser or Individual.

    """
    user = None
    user_created = False

    # First, try to match on username.
    user_username = generate_username(membersuite_entity)
    try:
        user = User.objects.get(username=user_username)
    except User.DoesNotExist:
        pass

    # Next, try to match on email address.
    if not user:
        try:
            user = User.objects.filter(
                email=membersuite_entity.email_address)[0]
        except IndexError:
            pass

    # No match? Create one.
    if not user:
        user = User.objects.create(
            username=user_username,
            email=membersuite_entity.email_address,
            first_name=membersuite_entity.first_name,
            last_name=membersuite_entity.last_name)
        user_created = True

    return user, user_created
