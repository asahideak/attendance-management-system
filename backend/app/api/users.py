"""
勤怠管理システム - ユーザー管理API
"""
from fastapi import APIRouter
from app.schemas.auth import ApiResponse

router = APIRouter()

@router.get("/", response_model=ApiResponse)
async def get_users():
    """ユーザー一覧取得"""
    return ApiResponse(
        success=True,
        message="ユーザー一覧を取得しました",
        data={"users": []}
    )