#!/usr/bin/env bash
set -e
set -x

alembic upgrade head

# RabbitMQ может стартовать чуть позже app-контейнера.
# Делаем ожидание по host/port, которые задаются через BACKEND__BROKER__RABBIT__*.
python - <<'PY'
import os
import socket
import time

host = os.environ.get("BACKEND__BROKER__RABBIT__HOST", "localhost")
port = int(os.environ.get("BACKEND__BROKER__RABBIT__PORT", "5672"))

timeout_s = 2
retries = 60  # ~60 секунд

for i in range(retries):
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            print(f"RabbitMQ is reachable at {host}:{port}")
            break
    except OSError:
        if i == retries - 1:
            raise
        print(f"Waiting for RabbitMQ {host}:{port} ({i+1}/{retries})...")
        time.sleep(1)
PY

exec "$@"
