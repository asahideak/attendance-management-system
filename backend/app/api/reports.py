"""
勤怠管理システム - レポートAPI
"""
from fastapi import APIRouter
from app.schemas.auth import ApiResponse

router = APIRouter()

@router.get("/", response_model=ApiResponse)
async def get_reports():
    """レポート一覧取得"""
    return ApiResponse(
        success=True,
        message="レポート一覧を取得しました",
        data={"reports": []}
    )