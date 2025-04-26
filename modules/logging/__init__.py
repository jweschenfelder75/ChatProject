import sys

sys.path.append(sys.path[0] + "\\modules\\logging")
# PyCharm fix: https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from modules.logging.filelogger import *   # noqa: E402
