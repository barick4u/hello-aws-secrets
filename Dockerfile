FROM python:3.14.3-slim

WORKDIR /app

COPY app.py .

CMD ["python", "app.py"]
