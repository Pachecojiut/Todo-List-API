from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> int:
    if credentials is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    user_id = decode_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return user_id




