from modules.chat_server import ChatServer

# TODO: DocStrings are missing!

ip = "127.0.0.1"
port = 5555

"""
Program entry point (starts the ChatServer).
"""
if __name__ == "__main__":
    server = ChatServer(ip, port)
    server.connect()
