FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SDOT_CSV_PATH=/data/S_DOT_ENV_2026.07.27-08.02.csv

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir .

EXPOSE 8000

CMD ["uvicorn", "public_sensor_ml_mvp.dashboard.app:app", "--host", "0.0.0.0", "--port", "8000"]
