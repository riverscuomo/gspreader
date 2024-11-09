import os
from dotenv import load_dotenv

load_dotenv()

GSPREADER_GOOGLE_CREDS = os.environ.get("GSPREADER_GOOGLE_CREDS", None)
GSPREADER_GOOGLE_CREDS_PATH = os.environ.get(
    "GSPREADER_GOOGLE_CREDS_PATH", None
)
GSPREADER_GOOGLE_CLIENT_EMAIL = os.environ["GSPREADER_GOOGLE_CLIENT_EMAIL"]
