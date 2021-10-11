# Copyright 2021 Mario Román Dono
# Copyright 2018 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os
import json
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

sender = os.getenv("FROM_EMAIL")
to = os.getenv("TO_EMAIL")
subject = os.getenv("SUBJECT_EMAIL")
creds_var = json.loads(base64.b64decode(os.getenv("GMAIL_CREDENTIALS")))
token_var = json.loads(base64.b64decode(os.getenv("GMAIL_TOKEN")))

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message_text(json_object):
  json_dict = json.loads(json_object)

  if "data" in json_dict: # Solo se genera el texto del mensaje si existen tweets
    texto = "Se han encontrado los siguientes tweets (de más nuevo a más antiguo):\n\n"
    for tweet in json_dict["data"]:
      texto += tweet["text"] + "\n"
      # Se utiliza el nombre de usuario twitter porque no importa cuál se ponga. Referencia: https://blog.twitter.com/developer/en_us/topics/tips/2020/getting-to-the-canonical-url-for-a-tweet
      texto += f'Enlace: https://twitter.com/twitter/status/{tweet["id"]}\n' 
      texto += '-------------------------------------------------------------\n'
    return texto
  else:
    return None


def connect_to_api():
    creds = None
    if (os.path.exists("token.json")):
      creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    elif (os.getenv("GMAIL_TOKEN")):
      creds = Credentials.from_authorized_user_info(token_var, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = None
            if (os.path.exists("credentials.json")):
              flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            elif (os.getenv("GMAIL_TOKEN")):
              flow = InstalledAppFlow.from_client_config(creds_var, SCOPES)
            else:
              raise Exception("No credentials file or env variable!")
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print(f'Message Id: {message["id"]}')
    return message
  except HttpError as error:
    print(f'An error occurred: {error}')

def send_email(json):  
  message_text = create_message_text(json)
  if message_text is not None:
    serv = connect_to_api()
    msj = create_message(message_text)
    send_message(serv, "me", msj)
  else:
    print('No existen tweets nuevos para enviar')

if __name__ == "__main__":
  send_email()