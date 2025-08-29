from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv


from bson import ObjectId

from app.database import get_db
from app.models.user import Token, TokenData, User, UserCreate, UserLogin

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class AuthController:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def get_user_by_email(db, email: str) -> Optional[User]:
        user_data = await db.users.find_one({"email": email})
        if user_data:
            user_data["id"] = user_data["_id"]
            return User(**user_data)
        return None

    @staticmethod
    async def authenticate_user(db, email: str, password: str) -> Optional[User]:
        user = await AuthController.get_user_by_email(db, email)
        if not user:
            return None
        if not AuthController.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def register_user(db, user_data: UserCreate) -> User:
        # Check if user already exists
        existing_user = await AuthController.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        # Create new user
        hashed_password = AuthController.get_password_hash(user_data.password)
        user_dict = {
            "email": user_data.email,
            "user_name": user_data.user_name,
            "hashed_password": hashed_password
        }
        result = await db.users.insert_one(user_dict)
        user_dict["id"] = result.inserted_id
        return User(**user_dict)

    @staticmethod
    async def login_user(db, user_credentials: UserLogin):
        user = await AuthController.authenticate_user(
            db, user_credentials.email, user_credentials.password
        )
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthController.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        user_public = {
            "id": user.id,
            "email": user.email,
            "user_name": user.user_name
        }
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_public
        }

    @staticmethod
    async def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        
        user = await AuthController.get_user_by_email(db, email=token_data.email)
        if user is None:
            raise credentials_exception
        return user