from core import history,api,conversation

def init():
    history.choose()


def main():
    init()
    max_turns = 16
    global profile_name, api_key
    # history = load_memory(history, profile_name, api_key)
    while True:
        conversation.handle(max_turns)


main()