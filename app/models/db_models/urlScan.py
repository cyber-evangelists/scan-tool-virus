from beanie import Document
from typing import Any, Optional, Dict
from datetime import datetime
from bson.objectid import ObjectId

class UrlScan(Document):
    username: str
    url: str
    status: bool = False
    scan_report : Optional[Dict] = None
    error : Any = None
    created_at: datetime = datetime.now()
    # updated_at: datetime = datetime.now()
    
    class Settings:
        name = "UrlScan"


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise ValueError("ObjectId expected")
        return str(v)