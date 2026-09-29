@echo off

echo Starting EduGenie...

call .venv\Scripts\activate

uvicorn main:app --reload

pause