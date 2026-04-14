import base64
import unittest
from email import message_from_bytes

from flask import Flask

from notifications.gmail_client import create_message
from notifications.services.two_factor_mailer import TwoFactorMailer


class EmailTemplateTests(unittest.TestCase):
    def test_create_message_builds_multipart_with_html(self):
        message = create_message(
            sender="no-reply@example.com",
            to="user@example.com",
            subject="Codigo 2FA",
            message_text="Este codigo expira en 5 minutos.",
            message_html="<p><strong>Tiempo de expiracion:</strong> 5 minutos.</p>",
        )

        raw = base64.urlsafe_b64decode(message["raw"].encode("utf-8"))
        parsed = message_from_bytes(raw)

        self.assertTrue(parsed.is_multipart())
        payload_types = [part.get_content_type() for part in parsed.get_payload()]
        self.assertIn("text/plain", payload_types)
        self.assertIn("text/html", payload_types)
        self.assertIn("multipart/alternative", parsed.get_content_type())

    def test_mailer_rejects_non_positive_ttl(self):
        app = Flask(__name__)
        app.config["DRY_RUN"] = True

        with app.app_context():
            with self.assertRaises(ValueError):
                TwoFactorMailer().send_code(
                    to="user@example.com",
                    code="123456",
                    ttl_minutes=0,
                )


if __name__ == "__main__":
    unittest.main()

