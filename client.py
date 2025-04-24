from modules.views.client_ui import ClientUI

# TODO: DocStrings are missing!

ip = "127.0.0.1"
port = 5555


"""
Program entry point (starts the ChatClient).
"""
if __name__ == "__main__":
    client = ClientUI(ip, port)
