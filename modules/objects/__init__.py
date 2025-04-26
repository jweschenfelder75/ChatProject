import sys

sys.path.append(sys.path[0] + "\\modules\\objects")
# PyCharm fix: https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from modules.objects.result import *   # noqa: E402
from modules.objects.message import *   # noqa: E402
from modules.objects.client import *   # noqa: E402
from modules.objects.clientpool import *   # noqa: E402
