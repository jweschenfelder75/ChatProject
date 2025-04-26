from modules.chat_server import ChatServer

# TODO: DocStrings are missing!


"""
Program entry point (starts the ChatServer).
"""
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5555
    server = ChatServer(ip, port)
