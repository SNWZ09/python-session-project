from fastapi import APIRouter
from app.api.routes_auth import router as router_for_authentification

#тут главный роутер
main_router = APIRouter()

#присоединяем к главному роутеру эндпоинты из routes_auth.py
main_router.include_router(router_for_authentification)
