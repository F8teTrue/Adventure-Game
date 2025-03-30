from items import Weapon, Armour, Potion, Misc
from choice import continue_clear_screen, pause_clear_screen, clear_screen
from formatter import Formatter
import pygame as pg
import sys

class Player:
    """
    Class for creating and using a player character in the game.

    Parameters:
        name (str): The player's name.

    **Starting Attributes:**
        **gold** (int): 
            The player's currency for buying items. Starts at 15.
        
        **level** (int): 
            The player's current level. Starts at 1.
        
        **xp** (int): 
            The player's experience points. Used for leveling up. Starts at 0.
        
        **max_health** (int): 
            The player's maximum health. Starts at 30.
        
        **health** (int): 
            The player's current health. Starts equal to max_health.
        
        **base_attack** (int): 
            The player's base attack value (before boosts). Starts at 5.
        
        **attack** (int): 
            The player's total attack value, including active effects.
        
        **base_defence** (int): 
            The player's base defence value (before boosts). Starts at 0.
        
        **defence** (int): 
            The player's current defence. Resets to base_defence at the start of each battle.
        
        **inventory** (list): 
            A list of items the player owns. Starts as an empty list.
        
        **active_effects** (dict): 
            Active status effects (e.g., strength_boost) that modify player stats.
        
        **weapon** (Weapon or None): 
            The player's equipped weapon, which affects attack; starts as None.
        
        **armour** (Armour or None): 
            The player's equipped armour, which affects defence; starts as None.
        
        **active_quest** (Quest or None):
            The current quest the player has accepted or None if no quest is accepted.
        
        **quest_progress** (int): The progress of the player's active quest. Starts at 0.

        **completed_quests** (list): A list of completed quests.
    """
    def __init__(self, name : str):
        self.name = name
        self.gold = 15
        self.level = 1
        self.xp = 0
        self.max_health = 30
        self.health = self.max_health
        self.base_attack = 5
        self.attack = 5 
        self.base_defence = 0
        self.defence = 0
        self.inventory = {}
        self.active_effects = {}
        self.weapon = None
        self.armour = None
        self.active_quest = None
        self.quest_progress = 0
        self.completed_quests = []
    
    # def display_status(self):
    #     """
    #     Display the player's current status, including health, level, XP, attack, and gold.
    #     """
    #     print(
    #         f"\n{Formatter.cyan_bold('Name:')} {self.name}, "
    #         f"{Formatter.cyan_bold('Level')} {self.level}: "
    #         f"({Formatter.green_bold(self.xp)}/{self.calculate_xp_needed()}), "
    #         f"{Formatter.green_bold('Health:')} {Formatter.green_bold(self.health)}/{Formatter.white_bold(self.max_health)}, "
    #         f"{Formatter.blue_bold('Attack:')} {self.attack}, "
    #         f"{Formatter.yellow_bold('Gold:')} {self.gold}"
    #     )
    #     continue_clear_screen()


    # Methods used for combat

    def take_damage(self, damage : int):
        """
        Reduce health when player takes damage.
        
        Parameters:
            damage (int): The amount of damage player takes. Damage taken is reduced by defence.
        """
        effective_defense = min(self.defence, damage)
        damage_taken = damage - effective_defense

        self.defence -= effective_defense
        self.health -= damage_taken

        if self.health <= 0:
            print(Formatter.red_bold("You have died."))
            exit()
        else:
            # print(f"{Formatter.green_bold(self.name)} has {Formatter.green_bold(self.health)} health remaining.")
    
            if self.defence > 0 or (self.defence == 0 and effective_defense > 0):
                print(f"{Formatter.green_bold(self.name)}'s remaining defense: {Formatter.blue_bold(self.defence)}")

    def start_battle(self):
        """
        Reset defence to base_defence at the start of a battle.
        """
        self.defence = self.base_defence
        print(f"{Formatter.green_bold(self.name)} starts with {Formatter.blue_bold(self.defence)} defence.")
    
    def attack_creature(self, creature: object):
        """
        Player attacks the creature

        Parameters:
            creature (Creature): The target creature being attacked.
        """
        self.apply_attack_effects()
        print(f"{Formatter.green_bold(self.name)} attacks {Formatter.red_bold(creature.name)} for {Formatter.blue_bold(self.attack)} damage!")
        creature.take_damage(self.attack)

        if "strength_boost" in self.active_effects:
            self.active_effects["strength_boost"]["duration"] -= 1
            if self.active_effects["strength_boost"]["duration"] <= 0:
                del self.active_effects["strength_boost"]
                print(Formatter.yellow_bold(f"{self.name}'s strength boost has worn off."))
    
    def apply_attack_effects(self):
        """
        Apply any active attack effects, e.g. strength potion, to the player's attack.
        """
        self.attack = self.base_attack

        if "strength_boost" in self.active_effects:
            boost_value = self.active_effects["strength_boost"]["value"]
            self.attack += boost_value 
            
        
    def add_effect(self, name : str, effect_type : str, effect_value : int, duration : int):
        """
        Add a temporary effect to the player, modifying their stats for a set duration.

        Parameters:
            name (str): The effect's name.
            effect_type (str): The type of effect (e.g., "strength_boost").
            effect_value (int): The value of the effect (e.g. +3 attack).
            duration (int): The number of turns the effect lasts.
        """
        self.active_effects[effect_type] = {"value": effect_value, "duration": duration}
        print(f"{Formatter.green_bold(self.name)} gained a temporary {Formatter.cyan_bold(name)} effect.")

    # Methods used for inventory management

    def get_inventory_item(self, item_key : str):
        """
        Retrieve an item from the inventory based on its key.

        Parameters:
            item_key (str): The key name of the item.

        Returns:
            dict or None: A dictionary containing the item and its quantity, or None if not found.
        """
        if item_key in self.inventory:
            return self.inventory[item_key]
        return None

    def add_to_inventory(self, item : object):
        """
        Add an item to the player's inventory. Stacks items if they are already in the inventory.
        
        Parameters:
            item (Item): The item to add.
        """
        item_key = item.name.lower().replace(" ","_")
        if item_key in self.inventory:
            self.inventory[item_key]['quantity'] += 1
        else:
            self.inventory[item_key] = {"item": item, "quantity": 1}
        if not isinstance(item, Misc):
            print(f"{Formatter.cyan_bold(item.name)} has been added to your inventory.") 
    
    def remove_from_inventory(self, item_key : str, quantity : int = 1):
        """
        Remove an item from the inventory by its key.

        Parameters:
            item_key (str): The key name of the item to remove.
            quantity (int): The number of items to remove. Defaults to 1.
        """
        if item_key in self.inventory:
            item_data = self.inventory[item_key]
            if item_data["quantity"] > quantity:
                item_data["quantity"] -= quantity
            else:
                del self.inventory[item_key]
        else:
            print(Formatter.yellow_bold(f"Item '{item_key}' is not in your inventory."))
    
    def categorise_inventory(self):
        """
        Organize the player's inventory by item categories.
        """
        categories = {
            "Weapons": [],
            "Armours": [],
            "Potions": [],
            "Miscellaneous": []
        }

        for details in self.inventory.values():
            item = details["item"]
            if isinstance(item, Weapon):
                categories["Weapons"].append((item, details["quantity"]))
            elif isinstance(item, Armour):
                categories["Armours"].append((item, details["quantity"]))
            elif isinstance(item, Potion):
                categories["Potions"].append((item, details["quantity"]))
            else:
                categories["Miscellaneous"].append((item, details["quantity"]))
        
        return categories
    
    def get_inventory_mapping(self):
        """
        Returns inventory data by category and a flat item number -> key map.

        Returns:
            tuple: A tuple containing:
                - categories (dict): A dictionary of item categories and their items.
                - item_mapping (dict): A mapping of item numbers to item keys.
        """
        categories =  self.categorize_inventory()
        item_mapping = {}
        item_number = 1

        for category, items in categories.items():
            for item, quantity in items:
                item_key = item.name.lower().replace(" ", "_")
                item_mapping[item_number] = item_key
                item_number += 1
        
        return categories, item_mapping
    
    def use_item(self, item_key : str) -> str:
        """
        Use or equip an item from the inventory.

        Parameters:
            item_key (str): The key name of the item to use.

        Returns:
            str: Action feedback for UI display.
        """
        if item_key not in self.inventory:
            return f"Item '{item_key}' is not in your inventory."
        
        item_data = self.inventory[item_key]
        item = item_data["item"]

        if isinstance(item, Weapon):
            item.equip(self)
            return f"Equipped {item.name}."
        
        elif isinstance(item, Armour):
            item.equip(self)
            return f"Equipped {item.name}."
        
        elif isinstance(item, Potion):
            if item.effect_type == "strength_boost" and "strength_boost" in self.active_effects:
                return "You already have an active strength boost. Wait until it wears off to use another."
            item.use(self)
            item_data["quantity"] -= 1
            if item_data["quantity"] <= 0:
                del self.inventory[item_key]
            return f"Used {item.name}."
        
        else:
            return f"{item.name} cannot be used."
    
    # def view_inventory(self):
    #     """
    #     Display the player's inventory with numbered items.
    #     Returns a mapping of numbers to item keys.
    #     """
    #     if not self.inventory:
    #         print(Formatter.yellow_bold("\nYour inventory is empty."))
    #         continue_clear_screen()
    #         return {}

    #     print(f"\n{Formatter.green_bold(self.name)}'s Inventory:")
    #     item_mapping = {}
    #     item_number = 1
    #     categories = self.categorize_inventory()

    #     for category, items in categories.items():
    #         print(f"\n{Formatter.yellow_bold(category)}:")
    #         if not items:
    #             print("  No items in this category.")
    #         else:
    #             for item, quantity in items:
    #                 stack_info = f" ({Formatter.blue_bold(f'x{quantity}')})" if quantity > 1 else ""
    #                 equipped_marker = ""
    #                 if item == self.weapon or item == self.armour:
    #                     equipped_marker = f" {Formatter.red_bold('(Equipped)')}"
    #                 print(f"  {Formatter.blue_bold(item_number)}. {Formatter.white_bold(item.name)}{stack_info}{equipped_marker} - {item.description}")
    #                 item_mapping[item_number] = item.name.lower().replace(" ", "_") 
    #                 item_number += 1

    #     return item_mapping


    # def use_item(self, item_number, item_mapping):
    #     """
    #     Use or equip an item from the inventory by number.

    #     Parameters:
    #         item_number (int): The number of the item to use.
    #         item_mapping (dict): Mapping of item numbers to item keys.
    #     """
    #     if item_number not in item_mapping:
    #         print(Formatter.yellow_bold(f"Invalid item number '{item_number}'."))
    #         return

    #     item_key = item_mapping[item_number]
    #     item = self.inventory[item_key]["item"] 

    #     if isinstance(item, Weapon):
    #         item.equip(self)
    #     elif isinstance(item, Armour):
    #         item.equip(self)
    #     elif isinstance(item, Potion):
    #         if item.effect_type == "strength_boost" and "strength_boost" in self.active_effects:
    #             print(Formatter.yellow_bold("You already have an active strength boost. Wait until it wears off to use another."))
    #             return
    #         item.use(self)
    #         self.inventory[item_key]["quantity"] -= 1 
    #         if self.inventory[item_key]["quantity"] <= 0:
    #             del self.inventory[item_key]
    #     else:
    #         print(f"{Formatter.yellow_bold(item.name)} cannot be used.")
    
    # def manage_inventory(self):
    #     """
    #     Allow the player to manage their inventory using item numbers.
    #     """
    #     while True:
    #         item_mapping = self.view_inventory()  # Display the inventory and get the mapping
    #         if not item_mapping:  # If inventory is empty, exit
    #             return

    #         choice = input(f"\nEnter the {Formatter.blue_bold('number')} of the {Formatter.white_bold('item')} to use, or '{Formatter.red_bold('back')}' to return: ").lower()

    #         if choice == "back":
    #             clear_screen()
    #             break

    #         try:
    #             item_number = int(choice)
    #             self.use_item(item_number, item_mapping)
    #             pause_clear_screen(3) 

    #         except ValueError:
    #             print(Formatter.red_bold("Invalid input. Please enter a number or 'back'."))
    #             pause_clear_screen(2)

    def adjust_gold(self, amount : int):
        """
        Adjust the player's gold by a specified amount.

        Parameters:
            amount (int): The amount to add to player's gold. Negative number to subtract.
        """
        self.gold += amount
        print(f"{Formatter.green_bold(self.name)} now has {Formatter.yellow_bold(self.gold)} gold.")

    # XP and leveling system

    def calculate_xp_needed(self):
        """
        Calculate the XP required to reach the next level.

        Returns:
            int: XP needed to level up.
        """
        return int(1.2 * self.level ** 3 + 10 * self.level)

    def gain_xp(self, amount : int):
        """
        Add XP to the player and check for level up.

        Parameters:
            amount (int): The amount of XP to add.
        """
        self.xp += amount

        while self.xp >= self.calculate_xp_needed():
            self.level_up()
    
    def level_up(self):
        """
        Increase the player's level and increase stats, adjusting health and attack.
        """
        xp_needed = self.calculate_xp_needed()
        self.level += 1
        self.xp -= xp_needed
        self.max_health += 3
        self.health += 3

        if self.level % 3 == 0: # Increase base attack every 3 levels
            self.base_attack += 1
        
        self.attack = self.base_attack
        print(f"\n{Formatter.green_bold(self.name)} leveled up to {Formatter.cyan_bold('Level ' + str(self.level))}!")
        print(
            f"{Formatter.white_bold('Max Health')} has increased, and your {Formatter.green_bold('Health')} is now "
            f"{Formatter.green_bold(self.health)}/{Formatter.white_bold(self.max_health)}, "
            f"and {Formatter.blue_bold('Attack')} is now {Formatter.blue_bold(self.attack)}.\n"
        )