from typing import Any


class UnknownDemoFormat(Exception):
    def __init__(self, demo_protocol, net_protocol, mod_name):
        super().__init__(f'Unknown demo format ({demo_protocol}, {net_protocol}, {mod_name})')


class ExpectedBetweenGotException(Exception):
    expected_lower_included: Any
    expected_upper_excluded: Any
    got: Any

    def __init__(self, expected_lower_included: Any, expected_upper_excluded: Any, got: Any):
        super().__init__(f'Expected [{expected_lower_included}; {expected_upper_excluded}), got {got}')

        self.expected_lower_included = expected_lower_included
        self.expected_upper_excluded = expected_upper_excluded
        self.got = got


class InvalidNetMsgLength(ExpectedBetweenGotException):
    pass


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
