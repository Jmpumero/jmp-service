class NotFoundException(Exception):
    def __init__(self, message="Not Found") -> None:
        self.message = message
        self.status_code = 404