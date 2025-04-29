import sys

sys.path.append(f"{sys.path[0]}\\modules\\logging")
# PyCharm fix: https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from modules.logging.file_logger import *   # noqa: E402
