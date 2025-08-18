import jwt
import secrets
import time
from typing import Optional

from app.config.settings import settings


class OAuthStateError(Exception):
    """Raised when OAuth state validation fails"""
    pass


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