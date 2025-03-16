import sys, time, threading, keyboard

# Function for printing strings slowly to create a more realistic dialogue effect
def print_slow(text):
    """
    Writes a string with a slight delay between each character to simulate typing.
    Adds longer pauses for punctuation marks like ".", "?", "!", and ",", and handles ellipses ("...") as a single pause.
    Allows the user to skip the wait by pressing the Space key.
    """
    skip = threading.Event()

    def wait_for_enter():
        """
        Wait for the Space key to be pressed to skip the slow print effect.
        """
        keyboard.wait("space")
        skip.set()

    # Start the listener thread
    listener = threading.Thread(target=wait_for_enter, daemon=True)
    listener.start()

    i = 0
    while i < len(text):
        if skip.is_set():  # Check if the skip event is triggered
            sys.stdout.write(text[i:])
            sys.stdout.flush()
            break

        if text[i:i+3] == "...":
            sys.stdout.write("...")
            sys.stdout.flush()
            time.sleep(1)
            i += 3
        elif text[i] in [".", "?", "!"]:
            sys.stdout.write(text[i])
            sys.stdout.flush()
            time.sleep(0.4)
            i += 1
        elif text[i] == ",":
            sys.stdout.write(text[i])
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
        else:
            sys.stdout.write(text[i])
            sys.stdout.flush()
            time.sleep(0.05)
            i += 1

    print()