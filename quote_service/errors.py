
class UnsupportedActionError(Exception):
    pass


class UnsupportedAmountError(Exception):
    def __init__(self, max_amount):
        self.max_amount = max_amount
