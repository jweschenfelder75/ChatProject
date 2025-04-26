from modules.logging import FileLogger


class Utils:
    LENGTH_HEADER_SIZE = 8
    USER_HEADER_SIZE = 16

    def __init__(self):
        self.log = FileLogger(Utils.__class__.__name__)

    def format_message(self, username: str, message: str, /):
        if not message:
            self.log.warning("Not a message.")
            return None
        length_header = f"{len(message):<{Utils.LENGTH_HEADER_SIZE}}"
        user_header = f"{username:<{Utils.USER_HEADER_SIZE}}"
        return f"{length_header}{user_header}{message}"
