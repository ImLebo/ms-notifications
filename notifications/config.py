import os


class Config:
    GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
    GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH", "confidencial/credentials.json")
    GMAIL_TOKEN_PATH = os.getenv("GMAIL_TOKEN_PATH", "confidencial/token.pickle")
    GMAIL_SENDER = os.getenv("GMAIL_SENDER", "luis.balaguera35298@ucaldas.edu.co")
    DRY_RUN = os.getenv("NOTIFICATIONS_DRY_RUN", "false").lower() == "true"


