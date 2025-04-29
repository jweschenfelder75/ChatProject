"""
Some small CLI UI for the Socket Server.
"""


class ServerUI:
    def __init__(self):
        """
        Constructor of the class ServerUI.
        """
        self.__str = "\n"
        self.__str += "  //  \n"
        self.__str += " ('>  \n"
        self.__str += " /rr  \n"
        self.__str += "*\\))_ \n"

    def __str__(self):
        """
        Returns the string defined in self.__str which represents an Easter bunny.
        It is the logo of the Socket Server. ;-)

        Returns:
            str: Easter bunny as ASCII art
        """
        return self.__str
