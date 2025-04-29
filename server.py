from modules.chat_server import ChatServer

"""
Program entry point (starts the ChatServer). The Chat Server must be started before the Chat Client.
"""
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5555
    server = ChatServer(ip, port)
