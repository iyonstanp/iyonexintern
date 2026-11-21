import base64
import hashlib
import hmac
import json
import os
import re
import secrets
import time
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

        # Temporary one-rupee LIVE gateway verification. Never accept an amount from the browser.
        amount = 100
        reference = "ESI-1M-LIVE-TEST"
        name = str(payload.get("name", "")).strip()[:80]
        email = str(payload.get("email", "")).strip()[:120]

        if amount != 100:
            return send_json(self, 400, {"error": "This temporary gateway verification is fixed at INR 1.00."})
        if not name or not email or len(email) > 120 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            return send_json(self, 400, {"error": "Enter your name and a valid email address."})

        key_id = os.environ.get("RAZORPAY_KEY_ID", "").strip()
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "").strip()
        if (not key_id.startswith("rzp_test_") or not key_secret
                or key_secret.startswith("REPLACE_WITH_")):
            return send_json(self, 503, {"error": "Test Razorpay credentials are not configured. Add a newly rotated test Key ID and Secret in Vercel."})

        receipt = reference[:30] + "-" + secrets.token_hex(4)
        order_payload = {
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "notes": {
                "iyonex_reference": reference,
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

        # Short-lived proof that this exact order was created by this backend.
        token_payload = {
            "order_id": order["id"],
            "amount": amount,
            "currency": "INR",
            "receipt": receipt,
            "reference": reference,
            "iat": int(time.time())
        }
        encoded_token_payload = base64.urlsafe_b64encode(
            json.dumps(token_payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
        ).decode("ascii").rstrip("=")
        token_signature = hmac.new(
            key_secret.encode("utf-8"),
            encoded_token_payload.encode("ascii"),
            hashlib.sha256
        ).hexdigest()
        order_token = encoded_token_payload + "." + token_signature

        return send_json(self, 201, {
            "order_id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key_id": key_id,
            "order_token": order_token
        })

    def do_GET(self):
        return send_json(self, 405, {"error": "Method not allowed."})

    def log_message(self, format, *args):
        # Avoid writing customer information or payment payloads to function logs.
        return
