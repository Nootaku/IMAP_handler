import email


class Sender:
    def __init__(self, raw_sender):
        self.raw_sender = raw_sender
        self.name, self.address = email.utils.parseaddr(
            self.raw_sender
        )
