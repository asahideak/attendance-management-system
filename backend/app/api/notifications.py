"""
勤怠管理システム - 通知管理API
"""
from fastapi import APIRouter
from app.schemas.auth import ApiResponse

router = APIRouter()

@router.get("/", response_model=ApiResponse)
async def get_notifications():
    """通知一覧取得"""
    return ApiResponse(
        success=True,
        message="通知一覧を取得しました",
        data={"notifications": []}
    )