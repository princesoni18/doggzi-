from fastapi import HTTPException, status, Depends
from typing import List
from bson import ObjectId
from app.models.pet import Pet, PetCreate
from app.models.user import User
from app.utils.logger import logger

class PetController:
    @staticmethod
    async def create_pet(db, pet_data: PetCreate, current_user: User) -> Pet:
        pet_dict = pet_data.dict()
        pet_dict["owner_id"] = current_user.id
        try:
            result = await db.pets.insert_one(pet_dict)
            pet_dict["id"] = result.inserted_id
            logger.info(f"Pet created for user: {current_user.email}")
            return Pet(**pet_dict)
        except Exception as e:
            logger.error(f"Error creating pet for user {current_user.email}: {e}")
            raise

    @staticmethod
    async def get_user_pets(db, current_user: User) -> List[Pet]:
        try:
            pets_cursor = db.pets.find({"owner_id": current_user.id})
            pets = []
            async for pet_data in pets_cursor:
                pet_data["id"] = pet_data["_id"]
                pets.append(Pet(**pet_data))
            logger.info(f"Fetched pets for user: {current_user.email}")
            return pets
        except Exception as e:
            logger.error(f"Error fetching pets for user {current_user.email}: {e}")
            raise