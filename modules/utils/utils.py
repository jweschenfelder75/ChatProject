class Utils:
    __length_header_size = 8
    __user_header_size = 16

    @staticmethod
    def get_length_header_size() -> int:
        return Utils.__length_header_size

    @staticmethod
    def get_user_header_size() -> int:
        return Utils.__user_header_size

    def format_message(self, username: str, message: str, /):
        if not message:
            return None
        length_header = f"{len(message):<{self.get_length_header_size()}}"
        user_header = f"{username:<{self.get_user_header_size()}}"
        return f"{length_header}{user_header}{message}"
