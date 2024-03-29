FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000 80

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]