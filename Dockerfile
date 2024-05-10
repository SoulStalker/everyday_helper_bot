FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache -r /app/requirements.txt

# Копируем все файлы, кроме .env
COPY . /app/

# Запускаем приложение
CMD ["python", "-m", "bot"]
