import imaplib
# import base64
# import os
import email
import dotenv


def login(user, password, email_host, email_port):
    mailbox = imaplib.IMAP4_SSL(email_host, email_port)
    mailbox.login(user, password)
    return mailbox


def getMailboxContent(mailbox, charset=None, filter='ALL'):
    _, data = mailbox.search(charset, filter)
    mail_ids = data[0]
    return mail_ids


def getMessageBody(message, sender_name):
    body_candidates = []
    attachments = []
    attached_files = []

    # Get all the MIME types that are text
    for part in message.walk():
        # Get rid of wrappers:
        if part.get_content_maintype() == 'text':
            body_candidates.append(
                (part, part.get_content_type())
            )
        if part.get('Content-Disposition') is not None:
            attachments.append(
                (part.get_filename(), part.get_payload(decode=True))
            )

    if len(body_candidates) < 1:
        return None

    body = body_candidates[0][0].get_payload(decode=True).decode('utf-8')

    for i in attachments:
        file_name = f'ORDER_{sender_name}_{attachments.index(i)}'
        file_extension = i[0].split('.')[-1]
        file_path = file_name + '.' + file_extension
        with open(file_path, 'wb') as file:
            file.write(i[1])
        attached_files.append(file_name)

    return body, attached_files


def parseEmail(message):
    """Each part is also of type email.message.Message
    """
    # Get Sender name and Email:
    sender_name, sender_email = email.utils.parseaddr(
        message.get('From')
    )
    print('{}From: {}{}'.format(
        ' ' * 8,
        ' ' * (12 - len('From')),
        sender_email)
    )

    # Get Subject
    subject = message.get('Subject')
    print('{}Subject: {}{}'.format(
        ' ' * 8,
        ' ' * (12 - len('Subject')),
        subject)
    )

    # Get Date
    date = message.get('Date')
    print('{}Date: {}{}'.format(
        ' ' * 8,
        ' ' * (12 - len('Date')),
        date)
    )

    # Get Body
    body, attachments = getMessageBody(message, sender_name)
    print('{}Body:\n{}'.format(
        ' ' * 8,
        body)
    )

    print('{}Attachments: {}{}'.format(
        ' ' * 8,
        ' ' * (12 - len('Attachments')),
        attachments)
    )


def main():
    config = dotenv.dotenv_values(".env")
    email_user = config['EMAIL']
    email_pass = config['PASSWORD']
    email_host = config['HOST']
    email_port = config['PORT']

    # Login to the Email Address
    mailbox = login(email_user, email_pass, email_host, email_port)

    # Select the mailbox
    mailbox.select('Inbox')

    # Extract all incomming mail
    mail_ids = getMailboxContent(mailbox)
    id_list = mail_ids.split()  # [b'0', b'1', ..., b'n']

    for mail in id_list:
        if mail.decode('utf-8') != '6':
            continue
        # Get Raw Email as bytes
        # RFC822 is an Internet Message Access Protocol
        _, data = mailbox.fetch(mail, '(RFC822)')
        print(f'EMAIL: {id_list.index(mail)}')
        print('-------------------------------')
        raw_email = data[0][1]

        # Decode Email ==> message object
        message = email.message_from_bytes(raw_email)

        # Get Subject
        parseEmail(message)


if __name__ == '__main__':
    main()
