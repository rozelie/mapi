FROM python:3.9.13-slim-buster

RUN apt-get update

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install /app

EXPOSE 80
CMD ["python", "-m" , "myapi"]