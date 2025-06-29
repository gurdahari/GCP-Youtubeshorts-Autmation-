# config.py
import os
import datetime

# === GCP / GCS CONFIG ===
PROJECT_ID = "xxxxxxxxxxxx"
GCS_BUCKET_NAME = "xxxxx"

# === SHOPIFY LINK ===
SHOP_URL = "xxxxxxxxx"

# === OPENAI CONFIG ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === YOUTUBE CONFIG ===
# Put your client ID/secret in a separate JSON, then do an OAuth flow to get 'token.json'
YOUTUBE_CREDENTIALS_FILE = "token.json"

# === SYSTEM CONFIG ===
STATE_FILE = "state.json"
VIDEOS_TO_UPLOAD_PER_RUN = 1
PUBLISH_DELAY_HOURS = 24


# === TIME HELPERS ===
def get_publish_time_utc():
    """
    מחזיר זמן פרסום עתידי בפורמט ISO 8601 (UTC) על בסיס הגדרת PUBLISH_DELAY_HOURS.
    """
    dt = datetime.datetime.utcnow() + datetime.timedelta(hours=PUBLISH_DELAY_HOURS)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
