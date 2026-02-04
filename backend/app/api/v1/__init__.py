from fastapi import APIRouter
from app.api.v1.endpoints import auth, logs, users, alert_rules

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(logs.router, prefix="/logs", tags=["Firewall Logs"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(alert_rules.router, prefix="/alert-rules", tags=["Alert Rules"])
