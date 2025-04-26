import sys

sys.path.append(f"{sys.path[0]}\\modules\\views")
# PyCharm fix: https://stackoverflow.com/questions/36827962/pep8-import-not-at-top-of-file-with-sys-path
from modules.views.server_ui import *   # noqa: E402
from modules.views.client_ui import *   # noqa: E402
