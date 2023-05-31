from fastapi import APIRouter, Body, Depends, File, Response, Request, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse
# from fastapi.security import OAuth2PasswordBearer
from fastapi import Cookie
from typing import Optional
import jwt
from datetime import datetime, timedelta
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils


SECRET_KEY = "your-secret-key"  # Replace with your actual secret key
ALGORITHM = "HS256"  # Or another algorithm like "RS256"

saml_config = {
    "strict": True,
    "debug": False,
    "sp": {
        "entityId": "https://sp.example.com/metadata",
        "assertionConsumerService": {
            "url": "https://sp.example.com/acs",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
        },
        "singleLogoutService": {
            "url": "https://sp.example.com/sls",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
        "x509cert": "",
        "privateKey": ""
    },
    "idp": {
        "entityId": "https://idp.example.com/metadata",
        "singleSignOnService": {
            "url": "https://idp.example.com/sso",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "singleLogoutService": {
            "url": "https://idp.example.com/slo",
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        "x509cert": ""
    }
}

router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.get("/sso")
async def sso(request: Request):
    print("saml")
    saml_auth = OneLogin_Saml2_Auth(request, saml_config)
    saml_auth.login()
    return Response(saml_auth.get_last_response_xml(), media_type="application/xml")

@router.post("/acs")
async def acs(request: Request):
    saml_auth = OneLogin_Saml2_Auth(request, saml_config)
    saml_auth.process_response()
    
    if not saml_auth.is_authenticated():
        return {"error": "Not authenticated"}

    # Get user attributes from the SAML response
    user_attributes = saml_auth.get_attributes()

    # Create a JWT with the user attributes as the payload
    jwt_secret = "your_jwt_secret"
    jwt_algorithm = "HS256"
    jwt_payload = {
        "user": user_attributes,
    }
    jwt_token = jwt.encode(jwt_payload, jwt_secret, algorithm=jwt_algorithm)
    return {"success": "Authenticated", "token": jwt_token}

@router.get("/slo")
async def slo(request: Request):
    saml_auth = OneLogin_Saml2_Auth(request, saml_config)
    saml_auth.logout()
    return Response(saml_auth.get_last_response_xml(), media_type="application/xml")

@router.post("/sls")
async def sls(request: Request):
    saml_auth = OneLogin_Saml2_Auth(request, saml_config)
    saml_auth.process_slo()
    if not saml_auth.is_authenticated():
        return {"success": "Logged out"}
    return {"error": "Logout failed"}

@router.get("/login")
async def login(request: Request):
    # Parse the SAML response from the request body
    # form_data = await request.form()
    # SAMLResponse = form_data.get('SAMLResponse')
    SAMLResponse = True

    if SAMLResponse:
        # TODO: Parse and validate the SAMLResponse
        # If it's valid, create a JWT for the user

        refresh_token_payload = {
            "exp": datetime.utcnow() + timedelta(days=7),  # Expires in 7 days
            "iat": datetime.utcnow(),
            "sub": "user-id",  # Replace with the actual user ID
            "type": "refresh",  # Add a type to distinguish between access and refresh tokens
        }

        # Generate the JWTs
        refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

        # Redirect the user back to the Vue application
        response = JSONResponse(content={"status": "success"}, status_code=200)

        # Set the tokens as secure, HttpOnly cookies in the response
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="strict")

        return response

    else:
        return JSONResponse(status_code=400, content={"detail": "Invalid SAML response"})


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

        # You could also add additional checks here (e.g., is the token expired?)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")
        
        if payload.get("exp") < datetime.utcnow().timestamp():
            raise HTTPException(status_code=400, detail="Token is expired")

        return {"isAuthenticated": True}
    except Exception as e:
        return {"isAuthenticated": False}
