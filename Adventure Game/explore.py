from events import CreatureCombatEvent, BossEvent, TreasureEvent
from quest import StoryQuest
import random as rn
from choice import clear_screen, continue_clear_screen
from formatter import Formatter

class ExplorationEvent:
    """
    Handles exploration events in an area.

    Parameters:
        player (Player): The player exploring the area.
        area (Area): The area being explored.
    
    **Startin Attributes**:
        **quest** (StoryQuest or None): 
            The active story quest, if any.
        **quest_step_progressed** (bool): 
            Tracks if a quest step has been progressed during exploration.
        **event_sequence** (list or None): 
            A list of events to execute in order (e.g. ["combat", "story"])
        **current_event_index** (int): 
            The index of the current event in the sequence.
    """
    def __init__(self, player : object, area : object):
        self.player = player
        self.area = area

        self.quest = player.active_quest if isinstance(player.active_quest, StoryQuest) else None
        self.quest_step_progressed = False
        self.event_sequence = list(self.area.event_sequence)
        self.current_event_index = 0

    def start(self):
        """
        Start the exploration of the area, triggering events in sequence.
        """
        clear_screen()
        print(f"{Formatter.cyan_bold('Exploring ' + self.area.name + '...')}")
        
        # If a specific sequence is provided, a loop will trigger each event in order
        for event_type in self.event_sequence:
            self.trigger_event(event_type)
            if self.player.health <= 0:
                break
                
        self.end_exploration()

    
    def trigger_event(self, event_type):
        """
        Triggers the specified event type.

        Parameters:
            event_type (str): The type of event to trigger (e.g. "combat", "story", "boss").
        """
        if event_type == "combat":
            CreatureCombatEvent(self.player, self.area).trigger()
        elif event_type == "treasure":
            if rn.random() < self.area.treasure_chance: # Trigger treasure event based on area treasure chance
                TreasureEvent(self.player, self.area).trigger()
        elif event_type == "boss":
            BossEvent(self.player, self.area).trigger()
        elif self.quest and not self.quest_step_progressed:
            self.check_story_progression()
        else:
            print(Formatter.yellow_bold(f"Unknown event type: {event_type}"))


    def check_story_progression(self):
        """
        Check if the current area matches a story quest step and progress the quest if it does.
        """
        if self.quest.trigger_step(
            "exploration", {"area": self.area.name.lower().replace(" ", "_")}, self.player
        ):
            self.quest_step_progressed = True

    
    def end_exploration(self):
        """
        Handle the end of exploration. Check for quest completion.
        """
        if self.quest and not self.quest_step_progressed:
            self.check_story_progression()

        print(f"\nExploration of {Formatter.cyan_bold(self.area.name)} is complete.") 
        continue_clear_screen()