FROM python:3.9.13-slim-buster

RUN apt-get update

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install /app

EXPOSE 8000
CMD ["uvicorn", "mapi.api:app", "--host", "0.0.0.0", "--port", "8000"]