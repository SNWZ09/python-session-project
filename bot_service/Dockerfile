FROM python:3.11-slim

#пишем рабочую папку внутри контейнера
WORKDIR /app

#устанавливаем виртуальное окружение
RUN pip install uv

#копируем pyproject.toml 
COPY pyproject.toml .

#запускаем виртуальное окружение
RUN uv sync

#копируем все файлы
COPY . .

#запускаем сервер
#к моему большому сожалению, одинарные кавычки тут не подойдут
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
