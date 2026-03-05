FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies cho psycopg2 + weasyprint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# BUG FIX: Tạo thư mục static trước để tránh warning W004
RUN mkdir -p /app/static

COPY . .

# BUG FIX 1: Dùng shell form để $PORT được expand đúng
# BUG FIX 2: Thêm migrate + collectstatic trước khi start
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --log-file -