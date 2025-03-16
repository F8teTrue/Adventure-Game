import random as rn
from formatter import Formatter

class Creature:
    """
    Class to create creatures in the game.

    Parameters:
        name (str): The name of the creature.
        type (str): The type of creature (e.g. undead or humanoid).
        max_health (int): The creature's maximum health.
        health (int): The creature's current health. Starts equal to max_health.
        attack (int): The creature's attack power.
        xp_drop (int): The amount of expirience points the creature should drop on death.
        gold_drop (int): The amount of gold the creature should drop on death.
        loot (list): List of potential loot the creature should drop on death.
    """
    def __init__(self, name : str, type : str, max_health : int, health : int, attack : int, xp_drop : int, gold_drop : int, loot : list = None):
        self.name = name
        self.type = type
        self.max_health = max_health
        self.health = health
        self.attack = attack
        self.xp_drop = xp_drop
        self.gold_drop = gold_drop
        self.loot = loot or []
    
    def take_damage(self, damage : int):
        """
        Reduce health when creature takes damage.

        Parameters:
            damage (int): The amount of damage the creature takes.
        """
        self.health -= damage
        if self.health <= 0:
            print(f"{Formatter.red_bold(self.name)} has been defeated!")
            
    
    def attack_player(self, player):
        """
        Inflicts damage on the player equal to the creature's attack power.

        Parameters:
            player (Player): The player object that will receive the damage.
        """
        print(f"{Formatter.red_bold(self.name)} attacks {Formatter.green_bold(player.name)} for {Formatter.yellow_bold(self.attack)} damage.")
        player.take_damage(self.attack)
    
    def get_rewards(self):
        """
        Returns the rewards for defeating the creature.

        Returns:
            rewards (dict): A dictionary containing the rewards for defeating the creature.
        """
        rewards = {"xp": self.xp_drop, "gold": self.gold_drop, "item": None}

        print(f"\n{Formatter.cyan_bold('Rewards:')}")
        if self.xp_drop > 0:
            print(f"- XP: {Formatter.green_bold(self.xp_drop)}")
        
        if self.gold_drop > 0:
            print(f"- Gold: {Formatter.yellow_bold(self.gold_drop)}")

        if self.loot:
            loot_item = rn.choice(self.loot)
            rewards["item"] = loot_item
            formatted_loot_item = loot_item.replace("_", " ").title()
            if loot_item:
                print(f"- Item: {Formatter.cyan_bold(formatted_loot_item)}")
        
        return rewards


def create_creature(creature_type : str):
    """
    Generate a creature instance based on the specified creature.

    Parameters:
        creature_type (str): The type of creature to create (e.g. "zombie", "skeleton").

    Returns:
        creature (Creature): An instance of the Creature class based on the specified type.
    """
    if creature_type == "zombie":
        health = rn.randint(8, 14)
        return Creature("Zombie", "Undead", health, health, 2, 3, 2)
    elif creature_type == "skeleton":
        health = rn.randint(7, 12)
        return Creature("Skeleteon", "Undead", health, health, 4, 3, 3)
    elif creature_type == "goblin":
        health = rn.randint(5, 7)
        return Creature("Goblin", "Humanoid", health, health, 3, 2, 4)
    elif creature_type == "spirit":
        health = rn.randint(10, 15)
        return Creature("Spirit", "Ethereal", health, health, 3, 5, 3)
    elif creature_type == "fairy":
        health = rn.randint(6, 10)
        return Creature("Fairy", "Ethereal", health, health, 2, 4, 2)
    elif creature_type == "fairy queen":
        health = rn.randint(15,19)
        return Creature("Fairy Queen", "Ethereal", health, health, 5, 15, 5)
    elif creature_type == "giant frog":
        health = rn.randint(13, 17)
        return Creature("Giant Frog", "Beast", health, health, 2, 8, 4)
    elif creature_type == "swamp monster":
        health = rn.randint(18, 22)
        return Creature("Swamp Monster", "Beast", health, health, 2, 10, 5)
    elif creature_type == "giant spider":
        health = rn.randint(13, 17)
        return Creature("Giant Spider", "Beast", health, health, 4, 8, 4)
    elif creature_type == "orc":
        health = rn.randint(18, 22)
        return Creature("Orc", "Humanoid", health, health, 5, 10, 5)
    elif creature_type == "troll":
        health = rn.randint(28, 32)
        return Creature("Troll", "Humanoid", health, health, 7, 12, 8)
    elif creature_type == "dark wizard":
        health = rn.randint(18, 22)
        return Creature("Dark Wizard", "Humanoid", health, health, 8, 20, 10, ["great_sword"])
    else:
        raise ValueError(f"Unknown creature type: {creature_type}")