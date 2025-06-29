from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
import sys

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CREDS_FILE = r"path/to/yourcerdentials.json"  # Full absolute path


def main():
    creds = None

    # If token.json exists, try to use it
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if creds and creds.valid:
            print("Existing 'token.json' is valid; no need to re-auth.")
            return
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                print("Token refreshed!")
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
                return
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Proceeding to run the OAuth flow for a new token...")

    # Debug: Print current working directory and files
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    try:
        files = os.listdir(cwd)
        print(f"Files in working directory: {files}")
    except Exception as e:
        print(f"Error listing directory contents: {e}")

    # Check if credentials file exists
    print(f"Checking for file: '{CREDS_FILE}'")
    if not os.path.exists(CREDS_FILE):
        print(f"Error: OAuth credentials file not found at:\n{CREDS_FILE}")
        sys.exit(1)
    else:
        print(f"Success: Found credentials file at {os.path.abspath(CREDS_FILE)}")

    try:
        print("Attempting to load credentials via OAuth flow...")
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=8080, prompt="consent")
    except Exception as e:
        print(f"Error during OAuth flow: {e}")
        sys.exit(1)

    try:
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        print("All done! 'token.json' created/updated successfully.")
    except Exception as e:
        print(f"Error writing token.json: {e}")


if __name__ == "__main__":
    main()
