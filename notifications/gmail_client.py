from __future__ import print_function

import base64
import os
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


def authenticate_gmail(credentials_path: str, token_path: str, scopes: list[str]):
    creds = None

    if os.path.exists(token_path):
        with open(token_path, "rb") as token_file:
            creds = pickle.load(token_file)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token_file:
            pickle.dump(creds, token_file)

    return creds


def create_message(
    sender: str,
    to: str,
    subject: str,
    message_text: str,
    message_html: str | None = None,
):
    if message_html:
        message = MIMEMultipart("alternative")
        message.attach(MIMEText(message_text, "plain", "utf-8"))
        message.attach(MIMEText(message_html, "html", "utf-8"))
    else:
        message = MIMEText(message_text, "plain", "utf-8")

    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {"raw": raw_message.decode()}


def send_message(service, user_id: str, message: dict):
    return service.users().messages().send(userId=user_id, body=message).execute()

