from fastapi import APIRouter, Depends, Request
from fastapi import HTTPException
from fastapi.security.utils import get_authorization_scheme_param
from beanie import PydanticObjectId
from app.services.url_scanner import url_scan
from app.auth.auth_bearer import JWTBearer
from app.services.logs import logger
from app.auth.auth_handler import decodeJWT
from app.models.db_models.urlScan import UrlScan
from app.models.request_models.urlScanRequest import UrlScanRequest

router = APIRouter()

@router.post("/scan", dependencies=[Depends(JWTBearer())], tags=["URL Scan"])
async def scan_url(
    request: Request,
    url: UrlScanRequest
) -> dict:
    target_url = url.url.strip()
    header_authorization: str = request.headers.get("Authorization")
    header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
    username = decodeJWT(header_param)["username"]
    
    try:
        report = url_scan(target_url)
        new_obj = UrlScan(
                username=username,
                url=target_url,
                status=True,
                scan_report=report,
            )
        new_obj = await new_obj.save()
        scan_id = str(new_obj.id)
        logger.info(f"successful url scan {scan_id} inserted in database")
        return {
            "scan_id": str(new_obj.id),
            "username": new_obj.username,
            "url": new_obj.url,
            "status": new_obj.status,
            "scan_report": new_obj.scan_report,
            "created_at": new_obj.created_at
            
        }
    except Exception as Err:
        new_obj = UrlScan(
                username=username,
                url=target_url,
                error=Err,
            )
        new_obj = await new_obj.save()
        scan_id = str(new_obj.id)
        logger.info(f"failed url scan {scan_id} inserted in database")
        raise HTTPException(status_code=500, detail=f"Scan failed: {Err}")


@router.get("/get-scans", dependencies=[Depends(JWTBearer())], tags=["URL Scan"])
async def get_scans(
    request: Request,
):
    header_authorization: str = request.headers.get("Authorization")
    header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
    username = decodeJWT(header_param)["username"]
    try:
        scans_report = await UrlScan.find({"username": username}).to_list(length=None)
        return {"scans_data": scans_report}
    except Exception as Err:
        raise HTTPException(status_code=500, detail=f"proccess failed: {Err}")
    
    
@router.get("/get-scan-report", dependencies=[Depends(JWTBearer())], tags=["URL Scan"])
async def get_scan_report(
    scanId: str,
) -> dict:
    if not PydanticObjectId.is_valid(scanId):
        raise HTTPException(status_code=400, detail=f"invalid input type")
    try:
        new_obj = await UrlScan.get(scanId)
        if new_obj:
            return {
                "scan_id": str(new_obj.id),
                "username": new_obj.username,
                "url": new_obj.url,
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
        
        