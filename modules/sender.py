"""EMAIL SENDER OBJECT

Class allowing to easily access the data relative to a sender.

Last update: Feb 18, 2022
"""
import email


class Sender:
    def __init__(self, raw_sender):
        self.raw_sender = raw_sender
        self.name, self.address = email.utils.parseaddr(
            self.raw_sender
        )
