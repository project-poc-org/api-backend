import uuid
from datetime import datetime, timedelta

import jwt
import redis
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .settings import settings


security_scheme = HTTPBearer()
redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def _session_key(session_id: str) -> str:
    return f"session:{session_id}"


def create_access_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    session_id = uuid.uuid4().hex

    payload = {"sub": username, "exp": expire, "sid": session_id}
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    ttl_seconds = int(settings.access_token_expire_minutes * 60)
    redis_client.setex(_session_key(session_id), ttl_seconds, username)

    return token


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> str:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
        )
        username = payload.get("sub")
        session_id = payload.get("sid")
        if not username or not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )

        stored_username = redis_client.get(_session_key(session_id))
        if stored_username != username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session is invalid or has expired",
            )

        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def revoke_session(token: str) -> None:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"verify_exp": False},
        )
        session_id = payload.get("sid")
        if session_id:
            redis_client.delete(_session_key(session_id))
    except jwt.PyJWTError:
        return
