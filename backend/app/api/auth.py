"""
勤怠管理システム - 認証API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest, LoginResponse, User, AuthUser,
    RefreshTokenRequest, PasswordResetRequest,
    PasswordChangeRequest, ApiResponse
)
import jwt
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter()
security = HTTPBearer()

# 仮のユーザーデータ（実際はデータベースから取得）
DEMO_USERS = {
    "1000001": {
        "id": "user_001",
        "employee_number": "1000001",
        "name": "山田太郎",
        "email": "yamada@company.jp",
        "password": "password123",  # 実際はハッシュ化
        "role": "general",
        "company_code": "1",
        "department_code": "DEV",
        "is_active": True
    },
    "2000001": {
        "id": "admin_001",
        "employee_number": "2000001",
        "name": "管理者太郎",
        "email": "admin@company.jp",
        "password": "admin123",
        "role": "admin",
        "company_code": "2",
        "department_code": "ADMIN",
        "is_active": True
    }
}

def create_access_token(user_data: dict) -> str:
    """アクセストークン生成"""
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    to_encode = {
        "user_id": user_data["id"],
        "employee_number": user_data["employee_number"],
        "role": user_data["role"],
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def create_refresh_token(user_data: dict) -> str:
    """リフレッシュトークン生成"""
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode = {
        "user_id": user_data["id"],
        "employee_number": user_data["employee_number"],
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

@router.post("/login", response_model=ApiResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """ユーザーログイン"""
    # ユーザー認証（実際はデータベースから取得 & パスワード検証）
    user_data = DEMO_USERS.get(request.employee_number)

    if not user_data or user_data["password"] != request.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="社員番号またはパスワードが正しくありません"
        )

    if not user_data["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="アカウントが無効です"
        )

    # トークン生成
    access_token = create_access_token(user_data)
    refresh_token = create_refresh_token(user_data)

    # ユーザー情報作成
    user = User(**{k: v for k, v in user_data.items() if k != "password"})

    return ApiResponse(
        success=True,
        message="ログインに成功しました",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.jwt_expire_minutes * 60,
            "user": user.dict()
        }
    )

@router.post("/refresh", response_model=ApiResponse)
async def refresh_token(request: RefreshTokenRequest):
    """トークンリフレッシュ"""
    try:
        payload = jwt.decode(
            request.refresh_token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="無効なリフレッシュトークンです")

        employee_number = payload.get("employee_number")
        user_data = DEMO_USERS.get(employee_number)

        if not user_data or not user_data["is_active"]:
            raise HTTPException(status_code=401, detail="ユーザーが見つかりません")

        # 新しいトークン生成
        new_access_token = create_access_token(user_data)
        new_refresh_token = create_refresh_token(user_data)

        return ApiResponse(
            success=True,
            message="トークンを更新しました",
            data={
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer",
                "expires_in": settings.jwt_expire_minutes * 60
            }
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="リフレッシュトークンが期限切れです")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="無効なリフレッシュトークンです")

@router.post("/logout", response_model=ApiResponse)
async def logout():
    """ログアウト"""
    return ApiResponse(
        success=True,
        message="ログアウトしました"
    )

@router.get("/me", response_model=ApiResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """現在のユーザー情報取得"""
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )

        employee_number = payload.get("employee_number")
        user_data = DEMO_USERS.get(employee_number)

        if not user_data:
            raise HTTPException(status_code=401, detail="ユーザーが見つかりません")

        user = User(**{k: v for k, v in user_data.items() if k != "password"})

        return ApiResponse(
            success=True,
            message="ユーザー情報を取得しました",
            data={"user": user.dict()}
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="トークンが期限切れです")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="無効なトークンです")

@router.post("/password/reset", response_model=ApiResponse)
async def password_reset(request: PasswordResetRequest):
    """パスワードリセット"""
    return ApiResponse(
        success=False,
        message="パスワードリセット機能は現在開発中です",
        errors=["機能が実装されていません"]
    )

@router.post("/password/change", response_model=ApiResponse)
async def password_change(request: PasswordChangeRequest):
    """パスワード変更"""
    return ApiResponse(
        success=False,
        message="パスワード変更機能は現在開発中です",
        errors=["機能が実装されていません"]
    )