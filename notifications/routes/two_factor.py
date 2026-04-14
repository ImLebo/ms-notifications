from flask import Blueprint, request

from notifications.services.two_factor_mailer import TwoFactorMailer

two_factor_bp = Blueprint("two_factor", __name__, url_prefix="/api/v1/2fa")
mailer = TwoFactorMailer()


@two_factor_bp.post("/send")
def send_two_factor_email():
    data = request.get_json(silent=True) or {}

    to = data.get("to")
    code = data.get("code")
    ttl_minutes = data.get("ttl_minutes", 5)
    request_id = data.get("request_id")

    try:
        ttl_minutes = int(ttl_minutes)
        if ttl_minutes <= 0:
            raise ValueError("ttl_minutes debe ser mayor a 0")

        result = mailer.send_code(to=to, code=code, ttl_minutes=ttl_minutes)
        return {
            "status": "ok",
            "message_id": result.get("id"),
            "dry_run": result.get("dry_run", False),
            "request_id": request_id,
        }, 200
    except ValueError as ex:
        return {"status": "error", "message": str(ex), "request_id": request_id}, 400
    except Exception as ex:
        return {
            "status": "error",
            "message": f"No fue posible enviar el correo 2FA: {str(ex)}",
            "request_id": request_id,
        }, 502


