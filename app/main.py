from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import init_db
from app.routers import userRouter
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()
    
@app.get("/")
async def home():
    return {"message": "Welcome to Email scanning project!"}



app.include_router(userRouter.router, prefix="/api/users")