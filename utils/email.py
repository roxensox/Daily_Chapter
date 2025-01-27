import os.path
import base64
import json
import quickstart as qs
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from email.message import EmailMessage
from testing import error_report


def get_user_email(session: object) -> str:
    '''
    Gets the email address of the current authorized user

    Args:
        session: the service object allowing access to the gmail api

    Returns:
        A string containing the authorized user's email address (obfuscating for personal security)
    '''
    return session.users().getProfile(userId="me").execute()["emailAddress"]


def get_contacts() -> list:
    '''
    Retrieves a list of contacts from a text file stored outside of the project directory

    Args:
        None

    Returns:
        A list of email addresses
    '''
    contacts = []
    with open("../../Contacts/contacts.txt", "r") as source:
        contacts = [line.strip() for line in source]
    return contacts


def create_email(body: str, subject: str, recipients: list, sender: str) -> int:
    '''
    Creates and sends an email message with html content

    Args:
        body: a string of html to be added to the body of the email
        subject: a string containing the subject of the email
        recipients: a list of email addresses to send the email to
        sender: the email address of the sending account

    Returns:
        0 if successful, 1 on error
    '''
    email = EmailMessage()
    email.set_content(body, subtype="html")
    email["To"] = recipients
    email["From"] = sender
    email["Subject"] = subject

    encoded_msg = base64.urlsafe_b64encode(email.as_bytes()).decode()
    create_msg = {"raw": encoded_msg}

    try:
        session.users().messages().send(userId="me", body=create_msg).execute()
        return 0

    except HttpError as error:
        print(f"Error: {error}")
        return HttpError


def get_html() -> str:
    '''
    Gets html from an html file in string format

    Args:
        None

    Returns:
        A string of html content
    '''
    with open("../resources/mailpage.html", "r") as html_src:
        body = "".join([i for i in html_src])
    return body


if __name__ == "__main__":
    session = qs.get_session()
    email_address = get_user_email(session)
    contacts = get_contacts()
    text = get_html()
    create_email(body=text, subject="testing", recipients=contacts, sender=email_address)
