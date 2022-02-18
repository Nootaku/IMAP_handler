"""EMAIL MESSAGE OBJECT

Class allowing to easily access the headers, body (text) and attachments of an
email.

Last update: Feb 18, 2022
"""
import email
from modules.sender import Sender
from modules.attachment import Attachment


class Email:
    def __init__(self, raw_email):
        self.full_email = email.message_from_bytes(raw_email)
        self.sender = Sender(self.full_email.get('From'))
        self.subject = self.full_email.get('Subject')
        self.date = self.full_email.get('Date')
        self.cdn = 'cdn'

    @property
    def body(self):
        body_candidates = []

        # Get all the MIME types that are text
        for part in self.full_email.walk():
            # Get rid of wrappers:
            if part.get_content_maintype() == 'text':
                body_candidates.append(
                    (part, part.get_content_type())
                )

        if len(body_candidates) < 1:
            return None

        body = body_candidates[0][0].get_payload(decode=True).decode('utf-8')

        return body

    @property
    def attachements(self):
        attachments = []

        # Get all the MIME types that are text
        for part in self.full_email.walk():
            if part.get('Content-Disposition') is not None:
                attachments.append(
                    Attachment(
                        file_name=part.get_filename(),
                        file_content=part.get_payload(decode=True))
                )

        return attachments

    def downloadAttachments(self):
        for i in self.attachements:
            file_path = self.cdn + '/ORDER_'
            file_path += self.sender.name + '_' + self.subject
            file_path += f'.{i.file_format}'
            # date = self.date

            i.save_to(file_path)
