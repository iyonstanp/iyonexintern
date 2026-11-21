import base64
import hashlib
import hmac
import json
import os
import re
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

        order_id = payload.get("razorpay_order_id")
        payment_id = payload.get("razorpay_payment_id")
        signature = payload.get("razorpay_signature")

        if not all(isinstance(value, str) and value for value in (order_id, payment_id, signature)):
            return send_json(self, 400, {"error": "Missing Razorpay order, payment or signature fields."})
        if not re.fullmatch(r"order_[A-Za-z0-9]+", order_id) or not re.fullmatch(r"pay_[A-Za-z0-9]+", payment_id) or not re.fullmatch(r"[A-Fa-f0-9]{64}", signature):
            return send_json(self, 400, {"error": "Invalid Razorpay payment fields."})

        key_id = os.environ.get("RAZORPAY_KEY_ID", "").strip()
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "").strip()
        if not key_id or not key_secret or key_secret.startswith("REPLACE_WITH_"):
            return send_json(self, 503, {"error": "Online payments are not configured yet."})

        message = (order_id + "|" + payment_id).encode("utf-8")
        expected = hmac.new(key_secret.encode("utf-8"), message, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, signature.lower()):
            return send_json(self, 400, {"error": "Payment signature verification failed."})

        # Confirm the payment belongs to this order and check its capture state.
        auth = base64.b64encode((key_id + ":" + key_secret).encode("utf-8")).decode("ascii")
        request = urllib.request.Request(
            "https://api.razorpay.com/v1/payments/" + payment_id,
            headers={"Authorization": "Basic " + auth},
            method="GET"
        )
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                payment = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            status = 401 if exc.code == 401 else 502
            return send_json(self, status, {"error": "Could not confirm payment status with Razorpay."})
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return send_json(self, 502, {"error": "Could not confirm payment status. Please contact IYONEX before retrying."})

        if payment.get("id") != payment_id or payment.get("order_id") != order_id:
            return send_json(self, 400, {"error": "The payment does not match the supplied Razorpay order."})

        order_request = urllib.request.Request(
            "https://api.razorpay.com/v1/orders/" + order_id,
            headers={"Authorization": "Basic " + auth},
            method="GET"
        )
        try:
            with urllib.request.urlopen(order_request, timeout=15) as response:
                order = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError:
            return send_json(self, 502, {"error": "Could not confirm the original order with Razorpay."})
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return send_json(self, 502, {"error": "Could not confirm the original order. Please contact IYONEX."})

        if (order.get("id") != order_id or order.get("currency") != "INR"
                or payment.get("currency") != "INR"
                or order.get("amount") != payment.get("amount")):
            return send_json(self, 400, {"error": "The payment amount or currency does not match the original order."})

        if payment.get("status") != "captured":
            return send_json(self, 202, {
                "verified": True,
                "paid": False,
                "payment_status": payment.get("status", "unknown"),
                "message": "The payment signature is valid, but Razorpay has not marked the payment as captured yet."
            })

        return send_json(self, 200, {
            "verified": True,
            "paid": True,
            "payment_id": payment_id,
            "order_id": order_id,
            "amount": payment.get("amount"),
            "currency": payment.get("currency")
        })

    def do_GET(self):
        return send_json(self, 405, {"error": "Method not allowed."})

    def log_message(self, format, *args):
        return
