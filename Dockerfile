FROM python:3.10-slim

WORKDIR /app

COPY ./requirements/prod.txt requirements.txt
RUN pip3 install --upgrade pip -r requirements.txt

COPY . .


CMD [ "python3", "-m" , "main"]
