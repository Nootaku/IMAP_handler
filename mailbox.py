import imaplib
import email
from message import Email


class Mailbox:
    def __init__(self, address, password, host, port):
        self.address = address
        self.password = password
        self.host = host
        self.port = port

        self.mailbox = imaplib.IMAP4_SSL(self.host, self.port)
        self.emails = []

    def login(self):
        """Login into mailbox.
        """
        self.mailbox.login(self.address, self.password)

    def select_folder(self, folder):
        """Select the mailbox folder that will be accessed.
        """
        self.mailbox.select(folder)

    def getEmailMessages(self, charset=None, filter='ALL'):
        """Really need info here
        """
        # empty self.emails
        self.emails = []

        # return OK, b[1 2 3 ... n]
        _, data = self.mailbox.search(charset, filter)

        # transform data into list [b'0', b'1', b'2', ..., b'n']
        email_ids = data[0].split()

        for email_id in email_ids:
            # get raw email (as bytes)
            _, data = self.mailbox.fetch(email_id, '(RFC822)')
            raw_email = data[0][1]

            # make an Email object
            message = Email(raw_email)

            # append the Email object to self.emails
            self.emails.append(message)
