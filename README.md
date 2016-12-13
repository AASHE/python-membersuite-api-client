[![Build Status](https://travis-ci.org/AASHE/python-membersuite-api-client.svg?branch=master)](https://travis-ci.org/AASHE/python-membersuite-api-client) [![Coverage Status](https://coveralls.io/repos/github/AASHE/python-membersuite-api-client/badge.svg?branch=master)](https://coveralls.io/github/AASHE/python-membersuite-api-client?branch=master) [![Issue Count](https://codeclimate.com/github/AASHE/python-membersuite-api-client/badges/issue_count.svg)](https://codeclimate.com/github/AASHE/python-membersuite-api-client) [![Requirements Status](https://requires.io/github/AASHE/python-membersuite-api-client/requirements.svg?branch=master)](https://requires.io/github/AASHE/python-membersuite-api-client/requirements/?branch=master)

# python-membersuite-api-client
A python interface to the MemberSuite API

## Installation

Install as you would any other package. Add to your requirements.txt:

    https://github.com/AASHE/python-membersuite-api-client/archive/master.zip

(to be updated when this package is added to PyPi)

## MemberSuite Configuration

In your MemberSuite account, you will need to create a dedicated API console
user. Ensure that API access is enabled for your MemberSuite account, and
also check the box for "API User" for this new user account.

Create a keypair for this user via the console and save the credentials
generated somewhere secure (they cannot be retrieved later if lost)

## Environment Variables

MS_ACCESS_KEY - MemberSuite access key from API user keypair
MS_SECRET_KEY - MemberSuite secret key from API user keypair
MS_ASSOCIATION_ID - Association ID
MS_USER_ID - User ID for the API user you created
MS_USER_PASS - Password for the API user you created

These are all required to properly generate the hashed signature data and
to call the Login WSDL method to authenticate and generate a session ID.

## Usage

Create your client instance by invoking "client = ConciergeClient()".

To authenticate and receive a session ID, call client.request_session().

This returns the session ID value when called, or this can be retrieved as an
attribute client.session_id.

This can now be used to make additional calls using the methods included in
the WSDL from MemberSuite. For documentation on available methods and their
usage, see http://api.docs.membersuite.com/

Use request_session() as a model for constructing the headers for 
your own functions in your app that follow this method:

    1) Alter client.url. Use the full URL for the SOAP action you are taking.
    2) Call client.construct_concierge_header() to generate a new header element.
    3) Call client.service.method_name(_soapheaders=[concierge_request_header], method arguments)
    4) Return any relevant data out of the response object

***IMPORTANT NOTE: In constructing headers, SessionId must appear first.***