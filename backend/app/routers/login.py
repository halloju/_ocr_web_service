from fastapi import APIRouter, HTTPException, Request, Response
from fastapi import Cookie
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os
import json
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.idp_metadata_parser import OneLogin_Saml2_IdPMetadataParser
from route_utils import async_call_mlaas_function
from fastapi.encoders import jsonable_encoder
from urllib.parse import urlparse
import re

from app.exceptions import CustomException, MlaasRequestError
from app.models.user import User
from utils.logger import Logger
from route_utils import get_request_id



SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
logger = Logger('login')


async def prepare_from_fastapi_request(request, debug=False):
    form_data = await request.form()
    x_forwarded_proto = request.headers.get('x-forwarded-proto')

    rv = {
        "http_host": request.headers.get('x-forwarded-host', request.client.host),
        "server_port": request.url.port,
        "script_name": "/backend" + request.url.path,
        "post_data": {},
        "get_data": {},
        "https": "on" if x_forwarded_proto == "https" else "off",  # Add this line
    }

    if (request.query_params):
        rv["get_data"] = request.query_params,
    if "SAMLResponse" in form_data:
        SAMLResponse = form_data["SAMLResponse"]
        rv["post_data"]["SAMLResponse"] = SAMLResponse
    if "RelayState" in form_data:
        RelayState = form_data["RelayState"]
        rv["post_data"]["RelayState"] = RelayState
    return rv


# Validate URL Format
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and re.match(r'http[s]?://', url)
    except:
        return False
    
    
def init_saml_auth(req):
    try:
        # Define the path to the settings file.
        filename = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'static', 'saml', 'settings.json')

        # Use context manager for reading the settings file.
        with open(filename, 'r') as json_data_file:
            settings_data = json.load(json_data_file)

        # Ensure the environment variable is present and valid.
        saml_idp_metadata_url = os.environ.get('SAML_IDP_METADATA_URL')
        if not saml_idp_metadata_url:
            raise ValueError("SAML_IDP_METADATA_URL is not set in environment variables")

        if not is_valid_url(saml_idp_metadata_url):
            return ValueError('Not a valid url')

        # Check if URL ends with 'xml'
        if not saml_idp_metadata_url.endswith('xml'):
            return ValueError('URL does not point to an XML file')

        # Parse remote IdP data with certificate validation.
        idp_data = OneLogin_Saml2_IdPMetadataParser.parse_remote(
            saml_idp_metadata_url, validate_cert=False)
        settings_data['idp']['x509cert'] = idp_data['idp']['x509certMulti']['signing'][0]

        # Initialize SAML authentication.
        auth = OneLogin_Saml2_Auth(req, settings_data)
        return auth

    except Exception as e:
        raise Exception(f"SAML Authentication initialization failed: {e}")

async def is_user_auth(user_id, rid, logger):
    input_data = {
            "business_unit": "C170",
            "request_id": rid,
            "inputs": jsonable_encoder({'user_id': user_id})
    }
    try:
        outputs = await async_call_mlaas_function(
            input_data,
            '/authenticate_user',
            project='GPUser',
            logger=logger
        )
        return outputs['is_authenticated']
    except MlaasRequestError as e:
        logger.info({'error_msg': e.message})
        raise e
    except Exception as e:
        logger.error({'error_msg': str(e)})
        raise CustomException(status_code=500, message=str(e))
    return False

router = APIRouter()


@router.get("/sso")
async def sso(request: Request):
    req = await prepare_from_fastapi_request(request)
    try:
        saml_auth = init_saml_auth(req)
        callback_url = saml_auth.login()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    response = Response(callback_url)
    return response



@router.post("/acs")
async def acs(request: Request):
    try:
        req = await prepare_from_fastapi_request(request)
        saml_auth = init_saml_auth(req)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")

    saml_auth.process_response()
    if not saml_auth.is_authenticated():
        logger.error(saml_auth.get_last_error_reason())
        return Response(headers={"Location": f"/"}, status_code=400)

    # Get user attributes from the SAML response
    user_attributes = saml_auth.get_attributes()
    rid = get_request_id()
    if (not await is_user_auth(user_attributes['EmployeeID'][0], rid, logger)):
        return Response(headers={"Location": f"/auth/access"}, status_code=303)

    # Create a JWT with the user attributes as the payload
    expire_time = datetime.utcnow() + timedelta(days=7)
    refresh_token_payload = {
        "exp": expire_time,  # Expires in 7 days
        "iat": datetime.utcnow(),
        # Replace with the actual user ID
        "sub": user_attributes['EmployeeID'][0],
        "type": "refresh",  # Add a type to distinguish between access and refresh tokens
    }

    # Generate the JWTs
    refresh_token = jwt.encode(
        refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Redirect the user back to the Vue application
    response = Response(headers={"Location": f"/"}, status_code=303)

    # Set the tokens as secure, HttpOnly cookies in the response
    response.set_cookie(key="refresh_token", value=refresh_token,
                        httponly=True, secure=True, samesite="strict",
                        expire_time=expire_time)

    return response


@router.get("/slo")
async def slo(request: Request):
    req = await prepare_from_fastapi_request(request)
    saml_auth = init_saml_auth(req)
    redirect_url = saml_auth.logout()
    response = Response(headers={"Location": redirect_url}, status_code=303)
    response.delete_cookie("refresh_token")
    return response


@router.post("/sls")
async def sls(request: Request):
    req = await prepare_from_fastapi_request(request)
    saml_auth = init_saml_auth(req)
    saml_auth.process_slo()
    if not saml_auth.is_authenticated():
        return {"success": "Logged out"}
    return {"error": "Logout failed"}


@router.get("/refresh_token")
async def refresh_token(refresh_token: Optional[str] = Cookie(None)):
    # Decode the refresh token
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")

        # Check that the token is a refresh token
        if token_type != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")

        # Create a new access token
        access_token_payload = {
            "exp": datetime.utcnow() + timedelta(hours=15),  # Expires in 15 hours
            "iat": datetime.utcnow(),
            "sub": user_id,
            "type": "access",
        }

        access_token = jwt.encode(
            access_token_payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": access_token, "token_type": "bearer"}

    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")


@router.get("/is_authenticated")
def is_authenticated(refresh_token: Optional[str] = Cookie(None)):
    try:
        # Decode the token and check if it's valid
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        # is the token expired?
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")

        if payload.get("exp") < datetime.utcnow().timestamp():
            raise HTTPException(status_code=400, detail="Token is expired")

        return {"isAuthenticated": True}
    except Exception as e:
        return {"isAuthenticated": True}


@router.get("/login")
def login(request: Request):
    # Decode the refresh token
    refresh_token_payload = {
        "exp": datetime.utcnow() + timedelta(days=7),  # Expires in 7 days
        "iat": datetime.utcnow(),
        "sub": '13520',  # Replace with the actual user ID
        "type": "refresh",  # Add a type to distinguish between access and refresh tokens
    }

    # Generate the JWTs
    refresh_token = jwt.encode(
        refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Redirect the user back to the Vue application
    response = Response(status_code=200)

    # Set the tokens as secure, HttpOnly cookies in the response
    response.set_cookie(key="refresh_token", value=refresh_token,
                        httponly=True, secure=True, samesite="strict")

    return response
