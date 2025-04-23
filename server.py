from modules.chat_server import ChatServer

# TODO: DocStrings are missing!


port = 5555

"""
Program entry point (starts the ChatServer).
"""
if __name__ == "__main__":
    server = ChatServer(5555)
    server.connect()
