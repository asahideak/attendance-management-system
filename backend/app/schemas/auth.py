"""
勤怠管理システム - 認証スキーマ
"""
from pydantic import BaseModel, Field
from typing import Optional


class LoginRequest(BaseModel):
    """ログインリクエスト"""
    employee_number: str = Field(..., description="社員番号", min_length=7, max_length=7)
    password: str = Field(..., description="パスワード", min_length=1)
    remember_me: bool = Field(default=False, description="ログイン状態保持")


class LoginResponse(BaseModel):
    """ログインレスポンス"""
    access_token: str = Field(..., description="アクセストークン")
    refresh_token: str = Field(..., description="リフレッシュトークン")
    token_type: str = Field(default="bearer", description="トークンタイプ")
    expires_in: int = Field(..., description="有効期限（秒）")


class User(BaseModel):
    """ユーザー情報"""
    id: str = Field(..., description="ユーザーID")
    employee_number: str = Field(..., description="社員番号")
    name: str = Field(..., description="氏名")
    email: str = Field(..., description="メールアドレス")
    role: str = Field(..., description="権限レベル")
    company_code: str = Field(..., description="会社コード")
    department_code: Optional[str] = Field(None, description="部署コード")
    is_active: bool = Field(..., description="アクティブ状態")


class AuthUser(BaseModel):
    """認証済みユーザー情報"""
    user: User
    permissions: list[str] = Field(..., description="権限リスト")


class RefreshTokenRequest(BaseModel):
    """トークンリフレッシュリクエスト"""
    refresh_token: str = Field(..., description="リフレッシュトークン")


class PasswordResetRequest(BaseModel):
    """パスワードリセットリクエスト"""
    employee_number: str = Field(..., description="社員番号")
    email: str = Field(..., description="メールアドレス")


class PasswordChangeRequest(BaseModel):
    """パスワード変更リクエスト"""
    current_password: str = Field(..., description="現在のパスワード")
    new_password: str = Field(..., description="新しいパスワード", min_length=8)
    confirm_password: str = Field(..., description="確認用パスワード")


class ApiResponse(BaseModel):
    """API共通レスポンス"""
    success: bool = Field(..., description="成功フラグ")
    message: str = Field(..., description="メッセージ")
    data: Optional[dict] = Field(None, description="レスポンスデータ")
    errors: Optional[list[str]] = Field(None, description="エラーリスト")