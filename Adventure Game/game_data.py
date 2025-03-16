import json, os
from area import Area
from shop import Shop
from quest import CombatQuest, StoryQuest

# Load area data from areas.json
with open("Adventure Game/json/areas.json", "r") as areas_file:
    areas_data = json.load(areas_file)

# Create area objects from the loaded data
areas = {}
for area_name, area_info in areas_data.items():
    areas[area_name.lower().replace(" ", "_")] = Area(
        name = area_info["name"],
        difficulty = area_info["difficulty"],
        creature_types = area_info["creature_types"],
        max_creatures = area_info.get("max_creatures", 3),
        treasure_chance = area_info.get("treasure_chance", 0.5),
        treasure_quality_list = area_info.get("treasure_quality_list", [1]),
        boss = area_info.get("boss"),
        event_sequence = area_info.get("event_sequence"),
        locked = area_info.get("locked", True)
    )


# Create shop objects by loading data from individual JSON files
shops_dir = "Adventure Game/json/shops/"
shops = {}

for filename in os.listdir(shops_dir):
    shop_path = os.path.join(shops_dir, filename)
    with open (shop_path, "r") as file:
        shop_data = json.load(file)
        shop_name = shop_data["name"]
        # Initialize the shop object with the loaded data and add it to the shops dictionary
        shops[shop_name] = Shop(shop_data)


# Load combat quest data from combat_quests.json
with open("Adventure Game//json/quests/combat_quests.json", "r") as combat_quest_file:
    combat_quest_data = json.load(combat_quest_file)

# Create combat quest objects from the loaded data
combat_quests = {}
for quest_id, quest_info in combat_quest_data.items():
    combat_quests[quest_id] = CombatQuest(
        desc = quest_info["desc"],
        area = quest_info["area"],
        reward = quest_info["reward"],
        target_type = quest_info["target_type"],
        target_count = quest_info["target_count"],
        min_difficulty = quest_info["min_difficulty"]
    )

# Load story quest data from story_quests.json
with open("Adventure Game//json/quests/story_quests.json", "r") as story_quest_file:
    story_quests_data = json.load(story_quest_file)

# Create story quest objects from the loaded data
story_quests = {}
for quest_id, quest_info in story_quests_data.items():
    story_quests[quest_id] = StoryQuest(
        desc = quest_info["desc"],
        area = quest_info["area"],
        reward = quest_info["reward"],
        unlock_area = quest_info.get("unlock_area"),
        steps = quest_info.get("steps", []),
        linked_location = quest_info.get("linked_location"),
        unlock_quest = quest_info.get("unlock_quest"),
        areas = areas 
    )