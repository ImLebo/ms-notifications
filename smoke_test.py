import json
import urllib.request

payload = {
    "to": "destinatario@correo.com",
    "code": "123456",
    "ttl_minutes": 5,
    "request_id": "smoke-test",
}

req = urllib.request.Request(
    url="http://localhost:5000/api/v1/2fa/send",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=20) as response:
        print("STATUS:", response.status)
        print(response.read().decode("utf-8"))
except Exception as ex:
    print("ERROR:", ex)

