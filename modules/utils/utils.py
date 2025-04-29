"""
Utility class with several methods.
"""


class Utils:
    __LENGTH_HEADER_SIZE = 8
    __USER_HEADER_SIZE = 16

    @staticmethod
    def get_length_header_size() -> int:
        """
        Returns the predefined __LENGTH_HEADER_SIZE constant (max. length of meta information).

        Returns:
            __LENGTH_HEADER_SIZE constant
        """
        return Utils.__LENGTH_HEADER_SIZE

    @staticmethod
    def get_user_header_size() -> int:
        """
        Returns the predefined __USER_HEADER_SIZE constant (max. length of meta information).

        Returns:
            predefined __USER_HEADER_SIZE
        """
        return Utils.__USER_HEADER_SIZE

    def format_message(self, username: str, message: str, /) -> str | None:
        """
        Formats a message and adds some meta information such as header and user header.

        Args:
            username (str): Username
            message (str): Text message

        Returns:
            str | None:
        """
        if not message:
            return None
        length_header = f"{len(message):<{self.get_length_header_size()}}"
        user_header = f"{username:<{self.get_user_header_size()}}"
        return f"{length_header}{user_header}{message}"
