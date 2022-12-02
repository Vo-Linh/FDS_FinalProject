FROM python:3.8-slim

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["uvicorn", "ui:app", "--host", "0.0.0.0", "--port", "80"]
