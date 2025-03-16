import os, time, sys, threading
from formatter import Formatter


class Choice:
    """
    A class represeting a choice the player can make in a location.

    Parameters:
        description (str): The description of the choice.
        action (callable): The action to execute when the choice is selected.
        clear_method (callable): The method to clear the screen after the choice is executed.
    """
    def __init__(self, description: str, action, clear_method = None):
        self.description = description
        self.action = action
        self.clear_method = clear_method

    def execute(self, locations: dict = None):
        """
        Executes the action and ensures a valid location name is returned.

        Parameters:
            locations (dict): Dictionary of available locations.

        Returns:
            str: The name of the new location if applicable.
        """
        if self.clear_method:
            self.clear_method()

        result = self.action()

        if isinstance(result, str) and locations:
            if result in locations:
                return result
            print(f"Invalid location specified: {result}")

        return result

    

def clear_screen():
    """
    Clear the console screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def continue_clear_screen():
    """
    Pause the program and clear the console screen when the player wants to continue.
    """
    input(Formatter.blue("\nPress Enter to continue..."))
    clear_screen()

def pause_clear_screen(pause_time : int = 5):
    """
    Pause the program and clear the console screen after a set amount of time or the player presses Enter.

    Parameters:
        pause_time (int): The amount of time to pause before clearing the screen.
    """
    skip = threading.Event()

    def wait_for_enter():
        """
        Waits for the player to press Enter to skip the pause.
        """
        try:
            if os.name == 'nt':  # Windows systems

                import msvcrt
                while not skip.is_set():
                    if msvcrt.kbhit():
                        if msvcrt.getch() == b'\r':  # Enter key
                            skip.set()
                            break
            else:  # Unix-based systems
                import select
                while not skip.is_set():
                    if select.select([sys.stdin], [], [], 0.1)[0]:
                        skip.set()
                        sys.stdin.readline()
                        break
        except Exception as e:
            pass

    # Start a background thread to listen for Enter key
    input_thread = threading.Thread(target=wait_for_enter, daemon=True)
    input_thread.start()

    # Countdown timer for the pause
    print(Formatter.blue("\nPress Enter to skip..."))
    for remaining_time in range(pause_time, 0, -1):
        if skip.is_set():
            break
        print(f"\r{Formatter.yellow_stat('Continuing in', remaining_time)} seconds... ", end="", flush=True,)
        time.sleep(1)

    # Signal the thread to stop and clean up
    skip.set()
    input_thread.join(timeout=0)

    clear_screen()