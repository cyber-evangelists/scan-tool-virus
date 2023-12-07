from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException, UploadFile, File, Form
from fastapi.security.utils import get_authorization_scheme_param
from beanie import PydanticObjectId
import json
from typing import Annotated
import shutil
import os
import uuid
from app.services.scanner import virus_scan
from app.auth.auth_bearer import JWTBearer
from app.services.logs import logger
from app.auth.auth_handler import decodeJWT
from app.models.db_models.fileScan import FileScan

router = APIRouter()
os.makedirs("scan-files", exist_ok=True)

@router.post("/scan-file", dependencies=[Depends(JWTBearer())], tags=["File Scan"])
async def upload_file(
    request: Request,
    file: Annotated[UploadFile, File()]
) -> dict:
    header_authorization: str = request.headers.get("Authorization")
    header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
    username = decodeJWT(header_param)["username"]
    original_file_name = file.filename
    content_type = file.content_type
    
    new_file_name = "scan-files" + "/" + str(uuid.uuid4()) + str(".") + str(original_file_name).split(".")[-1]
    
    with open(new_file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        report = virus_scan(original_file_name, new_file_name)
        os.remove(new_file_name)
        new_obj = FileScan(
                username=username,
                filename=original_file_name,
                status=True,
                scan_report=report,
            )
        new_obj = await new_obj.save()
        scan_id = str(new_obj.id)
        logger.info(f"successful scan {scan_id} inserted in database")
        return {
            "scan_id": str(new_obj.id),
            "username": new_obj.username,
            "filename": new_obj.filename,
            "status": new_obj.status,
            "scan_report": new_obj.scan_report,
            "created_at": new_obj.created_at
            
        }
    except Exception as Err:
        os.remove(new_file_name)
        new_obj = FileScan(
                username=username,
                filename=original_file_name,
                error=Err,
            )
        new_obj = await new_obj.save()
        scan_id = str(new_obj.id)
        logger.info(f"failed scan {scan_id} inserted in database")
        raise HTTPException(status_code=500, detail=f"Scan failed: {Err}")


@router.get("/get-scans", dependencies=[Depends(JWTBearer())], tags=["File Scan"])
async def get_scans(
    request: Request,
):
    header_authorization: str = request.headers.get("Authorization")
    header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
    username = decodeJWT(header_param)["username"]
    try:
        scans_report = await FileScan.find({"username": username}).to_list(length=None)
        return {"scans_data": scans_report}
    except Exception as Err:
        raise HTTPException(status_code=500, detail=f"proccess failed: {Err}")
    
    
@router.get("/get-scan-report", dependencies=[Depends(JWTBearer())], tags=["File Scan"])
async def get_scan_report(
    scanId: str,
) -> dict:
    if not PydanticObjectId.is_valid(scanId):
        raise HTTPException(status_code=400, detail=f"invalid input type")
    try:
        new_obj = await FileScan.get(scanId)
        if new_obj:
            return {
                "scan_id": str(new_obj.id),
                "username": new_obj.username,
                "filename": new_obj.filename,
                "status": new_obj.status,
                "scan_report": new_obj.scan_report,
                "created_at": new_obj.created_at
                
            }
        raise Exception("scan id not found")
    except Exception as Error:
        raise HTTPException(
            status_code=500,
            detail=f"error while fetching the object: {Error}",
        )
        
        