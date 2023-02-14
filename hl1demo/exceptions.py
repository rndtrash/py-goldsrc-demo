from typing import Any


class ExpectedGotException(Exception):
    expected: Any
    got: Any

    def __init__(self, expected: Any, got: Any):
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
