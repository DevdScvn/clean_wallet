# API для управления кошельками пользователей

Проект написан с использованием чистой архитектуры для удобного распределения слоев.

### 1. Клонируйте репозиторий и перейдите в каталог
```bash
git clone 
```
```bash
cd clean-backend
```
```bash
cd src
```
Опционально:
- если работа в PyChame сделать папку src, как sources root

### 2. Создайте виртуальное окружение и установите зависимости

```bash
uv sync
```

Команда `uv sync`:
- создаёт виртуальное окружение (если его нет);
- устанавливает зависимости из `pyproject.toml`;
- использует версии из `uv.lock` для воспроизводимой сборки.

###  Активируйте окружение (опционально)

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```



## Запуск через Docker

Все сервисы поднимаются одной командой:

```bash
docker compose up -d
```


## Запусук проекта локально без Dockerfile

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

Запуск воркера faststream c созданием очереди в rabbitmq

```bash
uv run faststream run clean_backend/fs_serve_app:faststream_app

```
Подъем миграций 

```bash
alembic upgrade head

```

## Использование приложения

1. Перейдите на ресурс http://localhost:5050/docs

    Роутеры распределены на v1 и v2

   - **v1**: Представляет restapi, включающее создание пользователей, управлением кошельком
   - **v2**: создание очереди для создания пользователей
2. Создайте пользователя по ресурсу POST /api/v1/users/
   - **{
  "username": "Name"
}**
3. С полученным ID пользователя - создайте кошелек по ресурсу POST /api/v1/wallets/
- **{
  "balance": 0,
  "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
}**

4. Добавьте/Убавьте необходимое количество суммы по ресурсу POST /api/v1/wallets/{wallet_id}/operation 
Передав id в параметрах ресурса

   
- **{
  "operation_type": "DEPOSIT",
  "amount": 1
}**

- -**{
  "operation_type": "WITHDRAW",
  "amount": 1
}**

5. Получите информацию о кошельке по ресурсу GET /api/v1/wallets/{wallet_id}/
 - **{
  "balance": "0.00",
  "username": "Name"
}**