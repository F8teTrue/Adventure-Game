import json
from formatter import Formatter

class Item:
    """
    Base class for items in the game.

    Parameters:
        name (str): The name of the item.
        effect_value (int): The effect value of the item (e.g., attack or defense bonus).
        description (str): A short description of the item and its effects.
    """
    def __init__(self, name : str, effect_value : int, description : str):
        self.name = name
        self.effect_value = effect_value
        self.description = description

class Weapon(Item):
    """
    Class for weapons, inheriting from Item.
    """
    def equip(self, player : object):
        """
        Unequip the player's current weapon (if any) and equip the new weapon, updating the player's attack stat.
        """
        if player.weapon:
            player.base_attack -= player.weapon.effect_value
        player.weapon = self
        player.base_attack += self.effect_value
        player.attack = player.base_attack
        print(f"{Formatter.green_bold(player.name)} equipped {Formatter.cyan_bold(self.name)}, gaining +{Formatter.yellow_bold(self.effect_value)} attack.")

    def unequip(self, player : object):
        """
        Unequip the player's current weapon, resetting the attack stat.
        """
        if player.weapon:
            player.base_attack -= player.weapon.effect_value
            player.weapon = None
            print(f"{Formatter.green_bold(player.name)} unequipped {Formatter.cyan_bold(self.name)}, losing -{Formatter.yellow_bold(self.effect_value)} attack.")

class Armour(Item):
    """
    Class for armours, inheriting from Item.
    """
    def equip(self, player : object):
        """
        Unequip the player's current armour (if any) and equip the new armour, updating the player's defence stat.
        """
        if player.armour:
            player.base_defence -= player.armour.effect_value
        player.armour = self
        player.base_defence += self.effect_value
        print(f"{Formatter.green_bold(player.name)} equipped {Formatter.cyan_bold(self.name)}, gaining +{Formatter.yellow_bold(self.effect_value)} defence.")
    
    def unequip(self, player : object):
        """
        Unequip the player's current armour, resetting the defence stat.
        """
        if player.armour:
            player.base_defence -= player.armour.effect_value
            player.armour = None
            print(f"{Formatter.green_bold(player.name)} unequipped {Formatter.cyan_bold(self.name)}, losing -{Formatter.yellow_bold(self.effect_value)} defence.")

class Potion(Item):
    """
    Class for potions, inheriting from Item.
    
    Parameters:
        effect_type (str): Type of effect (e.g., "heal", "strength_boost").
        duration (int, optional): Duration of the effect (only for certain types of effects).
    """
    def __init__(self, name : str, effect_type : str, effect_value : int, description : str, duration : int =None):
        super().__init__(name, effect_value, description)
        self.effect_type = effect_type
        self.duration = duration

    def use(self, player : object):
        """
        Apply the potion's effect to the player.

        Parameters:
            player (Player): The player object the effect should be applied to.
        """
        if self.effect_type == "heal":
            # Heal the player by the effect value, up to their maximum health
            player.health = min(player.max_health, player.health + self.effect_value)
            print(f"{Formatter.green_bold(player.name)} used {Formatter.cyan_bold(self.name)} and healed {Formatter.green_bold(self.effect_value)} health.")
        elif self.effect_type == "strength_boost":
            # Apply a strength boost effect if not already active
            if "strength_boost" in player.active_effects:
                print(Formatter.yellow_bold("Strength potion already active."))
            else:
                player.add_effect(self.name, self.effect_type, self.effect_value, self.duration)

class Misc(Item):
    """
    Class for miscellaneous items, inheriting from Item.

    Parameters:
        item_type (str): The type of the item (e.g. "story_item").
    """
    def __init__(self, name : str, item_type : str, effect_value : int, description : str):
        super().__init__(name, effect_value, description)
        self.item_type = item_type


# Load items data from the JSON file
with open("Adventure Game/json/items.json", "r") as items_file:
    items_data = json.load(items_file)

# Dictionaries to store different types of items
weapons = {}
armours = {}
potions = {}
miscellaneous = {}

# Create item objects from the loaded data and store them in the right dictionaries
for weapon in items_data["weapons"]:
    weapons[weapon["name"].lower().replace(" ", "_")] = Weapon(weapon["name"], weapon["effect_value"], weapon["desc"])

for armour in items_data["armours"]:
    armours[armour["name"].lower().replace(" ", "_")] = Armour(armour["name"], armour["effect_value"], armour["desc"])

for potion in items_data["potions"]:
    potions[potion["name"].lower().replace(" ", "_")] = Potion(
        potion["name"],
        potion["effect_type"],
        potion["effect_value"],
        potion["desc"],
        potion.get("duration")
    )

for misc in items_data["miscellaneous"]:
    miscellaneous[misc["name"].lower().replace(" ", "_")] = Misc(misc["name"], misc["type"], misc["effect_value"], misc["desc"])

# Combine all items into a single dictionary
all_items = {**weapons, **armours, **potions, **miscellaneous}