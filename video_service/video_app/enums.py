import os

# coding: utf-8
TIME_FORMAT_LOG = "[%Y-%b-%d %H:%M]"
VALIDATE_TOKEN_URL = os.getenv(
    "VALIDATE_TOKEN_URL",
    "http://localhost:5012/api/v1/auth/tokens/validate"  # local default
)
