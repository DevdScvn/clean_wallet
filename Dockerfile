FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends curl bash && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock* ./
COPY clean-backend ./clean-backend
RUN pip install --no-cache-dir uv \
    && uv sync --frozen --no-dev || uv sync --no-dev

ENV PATH="/app/.venv/bin:${PATH}"

COPY . .

EXPOSE 8000

RUN chmod +x /app/clean-backend/src/prestart.sh

WORKDIR /app/clean-backend/src

ENTRYPOINT ["/app/clean-backend/src/prestart.sh"]

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "clean_backend/app.py"]
