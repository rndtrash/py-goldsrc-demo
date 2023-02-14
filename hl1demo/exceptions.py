class ExpectedGotException(Exception):
    def __init__(self, expected, got):
        super().__init__(f'Expected {expected}, got {got}')

        self.expected = expected
        self.got = got


class InvalidMagicException(ExpectedGotException):
    pass


class InvalidDemoProtocolException(ExpectedGotException):
    pass


class InvalidNetProtocolException(ExpectedGotException):
    pass


class InvalidModException(ExpectedGotException):
    pass
