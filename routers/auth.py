import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd

logger = logging.getLogger(__name__)

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

users_db = {}

ratings = pd.read_csv('datasets/ratings.csv')

class User:
    def __init__(self, username: str, email: str, full_name: Optional[str] = None, disabled: bool = False, userId: int = None):
        self.username = username
        self.email = email
        self.full_name = full_name
        self.disabled = disabled
        self.userId = userId

def get_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError as e:
        logger.error(f"Token decoding failed: {e}")
        raise credentials_exception
    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

router = APIRouter()

@router.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Registering user: {form_data.username}")
    if form_data.username in users_db:
        logger.warning(f"Username {form_data.username} already exists.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    hashed_password = get_password_hash(form_data.password)
    new_user_id = ratings['userId'].max() + 1
    users_db[form_data.username] = {
        "username": form_data.username,
        "email": "",
        "full_name": "",
        "hashed_password": hashed_password,
        "disabled": False,
        "userId": new_user_id
    }
    logger.info(f"User {form_data.username} registered successfully with userId {new_user_id}.")
    return {"message": "User registered successfully"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Login attempt for user: {form_data.username}")
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, users_db[user.username].get('hashed_password')):
        logger.warning(f"Invalid login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "userId": user.userId}, expires_delta=access_token_expires
    )
    logger.info(f"User {form_data.username} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}
