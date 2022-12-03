import os

# from decouple import config as dconfig


# # Config settings from environment variables.
# # These are treated as secrets and therefore sourced from environment variables to follow best practices.
# GOOGLE_CREDS_PATH = dconfig("GOOGLE_CREDS_PATH")
# CLIENT_EMAIL = dconfig("CLIENT_EMAIL")

GSPREADER_GOOGLE_CREDS_PATH = os.environ["GSPREADER_GOOGLE_CREDS_PATH"]
GSPREADER_GOOGLE_CLIENT_EMAIL = os.environ["GSPREADER_GOOGLE_CLIENT_EMAIL"]
