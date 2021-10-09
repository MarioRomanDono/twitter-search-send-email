FROM python:3-alpine

WORKDIR /usr/src/app

RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

COPY . .

CMD [ "python", "./quickstart.py" ]