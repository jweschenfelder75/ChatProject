import os
import sys
from datetime import datetime


class FileLogger:
    __logfile = f"{sys.path[0]}\\chat_project.log"

    def __init__(self, component: str, /):
        self.__component = component

    def error(self, text: str, /):
        self.__writelog("ERROR", text)

    def warning(self, text: str, /):
        self.__writelog("WARN", text)

    def debug(self, text: str, /):
        self.__writelog("DEBUG", text)

    def info(self, text: str, /):
        self.__writelog("INFO", text)

    def __writelog(self, level: str, text: str, /):
        self.__roll()
        self.__now = datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        with open(FileLogger.__logfile, "a", encoding="UTF-8") as file:
            file.write(f"{self.__now}> {level:<5} - {self.__component}: {text}\n")

    @staticmethod
    def __roll():
        if os.path.isfile(FileLogger.__logfile):
            file_size = os.path.getsize(FileLogger.__logfile)
            if file_size > 5120:
                os.remove(FileLogger.__logfile)
