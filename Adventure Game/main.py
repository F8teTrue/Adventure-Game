from player import Player
from game_data import areas, shops, combat_quests, story_quests
from location import Location, Home, Village, QuestHall, Exploration
from formatter import Formatter
from choice import pause_clear_screen
from items import all_items

class Game:
    """
    Main game class that creates the player, manages locations, and handles the game loop.

    Responsibilities:
    - Initialize the player with a name.
    - Set up and link locations such as Home, Village, Quest Hall, and Exploration.
    - Run the main game loop, allowing the player to interact with the game world.
    """
    def __init__(self):
        """
        Initialize the game by setting up the player and locations.
        """
        while True:
            print(Formatter.cyan_bold("Welcome to the Adventure Game"))
            print(Formatter.cyan_bold("As an adventurer you're tasked with accepting quests and exploring areas.\nBut most important of all is to make sure you survive!"))
            player_name = input(Formatter.blue("\nWhat is your name adventurer: "))

            if len(player_name) > 15:
                print(Formatter.yellow_bold("\nThat name is too long."))
                pause_clear_screen(3)
                continue
            elif len(player_name) == 0:
                print(Formatter.yellow_bold("\nPlease enter a name."))
                pause_clear_screen(3)
                continue
            else:
                break
        
        # Create the player
        self.player = Player(player_name)

        # Set up locations
        self.location = {
            "home": Home(self.player),
            "village": Village(self.player, shops["Adventurer's Shop"]),
            "exploration": Exploration(self.player, areas),
        }
        self.location["quest_hall"] = QuestHall(self.player, combat_quests, story_quests, self.location)

        # Start the player at home
        self.current_location = self.location["home"]
    
    def main_loop(self):
        """
        Main game loop to navigate locations and manage player actions.
        
        Runs until the player dies or exits the game.
        """
        while self.player.health > 0:
            print(Formatter.location_name(self.current_location.name)) # Display current location
            action = self.current_location.get_action() # Get player action
            new_location = action.execute(self.location) # Execute action and check for location change

            if isinstance(new_location, Location): # Update current location if needed
                self.current_location = new_location          


if __name__ == "__main__":
    # Start the game
    game = Game()
    game.main_loop()