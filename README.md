# ms-notifications

Microservicio Flask para envio de correos de autenticacion 2FA con Gmail API.

Los correos 2FA se envian en formato texto + HTML (multipart) e incluyen una confirmacion explicita del tiempo de expiracion del codigo.

## Estructura

- `app.py`: punto de entrada del servicio.
- `notifications/config.py`: configuracion del servicio.
- `notifications/gmail_client.py`: autenticacion OAuth y envio Gmail.
- `notifications/services/two_factor_mailer.py`: logica de negocio de 2FA.
- `notifications/routes/two_factor.py`: endpoint HTTP para envio de codigo.

## Requisitos

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Configuracion

Variables opcionales:

- `GMAIL_CREDENTIALS_PATH` (default: `confidencial/credentials.json`)
- `GMAIL_TOKEN_PATH` (default: `confidencial/token.pickle`)
- `GMAIL_SENDER` (default: `luis.balaguera35298@ucaldas.edu.co`)
- `NOTIFICATIONS_DRY_RUN` (default: `false`)

## Ejecutar

```bash
python app.py
```

Servicio en `http://localhost:5000`.

## Endpoint principal

`POST /api/v1/2fa/send`

Body:

```json
{
  "to": "usuario@correo.com",
  "code": "123456",
  "ttl_minutes": 5,
  "request_id": "optional-trace-id"
}
```

`ttl_minutes` debe ser un entero mayor a `0`.

Respuesta exitosa:

```json
{
  "status": "ok",
  "message_id": "gmail-message-id",
  "dry_run": false,
  "request_id": "optional-trace-id"
}

## Prueba local sin Gmail OAuth

Para validar integracion con backend sin flujo OAuth de Gmail:

```bash
set NOTIFICATIONS_DRY_RUN=true
python app.py
```


