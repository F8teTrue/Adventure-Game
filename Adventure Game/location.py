from choice import Choice, clear_screen, continue_clear_screen, pause_clear_screen
from explore import ExplorationEvent
from quest import CombatQuest, StoryQuest
from npc import NPC
from formatter import Formatter

class Location:
    """
    Base class representing where the player is in the game world.

    Parameters:
        player (Player): The player object in the game.
        name (str): The name of the location.
        description (str): The description of the location.
    
    **Starting Attributes**:
        **choices** (list): 
            A list of choices available to the player in the location.
    """
    def __init__(self, player : object, name : str, description : str):
        self.player = player
        self.name = name
        self.description = description
        self.choices = []

        self.ui_config = {
            "button_width": 400,
            "button_height": 60,
            "button_spacing_x": 40,
            "button_spacing_y": 20,
            "columns": 3
        }

    def get_action(self):
        """
        Display choices and get action from player's input.
        """
        while True:
            print(self.description)
            for index, choice in enumerate(self.choices, 1):
                print(f"{Formatter.blue_bold(index)}. {choice.description}")
            try:
                # Get the player's choice and return the selected action
                selected = int(input(Formatter.blue("Enter the number of your choice: "))) - 1
                return self.choices[selected]      
            except:
                print(Formatter.yellow_bold("Invalid choice. Please try again."))
                pause_clear_screen(2)

class Home(Location):
    """
    The player's home location. The starting location of the game and the main hub.
    """
    def __init__(self, player : object, ui_manager : object):
        super().__init__(player, "Home", Formatter.white_bold("You are in your cozy home."))
        self.ui_manager = ui_manager
        self.choices = [
            Choice("Visit the village", lambda: "village", clear_method=clear_screen),
            Choice("Explore an area", lambda: "exploration", clear_method=clear_screen),
            Choice("Check Status", lambda: self.ui_manager.open_ui(self.status_ui, self.player)),
            Choice("Manage inventory", lambda: self.ui_manager.open_ui(self.inventory_ui, self.player)),
        ]

        self.ui_config.update({
            "button_width": 450,
            "button_height": 60,
            "columns": 2
        })

class Village(Location):
    """
    The village location where the player can visit shops and the quest hall.

    Parameters:
        player (Player): The player object in the game.
        shop (Shop): The shop object for the village.
    """
    def __init__(self, player : object, shop : object, ui_manager : object):
        super().__init__(player, "Village", Formatter.white_bold("The bustling village awaits."))
        self.shop = shop
        self.ui_manager = ui_manager
        self.npc_dict = {}
        self.choices = [
            Choice("Visit the Adventurer's Shop", lambda: self.ui_manager.open_ui(self.shop_ui, self.player)),
            Choice("Go to the Quest Hall", lambda: "quest_hall", clear_method=clear_screen),
            Choice("Return home", lambda: "home", clear_method=clear_screen)
        ]

        self.ui_config.update({
            "button_width": 475,
            "button_height": 60,
            "columns": 3
        })

    def update_npcs(self):
        """
        Update NPCs based on the player's active quest.
        """
        self.npc_dict = {} # Reset the NPC dictionary

        if self.player.active_quest and isinstance(self.player.active_quest, StoryQuest):
            quest = self.player.active_quest
            for step in quest.steps:
                if step["type"] == "interaction":
                    npc_name = step["trigger"].get("npc")
                    if npc_name:
                        self.npc_dict[npc_name] = NPC(
                            npc_name.replace("_", " ").title(),
                            dialogue_steps = [
                                step["dialogue"]
                                for step in quest.steps
                                if step["type"] == "interaction" and step["trigger"].get("npc") == npc_name
                            ],
                            quest_trigger = npc_name
                        )
        self.update_choices()
    
    def update_choices(self):
        """
        Update the choices based on NPC states or quests.
        """
        # Remove existing "Talk to" choices
        self.choices = [choice for choice in self.choices if "Talk to" not in choice.description]

        # Add new NPC interactions
        for npc in self.npc_dict.values():
            if not npc.interacted:
                self.choices.insert(0, Choice(f"Talk to {npc.name}", lambda npc = npc: npc.interact(self.player)))

