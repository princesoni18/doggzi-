

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from app.controllers.auth_controller import AuthController
from app.database import get_db
from app.models.user import Token, UserCreate, UserLogin
from app.utils.logger import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])



@router.post("/register", response_model=Token)
async def register(
    user_data: UserCreate,
    db = Depends(get_db)
):
    try:
        user = await AuthController.register_user(db, user_data)
        # Generate token for the new user
        access_token_expires = timedelta(minutes=30)
        access_token = AuthController.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        user_public = {
            "id": user.id,
            "email": user.email,
            "user_name": user.user_name
        }
        logger.info(f"User registered: {user.email}")
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user_public
        }
    except HTTPException:
        logger.warning("HTTPException during registration")
        raise
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")



@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db = Depends(get_db)
):
    try:
        response = await AuthController.login_user(db, user_credentials)
        logger.info(f"User logged in: {user_credentials.email}")
        return response
    except HTTPException:
        logger.warning("HTTPException during login")
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
