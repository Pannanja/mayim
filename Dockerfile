FROM python:3.11-slim



EXPOSE 8080

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8080
