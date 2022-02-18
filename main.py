"""SAVE EMAILS AND ATTACHEMENTS

Version: 0.0.1
Last update: Feb 18, 2022
"""
import dotenv
from modules.mailbox import Mailbox


def main():
    """Connect to an email address, login and retrieve all emails located in
    the 'Inbox' folder.
    """
    config = dotenv.dotenv_values(".env")
    email_address = config['EMAIL']
    email_psw = config['PASSWORD']
    email_host = config['HOST']
    email_port = config['PORT']

    # Create Mailbox object
    mailbox = Mailbox(email_address, email_psw, email_host, email_port)

    # Login to the Email Address
    mailbox.login()

    # Select the mailbox
    mailbox.select_folder('Inbox')

    # Extract all incomming mail from 'Inbox' folder
    mailbox.getEmailMessages()

    for i in mailbox.emails:
        attach_list = [a.file_name for a in i.attachments]

        print(f'EMAIL: {i.subject}')
        print('-------------------------------')
        print(f"{' ' * 8}From: {i.sender.address}")
        print(f"{' ' * 8}Subject: {i.subject}")
        print(f"{' ' * 8}Date: {i.date}")
        print(f"{' ' * 8}Body:\nSTART---")
        print(i.body)
        print(f"---END\n\n{' ' * 8}Downloading Attachment == > {attach_list}")

        i.downloadAttachments()
        print(f"{' ' * 8}Done\n\n")


if __name__ == '__main__':
    main()
