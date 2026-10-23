import requests
from functools import wraps
from flask import request, current_app
from video_app.enums import VALIDATE_TOKEN_URL
from video_app.utils import logged_error
from video_app.api.helper import send_error


def authorization_require():
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            authorization = request.headers.get("Authorization")
            
            # DEBUG: Log what we received
            current_app.logger.info(f"Received Authorization header: '{authorization}'")

            if not authorization:
                current_app.logger.error("No Authorization header found in request")
                return send_error(403, "You don't have permission")

            try:
                # DEBUG: Log what we're sending
                current_app.logger.info(f"Sending to auth service: {VALIDATE_TOKEN_URL} with header: {authorization[:20]}...")
                
                res = requests.get(
                    VALIDATE_TOKEN_URL,
                    headers={"Authorization": authorization},
                    timeout=5
                )
                current_app.logger.info(f"Auth service response: {res.status_code} {res.text[:200]}")
                res.raise_for_status()
                data = res.json()

                
                if data.get("code") != 200 or data.get("message", {}).get("text") != "Token valid":
                    return send_error(403, data.get("message", {}).get("text", "Invalid token"))

            except requests.exceptions.ConnectionError as e:
                current_app.logger.error(f"Cannot reach auth service at {VALIDATE_TOKEN_URL}: {e}")
                return send_error(503, "Authentication service unreachable")

            except requests.exceptions.Timeout:
                current_app.logger.error(f"Timeout calling auth service at {VALIDATE_TOKEN_URL}")
                return send_error(503, "Authentication service timed out")

            except requests.exceptions.HTTPError as e:
                current_app.logger.warning(f"Auth service rejected token: {e}")
                return send_error(403, "You don't have permission")

            except ValueError as e:
                current_app.logger.error(f"Invalid JSON from auth service: {e}")
                return send_error(503, "Authentication service returned invalid response")

            return fn(*args, **kwargs)

        return decorated_function
    return wrapper