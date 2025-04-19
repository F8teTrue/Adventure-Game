from items import all_items
from choice import pause_clear_screen, continue_clear_screen, clear_screen
from formatter import Formatter

class Shop:
    """
    A class for creating shops where the player can buy and sell items.

    Parameters:
        data (dict): A dictionary containing the shop's name, inventory, and prices.
    """
    def __init__(self, data : dict):
        self.name = data["name"]
        self.inventory = {"weapons": {}, "armours": {}, "potions": {}} # Categories of items in the shop
        self.prices = {"weapons": {}, "armours": {}, "potions": {}} # Prices of items in the shop

        # Load items and their prices into inventory and price dictionaries
        for category, items_list in  data["inventory"].items():
            for item_name, price in items_list.items():
                item_key = item_name.lower().replace(" ", "_")
                item = all_items.get(item_key)
                if item:
                    self.inventory[category][item_key] = item
                    self.prices[category][item_key] = price
    
    def get_items_by_category(self, category: str):
        """
        Returns a list of items in the specified category.
        
        Parameters:
            category (str): The category of items to retrieve (e.g., "weapons", "armours", "potions").

        Returns:
            list: A list of tuples containing item keys and their corresponding items.
        """
        return list(self.inventory.get(category.lower(), {}).items())

    def get_item_price(self, category: str, item_key: str):
        """
        Returns the price of an item in the given category.
        
        Parameters:
            category (str): The category of the item (e.g., "weapons", "armours", "potions").
            item_key (str): The key representing the item name.
        
        Returns:
            int: The price of the item, or 0 if the item is not found.
        """
        return self.prices.get(category, {}).get(item_key)
    
    def buy_item(self, player, category: str, item_key: str):
        """
        Allows the player to buy an item from the shop.

        Parameters:
            player (Player): The player who is buying the item.
            category (str): The category of the item (e.g., "weapons", "armours", "potions").
            item_key (str): The key representing the item name.
        
        Returns:
            bool: True if the item was bought successfully, False otherwise.
            str: A message indicating the result of the purchase.
        """
        item = self.inventory[category].get(item_key)
        print(f"Buying {item_key} from {category}") # Debug
        print(f"Inventory keys: {list(self.inventory[category].keys())}") # Debug
        price = self.get_item_price(category, item_key)

        if not item or price is None:
            return False, "Item not available."
        
        if player.gold < price:
            return False, "Not enough gold."
        
        player.add_to_inventory(item)
        player.adjust_gold(-price)
        return True, f"Bought {item.name} for {price} gold."

    def can_sell_item(self, item_key: str):
        """
        Checks if the shop can accept the item for sale.

        Parameters:
            item_key (str): The key representing the item name.
        
        Returns:
            bool: True if the shop can accept the item, False otherwise.
            str: The category of the item if accepted, None otherwise.
            int: The base price of the item if accepted, None otherwise.
        """
        for category, items in self.inventory.items():
            if item_key in items:
                price = self.prices[category].get(item_key)
                if price is not None:
                    return True, category, price
        return False, None, None
    
    def sell_item(self, player, item_key: str):
        """
        Allows the player to sell an item from their inventory to the shop at half its purchase price.

        Parameters:
            player (Player): The player selling the item.
            item_key (str): The key representing the item name.

        Returns:
            bool: True if the item was sold successfully, False otherwise.
            str: A message indicating the result of the sale.
        """
        item_data = player.get_inventory_item(item_key)
        if not item_data:
            return False, "Item not in inventory."
    
        item = item_data["item"]
        can_sell, category, base_price = self.can_sell_item(item_key)

        if not can_sell:
            return False, "This shop does not accept that item."
        
        sell_price = int(base_price * 0.5)
        player.remove_from_inventory(item_key)
        player.adjust_gold(sell_price)
        return True, f"Sold {item.name} for {sell_price} gold."

    # def display_inventory(self):
    #     """
    #     Display all items available in the shop along with their prices.

    #     Returns:
    #         item_mapping (dict): Mapping of item numbers to item keys and categories for selection.
    #     """
    #     print(f"\n{Formatter.white_bold('Here are the items for sale:')}")
    #     item_mapping = {}
    #     item_number = 1

    #     for category, category_items in self.inventory.items():
    #         print(f"\n{Formatter.yellow_bold(category.capitalize())}:")
    #         if not category_items:
    #             print(Formatter.yellow_bold("No items available in this category."))
    #         else:
    #             for item_key, item in category_items.items():
    #                 price = self.prices[category].get(item_key, "Price not set")
    #                 print(f"{Formatter.blue_bold(item_number)}. {Formatter.white_bold(item.name)} - {item.description} - {Formatter.yellow_bold(price)} gold")
    #                 item_mapping[item_number] = (category, item_key) # Map item number to category and key
    #                 item_number += 1
        
    #     return item_mapping
    
    # def enter_shop(self, player :object):
    #     """
    #     Handles player interaction with the shop.

    #     Parameters:
    #         player (Player): The player entering the shop.
    #     """
    #     print(f"\n {Formatter.location_name(f'Welcome to {self.name}!')}")
    #     while True:
    #         item_mapping = self.display_inventory()
            
    #         print(f"\n{Formatter.green_bold(player.name)}'s Gold: {Formatter.yellow_bold(player.gold)}")
    #         action = input(f"\nWould you like to ({Formatter.green_bold('B')})uy an item, ({Formatter.red_bold('S')})ell an item, or ({Formatter.yellow_bold('L')})eave the shop? --> ").lower()

    #         if action == "l": # Leave the shop
    #             print("Thank you for visiting the shop!")
    #             pause_clear_screen(3)
    #             break

    #         elif action == "b": # Buy an item
    #             try:
    #                 item_number = input(f"Enter the {Formatter.blue_bold('number')} of the {Formatter.white_bold('item')} you want to buy or '{Formatter.red_bold('back')}' to return: ")
    #                 if item_number == "back":
    #                     clear_screen()
    #                     continue

    #                 item_number = int(item_number)

    #                 if item_number not in item_mapping:
    #                     print(Formatter.yellow_bold("\nInvalid item number. Please select a valid item."))
    #                     pause_clear_screen(2)
    #                     continue

    #                 category, item_key = item_mapping[item_number]
    #                 self.buy_item(player, category, item_key)
    #                 continue_clear_screen()

    #             except ValueError:
    #                 print(Formatter.yellow_bold("\nInvalid input. Please enter a number."))
    #                 pause_clear_screen(2)
            
    #         elif action == "s": # Sell an item
    #             player.view_inventory()
    #             item_key = input(f"Enter the name of the {Formatter.white_bold('item')} you want to sell or '{Formatter.red_bold('back')}' to return: ").lower().replace(" ", "_")
    #             if item_key == "back":
    #                 clear_screen()
    #                 continue
    #             self.sell_item(player, item_key)
    #             pause_clear_screen()

    #         else:
    #             print(Formatter.yellow_bold("\nInvalid choice. Please select a valid option."))
    #             pause_clear_screen(2)
    #             continue

    # def buy_item(self, player : object, item_category : str, item_key : str):
    #     """
    #     Method that lets the player buy items from the shop.

    #     Parameters:
    #         player (Player): The player who is buying the item
    #         item_category (str): The category of the item (e.g. "weapons").
    #         item_key (str): The key representing the item name.
    #     """
    #     if item_category not in self.inventory:
    #         print(f"\n{Formatter.yellow_bold(f'Invalid category {item_category}. Please choose from weapons, armours, or potions.')}")
    #         return
    
    #     item = self.inventory[item_category].get(item_key)
    #     if not item:
    #         print(Formatter.yellow_bold("\nSorry this item is not available."))
    #         return
    
    #     price = self.prices[item_category].get(item_key, 0)
    #     if player.gold >= price:
    #         print(f"\n{Formatter.green_bold(player.name)} bought {Formatter.cyan_bold(item.name)} for {Formatter.yellow_bold(price)} gold.")
    #         player.add_to_inventory(item)
    #         player.adjust_gold(-price)
    #     else:
    #         print(Formatter.yellow_bold("\nNot enough gold for this item."))

    # def sell_item(self, player : object, item_key : str):
    #     """
    #     Allows the player to sell an item from their inventory to the shop at half its purchase price.
        
    #     Parameters:
    #         player (Player): The player selling the item.
    #         item_key (str): The key representing the item name.
    #     """
    #     item_data = player.get_inventory_item(item_key)
    #     if not item_data:
    #         print(Formatter.yellow_bold("\nYou don't have that item in your inventory."))
    #         return

    #     item = item_data["item"]
    #     for category, items in self.inventory.items():
    #         if item_key in items: # Check if the shop accepts the item
    #             base_price = self.prices[category].get(item_key)
    #             if base_price is not None:
    #                 sell_price = int(base_price * 0.5)
    #                 player.remove_from_inventory(item_key)
    #                 print(f"\n{Formatter.green_bold(player.name)} sold {Formatter.cyan_bold(item.name)} for {Formatter.yellow_bold(sell_price)} gold.")
    #                 player.adjust_gold(sell_price)
    #                 return
    #     print(Formatter.yellow_bold("\nThis shop does not accept that item."))