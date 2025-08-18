import jwt
import secrets
import time
from typing import Optional

import httpx
from app.config.settings import settings
from app.exception.auth_exception import SignupFailed
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


class OAuthStateError(Exception):
    """Raised when OAuth state validation fails"""
    pass


# OAuth error code to internal error code mapping
OAUTH_ERROR_MAPPING = {
    "access_denied": "oauth_cancelled",
    "invalid_request": "oauth_invalid_request",
    "unauthorized_client": "oauth_unauthorized",
    "unsupported_response_type": "oauth_unsupported",
    "invalid_scope": "oauth_invalid_scope",
    "server_error": "oauth_server_error",
    "temporarily_unavailable": "oauth_unavailable",
}


def map_oauth_error(error_code: str) -> str:
    """
    Map OAuth error code to internal error code.
    
    Args:
        error_code: OAuth error code from provider
        
    Returns:
        str: Internal error code for frontend display
    """
    return OAUTH_ERROR_MAPPING.get(error_code, "oauth_error")


async def exchange_oauth_code_for_user_info(auth_code: str) -> dict:
    """
    Exchange OAuth authorization code for user information.
    
    Args:
        auth_code: Authorization code from OAuth provider
        
    Returns:
        dict: User information from ID token
        
    Raises:
        SignupFailed: If token exchange or verification fails
    """
    try:
        # Exchange authorization code for tokens
        token_url = "https://oauth2.googleapis.com/token"
        redirect_uri = f"{settings.base_api_url}/auth/oauth/google/callback"

        token_data = {
            "client_id": settings.google_client_id,
            "client_secret": settings.google_client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_response.raise_for_status()
            tokens = token_response.json()

        # Verify the ID token
        id_info = id_token.verify_oauth2_token(
            tokens["id_token"],
            google_requests.Request(),
            audience=settings.google_client_id,
        )
        return id_info
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"OAuth token exchange failed: {e}")
        raise SignupFailed("OAuth authentication failed")


def generate_oauth_state() -> str:
    """
    Generate a secure OAuth state parameter using JWT.
    
    Returns:
        str: JWT token containing state data with expiration
    """
    state_data = {
        "nonce": secrets.token_urlsafe(16),
        "iat": int(time.time()),  # issued at
        "exp": int(time.time()) + 600,  # expires in 10 minutes
        "purpose": "oauth_state"  # helps identify token purpose
    }
    
    return jwt.encode(
        state_data, 
        settings.jwt_secret_key, 
        algorithm="HS256"
    )


def validate_oauth_state(state: Optional[str]) -> bool:
    """
    Validate OAuth state parameter JWT token.
    
    Args:
        state: JWT token to validate
        
    Returns:
        bool: True if valid, False otherwise
        
    Raises:
        OAuthStateError: If state is invalid with specific error details
    """
    if not state:
        raise OAuthStateError("State parameter is missing")
    
    try:
        # Decode and validate JWT
        payload = jwt.decode(
            state, 
            settings.jwt_secret_key, 
            algorithms=["HS256"]
        )
        
        # Additional validation
        if payload.get("purpose") != "oauth_state":
            raise OAuthStateError("Invalid state token purpose")
            
        return True
        
    except jwt.ExpiredSignatureError:
        raise OAuthStateError("State token has expired")
    except jwt.InvalidTokenError as e:
        raise OAuthStateError(f"Invalid state token: {str(e)}")
    except Exception as e:
        raise OAuthStateError(f"State validation failed: {str(e)}")