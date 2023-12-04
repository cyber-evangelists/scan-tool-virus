from fastapi import APIRouter, Depends
from fastapi import HTTPException, UploadFile, File, Form
from typing import Annotated
import shutil
import os
import uuid
from app.services.scanner import virus_scan
from app.auth.auth_bearer import JWTBearer

router = APIRouter()
os.makedirs("scan-files", exist_ok=True)

@router.post("/scan-file", dependencies=[Depends(JWTBearer())], tags=["file upload"])
async def upload_file(
    file: Annotated[UploadFile, File()]
) -> dict:
    
    original_file_name = file.filename
    content_type = file.content_type
    
    new_file_name = "scan-files" + "/" + str(uuid.uuid4()) + str(".") + str(content_type).split("/")[-1]
    
    with open(new_file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        report = virus_scan(original_file_name, new_file_name)
        # report = report.insert(0, {"filename": original_file_name})
        os.remove(new_file_name)
        return report
    except Exception as Err:
        os.remove(new_file_name)
        raise HTTPException(status_code=500, detail=f"Scan failed: {Err}")
    