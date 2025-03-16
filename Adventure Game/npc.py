from quest import StoryQuest
from otherFunctions import print_slow
from choice import continue_clear_screen
from formatter import Formatter

class NPC:
    """
    A class representing a Non-Player Character (NPC) in the game.

    Parameters:
        name (str): The name of the NPC.
        dialogue_steps (list): The dialogue or conversation text of the NPC.
        quest_trigger (str): Optional trigger for triggering a quest step.
    """
    def __init__(self, name : str, dialogue_steps : list, quest_trigger : str = None):
        self.name = name
        self.dialogue_steps = dialogue_steps
        self.quest_trigger = quest_trigger
        self.interacted = False # Flag to track if the NPC has been interacted with

    def get_current_dialogue(self, player : object):
        """
        Decides the current dialogue the NPC should display based on the player's active quest progress.

        Parameters:
            player (Player): The player interacting with the NPC.

        Returns:
            (str): The dialogue text to display.
        """
        if isinstance(player.active_quest, StoryQuest):
            quest = player.active_quest
            if quest.current_step < len(self.dialogue_steps):
                return self.dialogue_steps[quest.current_step]
            elif quest.current_step >= len(quest.steps):
                return f"{self.name}: Thank you for your help, brave adventurer!"
        return f"{self.name}: I have nothing more to say right now."
    
    def interact(self, player : object):
        """
        Interact with the NPC. Optionally trigger a quest step.

        Parameters:
            player (Player): The player interacting with the NPC.
        """
        if self.quest_trigger and isinstance(player.active_quest, StoryQuest):
            quest = player.active_quest
            current_step = quest.steps[quest.current_step]

            if current_step["type"] == "interaction" and current_step["trigger"].get("npc") == self.quest_trigger:
                dialogue = current_step.get("dialogue", f"{self.name} has nothing more to say right now.")
                print(Formatter.blue("\nPress Space to skip..."))
                print(f"\n{Formatter.cyan_bold(self.name)}:", end=" ")
                print_slow(dialogue)
                
                quest_progressed = quest.trigger_step("interaction", {"npc": self.quest_trigger}, player)
                if quest_progressed:
                    self.interacted = True
                continue_clear_screen()
                return

        print(Formatter.yellow_bold(f"{self.name} has nothing more to say right now."))
        continue_clear_screen()