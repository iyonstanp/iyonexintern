import base64
import json
import os
import re
import secrets
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler


def send_json(handler, status, payload):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("X-Content-Type-Options", "nosniff")
    handler.end_headers()
    handler.wfile.write(body)


def read_json(handler):
    try:
        length = int(handler.headers.get("Content-Length", "0"))
        if length < 1 or length > 8192:
            return None
        return json.loads(handler.rfile.read(length).decode("utf-8"))
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        payload = read_json(self)
        if not isinstance(payload, dict):
            return send_json(self, 400, {"error": "A valid JSON request is required."})

        amount = payload.get("amount")
        reference = payload.get("reference", "")
        name = str(payload.get("name", "")).strip()[:80]
        email = str(payload.get("email", "")).strip()[:120]

        if isinstance(amount, bool) or not isinstance(amount, int) or amount < 100:
            return send_json(self, 400, {"error": "Amount must be an integer of at least 100 paise."})
        if amount > 100000000:
            return send_json(self, 400, {"error": "Amount exceeds the online checkout limit of INR 10,00,000."})
        if not isinstance(reference, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,40}", reference):
            return send_json(self, 400, {"error": "Enter a valid IYONEX invoice or confirmation reference (letters, numbers, hyphens or underscores)."})
        if not name or not email or len(email) > 120 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return send_json(self, 400, {"error": "Enter your name and a valid email address."})

        key_id = os.environ.get("RAZORPAY_KEY_ID", "").strip()
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "").strip()
        if not key_id or not key_secret or key_secret.startswith("REPLACE_WITH_"):
            return send_json(self, 503, {"error": "Online payments are not configured yet. Please contact IYONEX."})

        receipt = reference[:30] + "-" + secrets.token_hex(4)
        order_payload = {
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "notes": {
                "iyონex_reference": reference,
                "customer_name": name,
                "customer_email": email
            }
        }
        auth = base64.b64encode((key_id + ":" + key_secret).encode("utf-8")).decode("ascii")
        request = urllib.request.Request(
            "https://api.razorpay.com/v1/orders",
            data=json.dumps(order_payload).encode("utf-8"),
            headers={
                "Authorization": "Basic " + auth,
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                order = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            status = 401 if exc.code == 401 else 502
            return send_json(self, status, {"error": "Razorpay rejected the order request. Check the test API credentials and account configuration."})
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return send_json(self, 502, {"error": "Could not reach Razorpay. Please try again."})

        if not order.get("id"):
            return send_json(self, 502, {"error": "Razorpay did not return an order ID."})

        return send_json(self, 201, {
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": key_id
        })

    def do_GET(self):
        return send_json(self, 405, {"error": "Method not allowed."})

    def log_message(self, format, *args):
        # Avoid writing customer information or payment payloads to function logs.
        return
