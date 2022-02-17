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


def filterHTMLText(body_list):
    for i in body_list:
        if 'text/html' in i:
            return i

    return None


def getMessageBody(message):
    body_candidates = []

    # Get all the MIME types that are text
    for part in message.walk():
        # Get rid of wrappers:
        if part.get_content_maintype() == 'text':
            body_candidates.append(
                (part, part.get_content_type())
            )

    if len(body_candidates) < 1:
        return None

    return body_candidates[0][0].get_payload(decode=True).decode('utf-8')

    # html = filterHTMLText(body_candidates)
    # if html:
    #     return html[0].get_payload(decode=True).decode('utf-8')
    # else:
    #     return body_candidates[0][0].get_payload(decode=True).decode('utf-8')


def getMessageAttachement(message):
    return None


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
    body = getMessageBody(message)
    print('{}Body:\n{}'.format(
        ' ' * 8,
        body)
    )

    # Get Attachement
    attachements = getMessageAttachement(message)
    print(attachements)


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
    id_list = mail_ids.split()

    for mail in id_list:
        if mail.decode('utf-8') != '6':
            continue
        # RFC822 is an Internet Message Access Protocol
        # Get Raw Email as bytes
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
