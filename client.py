from modules.chat_client import ChatClient

# TODO: DocStrings are missing!


port = 5555


"""
Program entry point (starts the ChatClient).
"""
if __name__ == "__main__":
    client = ChatClient(5555)
    client.connect()
