from items import all_items
from otherFunctions import print_slow
from formatter import Formatter

class Quest:
    """
    Base class to represent quests available to the player.
    
    Parameters:
        desc (str): Description of the quest objective.
        area (str): The name of the area where the quest takes place.
        reward (dict): Rewards for completing the quest.
    """
    def __init__(self, desc : str, area : str, reward : dict):
        self.desc = desc
        self.area = area
        self.reward_xp = reward.get("xp", 0)
        self.reward_gold = reward.get("gold", 0)
        self.reward_items = reward.get("items", [])
    
    def complete_quest(self, player):
        """
        Completes the quest, awarding the player with the quest's rewards.

        Parameters:
            player (Player): The player completing the quest and getting the rewards.
        """
        print(f"\n{Formatter.green_bold('Quest Complete:')} {self.desc}")
        print(f"{Formatter.cyan_bold('Rewards:')} {self.display_rewards()}")
        
        player.gain_xp(self.reward_xp)
        player.adjust_gold(self.reward_gold)

        for item_key in self.reward_items:
            item = all_items.get(item_key)
            if item:
                player.add_to_inventory(item)

    def display_rewards(self):
        """
        Formats the rewards and displays them.
        """
        if self.reward_items:
            item_rewards = ", ".join(
                item.replace("_", " ").title() for item in self.reward_items
            )
        else:
            item_rewards = "None"

        reward_message = (
            f"{Formatter.green_bold(self.reward_xp)} XP, {Formatter.yellow_bold(self.reward_gold)} gold, Items: {Formatter.green_bold(item_rewards)}"
        )

        return reward_message

    def is_complete(self, player):
        """
        Checks if the quest conditions are met.
        Should be overridden by subclasses.
        """
        raise NotImplementedError("This method should be implemented in subclasses.")


class CombatQuest(Quest):
    """
    Combat quest requiring the player to defeat creatures of a specific type or a specific amount.
    
    Parameters:
        target_count (str): Specifies the target type.
        target_count (int): Number of creatures to defeat.
        min_difficulty (int): Minimum difficulty of the area.
    """
    def __init__(self, desc : str, area : str, reward : dict, target_type : str, target_count : int, min_difficulty : int = 0):
        super().__init__(desc, area, reward)
        self.target_type = target_type
        self.target_count = target_count
        self.min_difficulty = min_difficulty