class QuestHall(Location):
    """
    Quest Hall location where players can view and accept quests.
    
    Parameters:
        player (Player): The player interacting with the Quest Hall.
        combat_quests (dict): Available combat quests.
        story_quests (dict): Available story quests.
        location (dict): Dictionary of locations in the game.
    """
    def __init__(self, player : object, combat_quests : dict, story_quests : dict, location : dict):
        super().__init__(player, "Quest Hall", Formatter.white_bold("Welcome to the Quest Hall!"))
        self.combat_quests = combat_quests
        self.story_quests = story_quests
        self.location = location # Dictionary of all game locations

        self.ui_config.update({
            "button_width": 350,
            "button_height": 50,
            "button_spacing_x": 30,
            "button_spacing_y": 15,
            "columns": 4
        })

        # Link locations to story quests for NPC updates
        for quest in self.story_quests.values():
            if isinstance(quest, StoryQuest):
                quest.locations = self.location
        
        # Unlock the first story quest
        if self.story_quests:
            first_story_quest = next(iter(self.story_quests.values()))
            first_story_quest.locked = False

    def display_quests(self):
        """
        Display categorized quests and the player's current quest.

        Returns:
            quest_mapping (dict): Mapping of quest numbers to quest IDs.
        """
        print(self.description)
        # Display player's current quest
        if self.player.active_quest and isinstance(self.player.active_quest, CombatQuest):
            current_quest = self.player.active_quest
            print(f"\n{Formatter.cyan_bold('Current Quest:')} {current_quest.desc}")
            print(f"{Formatter.cyan_bold('Progress:')} {Formatter.green_bold(self.player.quest_progress)}/{current_quest.target_count}")
        elif self.player.active_quest and isinstance(self.player.active_quest, StoryQuest):
            current_quest = self.player.active_quest
            print(f"\n{Formatter.cyan_bold('Current Quest:')} {current_quest.desc}")
            current_quest.display_current_step()
        else: 
            print(Formatter.white_bold("\nYou have no active quest at the moment."))

        # Display categorized available quests
        print(f"\n{Formatter.cyan_bold('Available Quests:')}")
        quest_index = 1
        quest_mapping = {}

        for category_name, quest_dict in [("Combat", self.combat_quests), ("Story", self.story_quests)]:
            print(f"\n{Formatter.yellow_bold(category_name + ' Quests')}:")
            if quest_dict:
                for quest_id, quest in quest_dict.items():
                    if isinstance(quest, StoryQuest) and quest.locked:
                        continue  # Skip locked story quests
                    print(f"{Formatter.blue(quest_index)}. {quest.desc} - {Formatter.green_bold('Rewards')}: {quest.display_rewards()}")
                    quest_mapping[quest_index] = quest_id
                    quest_index += 1
            else:
                print(Formatter.yellow_bold("No quests available in this category."))

        return quest_mapping

    def get_action(self):
        """
        Displays quests and allows player to accept a quest.
        """
        while True:
            quest_mapping = self.display_quests()
            choice = input(f"\nEnter the number of the {Formatter.cyan_bold('quest')} you want to accept, or '{Formatter.red_bold('back')}' to return: ").lower()
            
            if choice == "back":
                clear_screen()
                return Choice("Return to Village", lambda: "village")
            
            try:
                quest_choice = int(choice)
                if quest_choice not in quest_mapping:
                    raise ValueError

                quest_id = quest_mapping[quest_choice]
                selected_quest = self.combat_quests.get(quest_id) or self.story_quests.get(quest_id)
                
                self.player.active_quest = selected_quest
                self.player.quest_progress = 0
                print(f"\n{Formatter.white_cyan_stat('You have accepted the quest', selected_quest.desc)}")

                # Update NPCs if the selected quest is a StoryQuest
                if isinstance(selected_quest, StoryQuest) and selected_quest.linked_location:
                    linked_location = self.location.get(selected_quest.linked_location)
                    if linked_location:
                        linked_location.update_npcs() 


                continue_clear_screen()

            except (ValueError, IndexError):
                print(Formatter.yellow_bold("Invalid choice. Please select a valid quest number or type 'back'."))
                pause_clear_screen(2)
                continue

            return Choice("Return to Village", lambda: "village")
    

class Exploration(Location):
    """
    Exploration location where the player can choose an area to explore.

    Parameters:
        player (Player): The player object in the game.
        areas (dict): Areas available for exploration.
    """
    def __init__(self, player : object, areas : dict, quest : object = None):
        super().__init__(player, "Exploration", "You venture out to explore an area.")
        self.areas = areas
        self.quest = quest

        self.ui_config.update({
            "button_width": 350,
            "button_height": 50,
            "columns": 3
        })

        # Create choices for each available area
        self.choices = [
            Choice(
                f"Explore {area.name} - (Difficulty: {area.difficulty})",
                lambda area=area: ExplorationEvent(self.player, area).start()
            )
            for area in areas.values() if not area.locked 
        ]
        self.return_choice = Choice("Return home", lambda: "home")
        self.choices.append(self.return_choice)
    
    def display_areas(self):
        """
        Display the available areas for exploration.
        """
        print(f"\n{Formatter.cyan_bold('Available Areas:')}")
        for idx, area in enumerate(self.areas.values(), start=1):
            if not area.locked:
                print(f"{Formatter.blue(idx)}. {Formatter.cyan_bold(area.name)} (Difficulty: {area.difficulty})")
            else:
                print(f"{Formatter.blue(idx)}. {Formatter.red_bold(area.name)} (Locked)") 
        
    def get_action(self):
        """
        Override get_action to handle area selection for exploration.
        """
        while True:
            self.display_areas()

            print(f"{Formatter.blue_bold(len(self.areas) + 1)}. {self.return_choice.description}")

            try:
                choice = int(input(Formatter.blue("Enter the number of your choice: "))) - 1

                # Handle return home
                if choice == len(self.areas):
                    clear_screen()
                    return self.return_choice

                selected_area = list(self.areas.values())[choice]
                if selected_area.locked:
                    print(Formatter.red_bold("This area is locked. Complete quests to unlock it!"))
                    pause_clear_screen(2)
                    continue

                # Return the exploration choice for the selected area
                return Choice(
                    f"Explore {selected_area.name}",
                    lambda area=selected_area: ExplorationEvent(self.player, area).start(),
                    clear_method=clear_screen,
                )
            except (ValueError, IndexError):
                print(Formatter.yellow_bold("Invalid choice. Please try again."))
                pause_clear_screen(2)