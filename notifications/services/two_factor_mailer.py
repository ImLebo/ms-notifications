import re
import uuid

from flask import current_app
from googleapiclient.discovery import build

from notifications.gmail_client import authenticate_gmail, create_message, send_message


class TwoFactorMailer:
    CODE_PATTERN = re.compile(r"^\d{6}$")

    def send_code(self, to: str, code: str, ttl_minutes: int = 5):
        if not to:
            raise ValueError("El campo 'to' es obligatorio")
        if not code or not self.CODE_PATTERN.match(code):
            raise ValueError("El código debe contener 6 dígitos")
        if ttl_minutes <= 0:
            raise ValueError("ttl_minutes debe ser mayor a 0")

        if current_app.config.get("DRY_RUN"):
            return {"id": f"dry-run-{uuid.uuid4()}", "dry_run": True}

        creds = authenticate_gmail(
            credentials_path=current_app.config["GMAIL_CREDENTIALS_PATH"],
            token_path=current_app.config["GMAIL_TOKEN_PATH"],
            scopes=current_app.config["GMAIL_SCOPES"],
        )
        service = build("gmail", "v1", credentials=creds)

        subject = "Codigo de verificacion de acceso (2FA)"
        body = (
            "Hola,\n\n"
            f"Tu codigo de verificacion es: {code}\n"
            f"Este codigo expira en {ttl_minutes} minutos.\n"
            "No compartas este codigo con nadie.\n\n"
            "Si no intentaste iniciar sesion, ignora este mensaje.\n"
        )
        body_html = f"""
<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Codigo 2FA</title>
</head>
<body style=\"margin:0;padding:0;background:#f3f6fb;font-family:Arial,Helvetica,sans-serif;color:#1f2937;\">
  <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"padding:24px 12px;\">
    <tr>
      <td align=\"center\">
        <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"max-width:560px;background:#ffffff;border-radius:12px;border:1px solid #e5e7eb;overflow:hidden;\">
          <tr>
            <td style=\"background:#0f172a;padding:18px 24px;color:#ffffff;font-size:16px;font-weight:700;\">Verificacion de acceso (2FA)</td>
          </tr>
          <tr>
            <td style=\"padding:24px;\">
              <p style=\"margin:0 0 12px 0;font-size:15px;line-height:1.6;\">Hola,</p>
              <p style=\"margin:0 0 16px 0;font-size:15px;line-height:1.6;\">Usa este codigo para completar tu inicio de sesion:</p>
              <div style=\"margin:0 0 16px 0;padding:14px 16px;border:1px dashed #94a3b8;border-radius:10px;background:#f8fafc;font-size:30px;letter-spacing:6px;font-weight:700;text-align:center;color:#0f172a;\">{code}</div>
              <p style=\"margin:0 0 12px 0;font-size:15px;line-height:1.6;\"><strong>Tiempo de expiracion:</strong> {ttl_minutes} minutos.</p>
              <p style=\"margin:0 0 12px 0;font-size:14px;line-height:1.6;color:#475569;\">No compartas este codigo con nadie.</p>
              <p style=\"margin:0;font-size:13px;line-height:1.6;color:#64748b;\">Si no intentaste iniciar sesion, ignora este mensaje.</p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""

        message = create_message(
            sender=current_app.config["GMAIL_SENDER"],
            to=to,
            subject=subject,
            message_text=body,
            message_html=body_html,
        )
        result = send_message(service, "me", message)
        result["dry_run"] = False
        return result


