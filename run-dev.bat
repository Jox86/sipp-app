@echo off
echo Iniciando SIPP - Desarrollo integrado...
echo.

echo 1. Iniciando backend Django...
start cmd /k "cd backend && venv\Scripts\activate && python manage.py runserver"

echo 2. Iniciando frontend React...
start cmd /k "cd frontend && npm run dev"

echo.
echo URLs:
echo - Frontend: http://localhost:5173
echo - Backend API: http://127.0.0.1:8000/api/
echo - Django Admin: http://127.0.0.1:8000/admin/
echo.
pause