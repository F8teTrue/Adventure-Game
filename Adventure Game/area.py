import random as rn
from creature import create_creature
from formatter import Formatter


class Area:
    """
    A class for creating different areas in the game that the player can explore.

    Parameters:
        name (str): The name of the area.
        difficulty (int): The difficulty of the area. Correlates with the type of  or amount of creatures that can be found there.
        creature_types (list): The types of creature that can be found in the area (e.g. ["zombie", "skeleton"]).
        max_creatures (int): The maximum amount of creatures that can spawn. Defaults to 3.
        boss (str, optional): The name of the boss creature, if one exists in the area.
        treasure_chance (float): The chance of finding treasure in the area. Defaults to 0.5.
        treasure_quality_list (list): The quality levels of treasure that can be found in the area. Defaults to [1], which is the worst.
        event_sequence (list): The sequence of events that can occur in the area. Defaults to ["combat"].
        locked (bool): Whether the area is initially locked. Defaults to True.

    **Starting Attributes:**
        **creatures** (list): 
            A list of creatures currently present in the area, generated during exploration.
        **boss_active** (bool): 
            Whether the boss has been spawned. Starts as False.
    """
    def __init__(self, name : str, difficulty : int, creature_types : list, max_creatures = 3, boss : str = None, treasure_chance : float = 0.5, treasure_quality_list : list = [1], event_sequence : list = None, locked : bool = True):
        self.name = name
        self.difficulty = difficulty
        self.creature_types = creature_types
        self.max_creatures = max_creatures
        self.creatures = []
        self.boss = boss
        self.boss_active = False
        self.treasure_chance = treasure_chance
        self.treasure_quality_list = treasure_quality_list
        self.event_sequence = event_sequence or ["combat"]
        self.locked = locked
    
    def generate_creatures(self):
        """
        Generate a random number of creatures for the area based on maximum amount of creatures and creature types.
        """
        num_creatures = rn.randint(1, self.max_creatures)
        self.creatures = [create_creature(rn.choice(self.creature_types)) for _ in range(num_creatures)]
        print(f"{Formatter.yellow_bold(num_creatures)} creatures have appeared in {Formatter.cyan_bold(self.name)}!")

    def spawn_boss(self):
        """
        Spawn the boss if it exists in the area, hasn't already appeared and is not already in the creatures list.
        """
        if self.boss and not self.boss_active and not any(c.name == self.boss for c in self.creatures):
            self.creatures.append(create_creature(self.boss))
            self.boss_active = True
            print(Formatter.red_bold(f"\nThe boss, {self.boss}, has appeared in the {self.name}!"))

    def choose_quality(self):
        """
        Decides the quality of treasure found based on the treasure quality list.

        Returns:
            chosen_quality (int): The chosen treasure quality level.
        """
        rarity_names = {
            1: "Common",
            2: "Blessed",
            3: "Enchanted",
            4: "Arcane",
            5: "Mythic",
            6: "Divine"
        }

        max_quality = max(self.treasure_quality_list)

        # Check if the list covers a full range from 1 to max_quality
        if self.treasure_quality_list == list(range(1, max_quality + 1)):
            # Use exponential weights for full ranges (e.g., [32, 16, 8, 4, 2, 1] for [1, 2, 3, 4, 5, 6])
            weights = [2 ** (max_quality - quality) for quality in self.treasure_quality_list]
        else:
            # For partial ranges, use linear weights (e.g., [3, 2, 1] for [1, 2, 3])
            weights = [len(self.treasure_quality_list) - i for i in range(len(self.treasure_quality_list))]

        # Choose a quality based on weights
        chosen_quality = rn.choices(self.treasure_quality_list, weights=weights, k=1)[0]
        rarity_name = rarity_names[chosen_quality]
        print(f"You have found a {Formatter.green_bold(rarity_name)} treasure!")
        return chosen_quality