import os.path
from globals import PATH

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    service = get_session()
    try:
        # Call the Gmail API
        results = service.users().labels().list(userId="me").execute()
        labels = results.get("labels", [])
        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])

    except HttpError as error:
        #TODO: - Handle errors from gmail API.
        print(f"An error occurred: {error}")


def get_session():
    creds = None
    flow = InstalledAppFlow.from_client_secrets_file(
        os.path.join(PATH, "../secure/credentials.json"), SCOPES
    )
    if os.path.exists(os.path.join(PATH, "../secure/token.json")):
        creds = Credentials.from_authorized_user_file(
            os.path.join(PATH, "../secure/token.json"), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(PATH, "../secure/credentials.json"), SCOPES
            )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open(os.path.join(PATH, "../secure/token.json"), "w") as token:
        token.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    return service


if __name__ == "__main__":
    main()
