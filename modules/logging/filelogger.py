import os, sys
from datetime import datetime


class FileLogger:
    logfile = f"{sys.path[0]}\\chat_project.log"

    def __init__(self):
        self.__now = datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')

    def error(self, text: str, /):
        self.writelog("ERROR", text)

    def warning(self, text: str, /):
        self.writelog("WARNING", text)

    def debug(self, text: str, /):
        self.writelog("DEBUG", text)

    def info(self, text: str, /):

        self.writelog("INFO", text)

    def writelog(self, level: str, text: str, /):
        self.roll()
        with open(FileLogger.logfile, "a", encoding="UTF-8") as file:
            file.write(f"{self.__now}> {level}: {text}")

    @staticmethod
    def roll():
        file_size = os.path.getsize(FileLogger.logfile)
        if file_size > 5120:
            os.remove(FileLogger.logfile)
