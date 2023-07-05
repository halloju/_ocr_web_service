from fastapi import APIRouter, Response, Request, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from fastapi import Cookie
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os
from onelogin.saml2.auth import OneLogin_Saml2_Auth


SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")


async def prepare_from_fastapi_request(request, debug=False):
    form_data = await request.form()
    x_forwarded_proto = request.headers.get('x-forwarded-proto')

    rv = {
        "http_host": request.headers.get('x-forwarded-host', request.client.host),
        "server_port": request.url.port,
        "script_name": "/backend" + request.url.path,
        "post_data": { },
        "get_data": { },
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


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')) ## saml
    return auth


router = APIRouter()


@router.get("/sso")
async def sso(request: Request):
    req = await prepare_from_fastapi_request(request)
    try:
        saml_auth = init_saml_auth(req)
        callback_url = saml_auth.login()
    except Exception as e:
        request.state.logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    response = Response(callback_url)
    return response

@router.post("/acs")
async def acs(request: Request):
    try:
        req = await prepare_from_fastapi_request(request)
        saml_auth = init_saml_auth(req)
    except Exception as e:
        request.state.logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    saml_auth.process_response()
    if not saml_auth.is_authenticated():
        request.state.logger.error(saml_auth.get_last_error_reason())
        return Response(headers={"Location": f"/"}, status_code=400)

    # Get user attributes from the SAML response
    user_attributes = saml_auth.get_attributes()

    # Create a JWT with the user attributes as the payload
    refresh_token_payload = {
            "exp": datetime.utcnow() + timedelta(days=7),  # Expires in 7 days
            "iat": datetime.utcnow(),
            "sub": user_attributes['EmployeeID'],  # Replace with the actual user ID
            "type": "refresh",  # Add a type to distinguish between access and refresh tokens
    }
    
     # Generate the JWTs
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Redirect the user back to the Vue application
    response = Response(headers={"Location": f"/#/home"}, status_code=303)

    # Set the tokens as secure, HttpOnly cookies in the response
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="strict")

    return response


@router.get("/slo")
async def slo(request: Request):
    req = await prepare_from_fastapi_request(request)
    saml_auth = init_saml_auth(req)
    saml_auth.logout()
    return Response(saml_auth.get_last_response_xml(), media_type="application/xml")


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
            "exp": datetime.utcnow() + timedelta(minutes=15),  # Expires in 15 minutes
            "iat": datetime.utcnow(),
            "sub": user_id,
            "type": "access",
        }

        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)

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
        return {"isAuthenticated": False}

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
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Redirect the user back to the Vue application
    response = Response(status_code=200)

    # Set the tokens as secure, HttpOnly cookies in the response
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="strict")

    return response
