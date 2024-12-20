from combat import combat
from creature import create_creature
from choice import continue_clear_screen
from formatter import Formatter

class Event:
    """
    Base class for events in the game.
    
    Parameters:
        player (Player): The player involved in the event.
        area (Area): The area where the event takes place.
    """
    def __init__(self, player : object, area : object = None):
        self.player = player
        self.area = area

    def trigger(self):
        """
        Triggers the event. To be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses should implement this method.")


class CreatureCombatEvent(Event):
    """
    Handles combat with regular creatures in an area.
    
    Parameters:
        player (Player): The player involved in combat.
        area (Area): The area where the combat takes place.
        quest (Quest or None): The player's active quest, if any.
    """
    def __init__(self, player : object, area : object):
        super().__init__(player, area)
        
    def trigger(self):
        """
        Triggers a combat event with creatures in the area.
        """
        self.area.generate_creatures()

        while self.area.creatures:
            creature = self.area.creatures.pop(0)
            print(f"You encounter a {Formatter.red_bold(creature.name)}!")
            result = combat(self.player, creature, self.area)

            if result == "fled":
                print(Formatter.green_bold(f"{self.player.name} has fled from combat!"))
                return

            if self.player.health <= 0:
                print(Formatter.red_bold("Game over!"))
                return
            
            continue_clear_screen()


class BossEvent(Event):
    """
    Handles a unique boss encounter in an area.

    Parameters:
        player (Player): The player involved in the boss battle.
        area (Area): The area where the boss encounter takes place.
    """
    def __init__(self, player : object, area : object):
        super().__init__(player, area)

    def trigger(self):
        """
        Triggers a boss encounter, where the boss appears if it hasn't been defeated.
        """
        if self.area.boss and not self.area.boss_active:
            boss = create_creature(self.area.boss)
            self.area.boss_active = True
            print(f"{Formatter.grey('The boss')} {Formatter.red_bold(boss.name)} {Formatter.grey('has appeared!')}")
            result = combat(self.player, boss, self.area)
            
            if result == "fled":
                print(Formatter.green_bold(f"{self.player.name} has fled from the boss battle!"))
            elif self.player.health <= 0:
                print(Formatter.red_bold("Game over!")) 
            else:
                self.area.boss_active = False
            
            continue_clear_screen()
        else:
            print(Formatter.blue("The boss has already been defeated or does not exist in this area."))

class TreasureEvent(Event):
    """
    An event that gives the player a chance to find a treasure.

    Parameters:
        player (Player): The player involved in the event.
        area (Area): The area where the event takes place.
    """
    def __init__(self, player : object, area : object):
        super().__init__(player, area)
        self.chance = area.treasure_chance # Chance of finding treasure

    def trigger(self):
        """
        Triggers a treasure event.
        """
        quality_gold_rewards = {
            1: 10,  # Common
            2: 20,  # Blessed
            3: 35,  # Enchanted
            4: 50,  # Arcane
            5: 75,  # Mythic
            6: 100  # Divine
        }

        quality = self.area.choose_quality()
        gold_reward = quality_gold_rewards.get(quality, 10)

        print(f"You received {Formatter.yellow_bold(gold_reward)} gold as a reward!")
        self.player.adjust_gold(gold_reward)