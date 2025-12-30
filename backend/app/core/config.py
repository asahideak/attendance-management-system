"""
勤怠管理システム - 設定管理
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """アプリケーション設定"""

    # アプリケーション基本設定
    app_name: str = "勤怠管理システムAPI"
    app_version: str = "1.0.0"
    debug: bool = False

    # データベース設定
    database_url: str

    # JWT設定
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 480  # 8時間

    # CORS設定
    cors_origins: list[str] = ["https://frontend-kwaka.vercel.app"]

    # セキュリティ設定
    session_secret: str

    # Firebase設定（通知用）
    firebase_server_key: Optional[str] = None

    # Google Cloud設定
    google_cloud_project_id: Optional[str] = None

    class Config:
        env_file = "../.env.local"
        case_sensitive = False


settings = Settings()