import os

REQUESTS_TIMEOUT = 5
REQUESTS_TIMEOUT_RAW = os.environ.get("BUGOUT_TIMEOUT_SECONDS")
try:
    if REQUESTS_TIMEOUT_RAW is not None:
        REQUESTS_TIMEOUT = int(REQUESTS_TIMEOUT_RAW)
except:
    raise Exception(
        f"Could not parse BUGOUT_REQUESTS_TIMEOUT environment variable as int: {REQUESTS_TIMEOUT_RAW}"
    )
