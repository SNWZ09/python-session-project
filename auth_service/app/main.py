# берем код из предыдущей работы (llm-p), которую можно найти на моём гитхабе,
# но немного редактируем:
# убираем импорт Middleware
# импортируем наш главный роутер
# импортируем настройки (это было)
# добавляем системную ручку /health
# добавим обработчик исключений

# для обработчика исключений нужно импортировать JSONResponse и Request
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# импорт роутера, настроек
from app.core.config import settings
from app.api.router import main_router

# импорт engine, Base и созданных исключений
from app.db.session import engine
from app.db.base import Base
from app.core.exceptions import BaseHTTPException


# собираем приложение
def create_app() -> FastAPI:

    # название берем из настроек
    app = FastAPI(title=settings.app_name)

    # подключаем роутер
    app.include_router(main_router)

    # событие запуска
    @app.on_event("startup")
    async def startup_event():
        # с запуском будут созданы все таблицы
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # событие выключения
    @app.on_event("shutdown")
    async def shutdown_event():
        await engine.dispose()

    # эндпоинт, который возвращает статус и окружение
    # для быстрой проверки сервера
    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "ok", "environment": settings.ENV}

    # обработчик исключений
    # FastAPI берет ошибку, переводит всё в JSONResponse и покажет юзеру
    # подготовленную в exceptions.py ошибку
    @app.exception_handler(BaseHTTPException)
    async def exception_handler_event(request: Request, exc: BaseHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    return app


app = create_app()
