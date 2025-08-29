from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routers.auth import router as auth
from app.routers.pet import router as pets
from dotenv import load_dotenv
load_dotenv()

from app.database import close_mongo_connection, connect_to_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Pet Management API",
    description="A FastAPI backend for managing pets with user authentication",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth)
app.include_router(pets)

@app.get("/")
async def root():
    return {"message": "Pet Management API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

