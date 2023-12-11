from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import init_db
from app.routers import userRouter
from app.routers import fileScanRouter
from app.routers import urlScanRouter
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
    return {"message": "Welcome to scanning project!"}


app.include_router(userRouter.router, prefix="/api/users")
app.include_router(fileScanRouter.router, prefix="/api/file-scan")
app.include_router(urlScanRouter.router, prefix="/api/url-scan")