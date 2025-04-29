import os
import sys
from datetime import datetime

"""
Logger which writes a log file.
"""


class FileLogger:
    __logfile = f"{sys.path[0]}\\chat_project.log"

    def __init__(self, component: str, /):
        """
        Constructor of the class FileLogger.

        Args:
            component (str): Some component/class (identifier) which has called the Logger,
                             it will be written in the Log.
        """
        self.__component = component

    def error(self, text: str, /):
        """
        Writes the given text with ERROR-Log-Level in a Log file.

        Args:
            text (str): Text which shall be written in the log file.
        """
        self.__writelog("ERROR", text)

    def warning(self, text: str, /):
        """
        Writes the given text with WARN-Log-Level in a Log file.

        Args:
            text (str): Text which shall be written in the log file.
        """
        self.__writelog("WARN", text)

    def debug(self, text: str, /):
        """
        Writes the given text with DEBUG-Log-Level in a Log file.

        Args:
            text (str): Text which shall be written in the log file.
        """
        self.__writelog("DEBUG", text)

    def info(self, text: str, /):
        """
        Writes the given text with INFO-Log-Level in a Log file.

        Args:
            text (str): Text which shall be written in the log file
        """
        self.__writelog("INFO", text)

    def __writelog(self, level: str, text: str, /):
        """
        Writes the given Log-Level and the text in a log file.
        Replaces the Logfile by a new log file when it is > 5 MB.

        Args:
            level (str): Log-Level which shall be written in the log file
            text (str): Text which shall be written in the log file
        """
        self.__roll()
        self.__now = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        with open(FileLogger.__logfile, "a", encoding="UTF-8") as file:
            file.write(f"{self.__now}> {level:<5} - {self.__component}: {text}\n")

    @staticmethod
    def __roll():
        """
        Replaces the Logfile by a new log file when it is > 5 MB.
        Attention: The old logfile will not be archived.
        """
        if os.path.isfile(FileLogger.__logfile):
            file_size = os.path.getsize(FileLogger.__logfile)
            if file_size > (5 * 1024 * 1024):
                os.remove(FileLogger.__logfile)
