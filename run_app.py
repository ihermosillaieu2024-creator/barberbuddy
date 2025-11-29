from src.barberbot import DB, handle

def main():
    print("Welcome to BarberBuddy! Type QUIT to exit.")
    print("Type SWITCH at any time to restart.")
    print("Are you a client or a barber? (Type: client / barber )")

    while True:
        user_msg = input("You: ")
        if user_msg.strip().upper() == "QUIT":
            print("Goodbye!")
            break

        reply = handle(DB, user_msg)
        print("Bot:", reply)

if __name__ == "__main__":
    main()