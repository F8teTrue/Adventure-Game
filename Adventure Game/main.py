from player import Player
from game_data import areas, shops, combat_quests, story_quests
from location import Home, Village, QuestHall, Exploration
from game_display import GameDisplay
from ui.ui_manager import UIManager
from items import all_items

class Game:
    """
    Main game class that initializes the player, locations, and launches the game UI.
    """
    def __init__(self):
        """
        Initializes the game immediately with a default player name.
        """
        # Initialize the game display and UI manager
        self.game_display = GameDisplay()
        self.ui_manager = UIManager(self.game_display.screen)

        # Create the player
        self.player = Player("Adventurer")
        self.player.add_to_inventory(all_items["basic_sword"])
        self.player.add_to_inventory(all_items["basic_sword"])
        self.player.add_to_inventory(all_items["great_sword"])
        self.player.add_to_inventory(all_items["leather_armour"])
        self.player.add_to_inventory(all_items["leather_armour"])
        self.player.add_to_inventory(all_items["plate_armour"])
        self.player.add_to_inventory(all_items["small_healing_potion"])
        self.player.add_to_inventory(all_items["small_strength_potion"])
        self.player.add_to_inventory(all_items["small_strength_potion"])
        self.player.add_to_inventory(all_items["large_healing_potion"])
        self.player.add_to_inventory(all_items["large_strength_potion"])
        self.player.add_to_inventory(all_items["wizard's_medallion"])
        # Set up locations
        self.locations = {
            "home": Home(self.player, self.ui_manager),
            "village": Village(self.player, shops["Adventurer's Shop"]),
            "exploration": Exploration(self.player, areas),
        }
        self.locations["quest_hall"] = QuestHall(self.player, combat_quests, story_quests, self.locations)

        # Initialize the game
        self.game_display.initialize_game(self.player, self.locations)

if __name__ == "__main__":
    Game()  # Start the game