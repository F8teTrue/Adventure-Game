from items import all_items
import random as rn
from quest import CombatQuest
from choice import continue_clear_screen, pause_clear_screen
from formatter import Formatter

def combat(player : object, creature : object, area : object):
    """
    Handles a turn-based combat system between the player and a creature.
    
    Parameters:
        player (Player): The player object participating in combat.
        creature (Creature): The creature object participating in combat.
        area (Area): The area where the combat takes place.
    """
    player.start_battle()

    while player.health > 0 and creature.health > 0:
        print(f"\n{Formatter.red_bold(creature.name)}'s Health: {Formatter.red_bold(creature.health)}")
        print(f"{Formatter.green_bold(player.name)}'s Health: {Formatter.green_bold(player.health)}/{player.max_health}\n")

        print(Formatter.cyan_bold("Choose an action:"))
        print(f"{Formatter.blue('1.')} Attack")
        print(f"{Formatter.blue('2.')} Use an item")
        print(f"{Formatter.blue('3.')} Check quest progress")
        print(f"{Formatter.blue('4.')} Try to flee from combat")

        choice = input(Formatter.blue("Enter the number of your choice: "))

        print()
        if choice == "1":
            player.attack_creature(creature)

            if creature.health > 0:
                creature.attack_player(player)
            else:
                # Handle rewards for defeating the creature
                rewards = creature.get_rewards()

                if rewards["xp"] > 0:
                    player.gain_xp(rewards["xp"])

                if rewards["gold"] > 0:
                    player.adjust_gold(rewards["gold"])

                if rewards["item"]:
                    item = all_items.get(rewards["item"])
                    if item:
                        player.add_to_inventory(item)
                    else:
                        print(Formatter.yellow_bold(f"The item '{rewards['item']}' could not be identified."))
                
                if player.active_quest and isinstance(player.active_quest, CombatQuest):
                    # Conditions for quest progress
                    quest = player.active_quest
                    meets_type_condition = (quest.target_type == "any" or creature.name.lower() == quest.target_type)
                    meets_area_difficulty = (quest.min_difficulty <= area.difficulty)

                    # Update quest progress if conditions are met
                    if meets_type_condition and meets_area_difficulty:
                        player.quest_progress += 1
                        print(f"Quest Progress: {Formatter.green_bold(player.quest_progress)}/{quest.target_count}")

                        # Check for quest completion
                        if player.quest_progress >= quest.target_count:
                            quest.complete_quest(player)
                            player.active_quest = None
                            player.quest_progress = 0 
                            print(Formatter.green_bold("\nQuest completed and rewards granted.\n"))

        elif choice == "2":
            if not player.inventory:
                print(Formatter.yellow_bold("Your inventory is empty. Please chose another option."))
                pause_clear_screen()
            else:
                player.manage_inventory()
                creature.attack_player(player)
        elif choice == "3":
            if player.active_quest and isinstance(player.active_quest, CombatQuest):
                print(f"{Formatter.cyan_bold('Current Quest')}: {player.active_quest.desc}")
                print(f"{Formatter.cyan_bold('Progress')}: {Formatter.green_bold(player.quest_progress)}/{player.active_quest.target_count}")
                continue_clear_screen()
            else:
                print(Formatter.yellow_bold(f"{player.name} does not have an active quest."))
                pause_clear_screen()
                continue
        elif choice == "4":
            if flee():
                print(f"{Formatter.green_bold(player.name)} successfully fled from {Formatter.red_bold(creature.name)}!")
                continue_clear_screen()
                return "fled"
            else:
                print(f"{Formatter.red_bold(player.name)} tried to flee, but {Formatter.red_bold(creature.name)} blocked the escape!")
                creature.attack_player(player)
                pause_clear_screen()
        else:
            print(Formatter.yellow_bold("Invalid choice. Please select a valid option."))
            pause_clear_screen()
            continue

def flee() -> bool:
    """
    Attempts to flee from combat with a 25% chance of success.
    
    Returns:
        bool: True if the player successfully flees, False otherwise.
    """
    chance_to_flee = 0.25
    return rn.random() < chance_to_flee