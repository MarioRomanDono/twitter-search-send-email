import base64
import os
import json
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError

sender = os.environ.get("FROM_EMAIL")
to = os.environ.get("TO_EMAIL")
subject = os.environ.get("SUBJECT_EMAIL")
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
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def create_message(message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
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

if __name__ == "__main__":
  send_email()
