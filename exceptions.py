# exceptions.py

class NotFoundException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class DuplicateException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class BadRequestException(Exception):
    def __init__(self, detail: str):
        self.detail = detail