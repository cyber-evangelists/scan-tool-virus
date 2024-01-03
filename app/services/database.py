from beanie import init_beanie
import motor.motor_asyncio
import asyncio
from app.services.logs import logger
from app.constants.config import mongo_url
from app.models.db_models.user import User
<<<<<<< HEAD

async def init_db():
    try:
        database_name = "files-scanner"
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        client.get_io_loop = asyncio.get_running_loop
        await init_beanie(database=client[database_name], document_models=[User])
=======
from app.models.db_models.fileScan import FileScan
from app.models.db_models.urlScan import UrlScan

async def init_db():
    try:
        database_name = "scanner-db"
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
        client.get_io_loop = asyncio.get_running_loop
        await init_beanie(database=client[database_name], document_models=[User, FileScan, UrlScan])
>>>>>>> c18931cd379c94ab8ef653a2d07b3d6f15040e9e
        logger.info('Database connected.')
    except Exception as err:
        logger.error(f'Database connection failed, error is: {err}')