class StoryQuest(Quest):
    """
    Story quest that may involve unique events or narrative progression.
    
    Parameters:
        desc (str): Description of the quest objective.
        area (Area): The name of the area where the quest takes place.
        reward (dict): Rewards for completing the quest.
        unlock_area (str): Name of the area to unlock upon quest completion.
        steps (list): List of steps to complete the quest.
        linked_location (str): Name of the location linked to the quest.
        areas (dict): Dictionary of areas in the game. Used to unlock areas.
        locations (dict): Dictionary of locations in the game. Used to update NPCs and linked locations.
    """
    def __init__(self, desc : str, area : object, reward : dict, unlock_area : str = None, steps : list = None, linked_location : str = None, areas : dict = None, locations : dict = None, unlock_quest : str = None):
        super().__init__(desc, area, reward)
        self.requires_story_event = True
        self.unlock_area = unlock_area
        self.steps = steps or []
        self.current_step = 0
        self.linked_location = linked_location
        self.unlock_quest = unlock_quest 
        self.areas = areas
        self.locations = locations
        self.locked = True
    
    def display_current_step(self):
        """
        Displays the current step of the quest.
        """
        if self.current_step < len(self.steps):
            step = self.steps[self.current_step]
            print(Formatter.cyan_bold(step['description']))

    def trigger_step(self, trigger_type : str, trigger_data : dict, player : object):
        """
        Check if the current step's trigger matches the given trigger type and data.

        Parameters:
            trigger_type (str): Type of trigger (e.g., "interaction", "exploration").
            trigger_data (dict): Data related to the trigger (e.g., {"npc": "villager"}).
            player (Player): The player interacting with the quest.

        Returns:
            bool: True if the step is triggered and progresses, False otherwise.
        """
        if self.current_step < len(self.steps):
            current_step = self.steps[self.current_step]
            current_trigger = current_step.get("trigger", {})

            # Check if the step's type and trigger match the provided type and data
            if current_step["type"] == trigger_type:
                if all(current_trigger.get(k) == v for k, v in trigger_data.items()):
                    self.progress_step(player)
                    return True

        print(Formatter.red_bold("Trigger did not match. Step not progressed."))
        return False

    def progress_step(self, player):
        """
        Progress to the next step of the quest. Completes the quest if all steps are done.

        Parameters:
            player (Player): The player progressing through the quest.
        """
        if self.current_step < len(self.steps):
            current_step = self.steps[self.current_step]
            
            # Unlock an area if specified in the current step
            if 'unlock_area' in current_step:
                unlock_area_key = current_step['unlock_area'] 
                area_to_unlock = self.areas.get(unlock_area_key)
                if area_to_unlock:
                    if area_to_unlock.locked:
                        area_to_unlock.locked = False
                        print(f"\nArea unlocked: {Formatter.cyan_bold(area_to_unlock.name)}")
                else:
                    print(f"Error: Area '{unlock_area_key}' not found in areas dictionary!")
            
            # Display story text for exploration steps
            if current_step["type"] == "exploration" and "story_text" in current_step:
                print(Formatter.blue("\nPress Space to skip..."))
                print(f"\n{Formatter.cyan_bold('Story:')}", end=" ")
                print_slow(current_step["story_text"])
                print()

            # Give the player story item if specified
            if "story_item" in current_step:
                story_item_key = current_step["story_item"]
                story_item = all_items.get(story_item_key)
                if story_item:
                    player.add_to_inventory(story_item)
                    print(f"{Formatter.magenta_bold(story_item.name)} has been added to your inventory.")
                else:
                    print(f"{Formatter.red_bold('Error: Story item not found.')}")
            
            if "reward_item" in current_step:
                reward_item_key = current_step["reward_item"]
                reward_item = all_items.get(reward_item_key)
                if reward_item:
                    player.add_to_inventory(reward_item)
                else:
                    print(f"{Formatter.red_bold('Error: Reward item not found.')}")

            self.current_step += 1

        # Check if all steps are complete
        if self.current_step >= len(self.steps):
            print(Formatter.green_bold("You have completed all the steps in this quest!"))
            self.complete_quest(player)
        else:
            self.display_current_step()
    
    def complete_quest(self, player):
        """
        Completes the quest, awards rewards, and handles linked NPCs or locations.

        Parameters:
            player (Player): The player completing the quest
        """
        super().complete_quest(player)

        # Handle linked location and NPC updates
        if self.linked_location:
            if not self.locations:
                print(Formatter.red_bold("Error: Locations not set in quest. Unable to update NPCs or linked location."))
                return

            linked_location = self.locations.get(self.linked_location)
            if linked_location and hasattr(linked_location, "npc_dict"):
                # Remove NPCs associated with the quest
                for step in self.steps:
                    if step["type"] == "interaction":
                        npc_name = step["trigger"].get("npc")
                        if npc_name in linked_location.npc_dict:
                            del linked_location.npc_dict[npc_name]

                linked_location.update_choices()

        # Remove the quest from the Quest Hall
        quest_hall = self.locations.get("quest_hall")
        if quest_hall:
            for category in [quest_hall.combat_quests, quest_hall.story_quests]:
                for quest_id, quest in list(category.items()):
                    if quest == self:
                        del category[quest_id]
                        break
            
            # Unlock the next quest if specified
            if self.unlock_quest and self.unlock_quest in quest_hall.story_quests:
                next_quest = quest_hall.story_quests[self.unlock_quest]
                next_quest.locations = self.locations
                next_quest.locked = False  # Unlock the next quest
                print(f"\n{Formatter.green_bold('New quest unlocked:')} {next_quest.desc}")