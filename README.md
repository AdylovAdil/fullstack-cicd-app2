# Full-Stack приложение с CI/CD

Готовый проект для лабораторной работы:
- Frontend: React + Vite
- Backend: Flask API
- Database: PostgreSQL
- CI: GitHub Actions
- CD: Railway

## Структура

```text
fullstack-app/
├── .github/workflows/ci.yml
├── frontend/
└── backend/
```

## Что умеет приложение

- показывает список записей из API
- добавляет новую запись
- удаляет запись
- отображает имя студента и ID студента

## Backend API

### GET /api/data
Получить все записи.

### POST /api/data
Добавить запись.

Пример JSON:
```json
{ "title": "Новая задача" }
```

### DELETE /api/data/:id
Удалить запись по id.

### GET /api/health
Проверка, что backend работает.

## Локальный запуск

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

Backend будет доступен на:
`http://localhost:5000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен на:
`http://localhost:5173`

## Переменные окружения

### Backend
- `DATABASE_URL` — строка подключения к PostgreSQL на Railway
- `PORT` — порт backend сервиса

Если `DATABASE_URL` не задан, приложение использует SQLite локально.

### Frontend
- `VITE_API_URL` — URL backend API
- `VITE_STUDENT_NAME` — имя студента
- `VITE_STUDENT_ID` — ID студента

## GitHub Actions CI

Файл `.github/workflows/ci.yml` запускает тесты backend при каждом push в `main`.

## Railway Deployment

### 1. Database
Создай:
**New → Database → PostgreSQL**

Railway сам создаст переменную:
- `DATABASE_URL`

### 2. Backend
Создай сервис из GitHub repo:
- Root Directory: `/backend`
- Variables:
  - `DATABASE_URL` → Reference из PostgreSQL
  - `PORT=5000`

Потом:
- Settings → Networking → Generate Domain

### 3. Frontend
Создай отдельный сервис:
- Root Directory: `/frontend`
- Variables:
  - `VITE_API_URL=https://your-backend-domain`
  - `VITE_STUDENT_NAME=Adil`
  - `VITE_STUDENT_ID=YOUR_STUDENT_ID`

## Что сдавать

- URL GitHub repository
- URL Frontend на Railway
- URL Backend API на Railway
- Скриншот зелёного GitHub Actions

## Примечание

Тебе нужно только:
1. вставить свой student ID в `VITE_STUDENT_ID`
2. загрузить проект в GitHub
3. подключить Railway
