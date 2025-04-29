from modules.views.client_ui import ClientUI

"""
Program entry point (starts the ChatClient). The Chat Client must be started after the Chat Server.
IP Address and Port must be the same as the of the Socket Server.
"""
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5555
    client = ClientUI(ip, port)
