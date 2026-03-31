**Запусук проекта**

Из src
```bash
cd clean-backend

cd src

fastapi dev clean_backend/app.py

```
Или из корня проекта
```bash
uvicorn clean_backend.app:app

```


```bash
 uv run faststream run clean_backend/fs_app:faststream_app

```


```bash
uv run faststream run clean_backend/fs_serve_app:faststream_app

```


```bash
alembic revision --autogenerate -m "create wallet model"

```

```bash
alembic upgrade head

```

