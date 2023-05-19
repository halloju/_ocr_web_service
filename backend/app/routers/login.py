from fastapi import APIRouter, Body, Depends, File, Response, Request, HTTPException, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
# from fastapi.security import OAuth2PasswordBearer
from fastapi import Cookie
from typing import Optional
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key"  # Replace with your actual secret key
ALGORITHM = "HS256"  # Or another algorithm like "RS256"


router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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
async def refresh_token(refresh_token: str):
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
        print(e)
        return {"isAuthenticated": False}
