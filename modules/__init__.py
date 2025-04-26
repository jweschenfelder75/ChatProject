import sys

sys.path.append(f"{sys.path[0]}\\modules")
# PyCharm fix: https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from modules.chat_server import *   # noqa: E402
from modules.chat_client import *   # noqa: E402
