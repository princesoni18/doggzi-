from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.controllers.auth_controller import AuthController
from app.controllers.pet_controller import PetController
from app.database import get_db
from app.models.pet import Pet, PetCreate
from app.models.user import User



router = APIRouter(prefix="/pets", tags=["Pets"])

@router.get("/", response_model=List[Pet])
async def get_pets(
    current_user: User = Depends(AuthController.get_current_user),
    db = Depends(get_db)
):
    try:
        return await PetController.get_user_pets(db, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=Pet)
async def create_pet(
    pet_data: PetCreate,
    current_user: User = Depends(AuthController.get_current_user),
    db = Depends(get_db)
):
    try:
        return await PetController.create_pet(db, pet_data, current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
