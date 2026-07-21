from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from app.utils.jwt import decode_access_token
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token:str = Depends(oauth2_scheme)):
    """
    Dependency lấy và xác thực token từ Request Header.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", 
        header={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload=decode_access_token(token)
        username :str=payload.get("sub")
        if username is None: 
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
