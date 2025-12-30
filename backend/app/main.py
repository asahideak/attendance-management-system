"""
勤怠管理システム - メインアプリケーション
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, attendance, users, notifications, reports

# FastAPIアプリケーション作成
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Bluetoothビーコン勤怠管理システム API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーター登録
app.include_router(auth.router, prefix="/api/auth", tags=["認証"])
app.include_router(attendance.router, prefix="/api/attendance", tags=["勤怠管理"])
app.include_router(users.router, prefix="/api/users", tags=["ユーザー管理"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["通知管理"])
app.include_router(reports.router, prefix="/api/reports", tags=["レポート"])

@app.get("/", tags=["基本"])
async def root():
    """ルートエンドポイント"""
    return {"message": f"{settings.app_name} v{settings.app_version}"}

@app.get("/health", tags=["基本"])
async def health_check():
    """ヘルスチェック"""
    return {"status": "healthy", "service": settings.app_name}