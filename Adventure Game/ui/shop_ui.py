import pygame as pg
from ui.button import Button, CloseButton

WHITE = (255, 255, 255)
TRANSPARENT_GREY = (30, 30, 30, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)

class ShopUI:
    """
    
    """
    def __init__(self, screen, ui_manager, shop, player):
        self.screen = screen
        self.ui_manager = ui_manager
        self.shop = shop
        self.player = player

        self.is_open = False
        self.active_tab = "weapons"
        self.item_buttons = []
        self.tab_buttons = []
        self.close_button = None
        self.font = pg.font.Font(None, 28)
        self.item_popup = None


        self.last_screen_size = self.screen.get_size()
    
    def set_shop(self, shop):
        """Sets the shop for the UI and updates the layout."""
        self.shop = shop
        self.update_layout()


    def toggle(self, player = None):
        """
        Toggles the shop UI open or closed.
        
        Parameters:
            player (Player): The player object to interact with the shop.
        """
        if not self.shop:
            print("[ShopUI] No shop set! Aborting toggle.")
            return
        self.is_open = True
        self.player = player
        self.update_layout()
        
    def update_layout(self):
        """
        
        """
        screen_width, screen_height = self.screen.get_size()
        self.popup_width = screen_width * 0.7
        self.popup_height = screen_height * 0.65
        self.popup_x = (screen_width - self.popup_width) // 2
        self.popup_y = (screen_height - self.popup_height) // 2

        self.button_width = self.popup_width - 60
        self.button_height  = 45
        self.spacing = 10

        self.close_button = CloseButton(
            self.popup_x + self.popup_width - 40,
            self.popup_y + 10,
            30,
            self.ui_manager
        )

        # Tabs
        self.tab_buttons = []
        categories = ["weapons", "armours", "potions"]
        tab_width = self.popup_width // len(categories) - 20
        for i, category in enumerate(categories):
            x = self.popup_x + 20 + i * (tab_width + 10)
            y = self.popup_y + 60
            self.tab_buttons.append(
                Button(
                    category.capitalize(), 
                    28,
                    x, 
                    y, 
                    tab_width, 
                    35, 
                    6,
                    lambda c = category: self.switch_tab(c)
                )
            )
        
        self.generate_item_buttons()

    def switch_tab(self, category):
        """
        Switches the active tab in the shop UI.

        Parameters:
            category (str): The category to switch to.
        """
        self.active_tab = category
        self.generate_item_buttons()

    def generate_item_buttons(self):
        """
        Generates item buttons based on the active tab.
        """
        self.item_buttons = []
        if not self.shop:
            return 
        items = self.shop.get_items_by_category(self.active_tab)

        x = self.popup_x + 30
        y = self.popup_y + 110

        for item_key, item in items:
            label = f"{item.name} - {item.description} ({self.shop.get_item_price(self.active_tab, item_key)} gold)"
            buy_action = lambda key=item_key, item=item: self.open_item_popup(item, key)

            self.item_buttons.append(
                Button(
                    label,
                    26,
                    x,
                    y,
                    self.button_width,
                    self.button_height,
                    6,
                    buy_action
                )
            )
            y += self.button_height + self.spacing
    
    def open_item_popup(self, item, item_key):
        """Opens a confirmation popup before buying."""
        price = self.shop.get_item_price(self.active_tab, item_key)

        def confirm():
            success, message = self.shop.buy_item(self.player, self.active_tab, item_key)
            self.item_popup.feedback_text = message
            self.item_popup.update_gold()
            self.generate_item_buttons()

        def cancel():
            self.item_popup = None

        self.item_popup = ShopItemPopup(self.screen, item, price, self.player, confirm, cancel)

    
    def buy_item(self, category, item_key):
        """
        Handles the purchase of an item.

        Parameters:
            category (str): The category of the item.
            item_key (str): The key of the item to buy.
        """
        success, message = self.shop.buy_item(self.player, category, item_key)
        print(message)
        self.generate_item_buttons()
    
    def handle_event(self, event, ui_manager):
        """
        Handles events for the shop UI.

        Parameters:
            event (pygame.event.Event): The event to handle.
            ui_manager (UIManager): The UI manager to handle events.
        """
        if self.screen.get_size() != self.last_screen_size:
            self.update_layout()
            self.last_screen_size = self.screen.get_size()
        
        if self.item_popup:
            self.item_popup.handle_event(event)
            return

        if self.close_button and self.close_button.handle_event(event, False):
            ui_manager.close_ui()

        for button in self.tab_buttons + self.item_buttons:
            button.handle_event(event, False)
    
    def draw(self):
        """
        Draws the shop UI on the screen if it's open.
        """
        if not self.is_open or not self.shop:
            return

        # Draw popup background
        popup_surface = pg.Surface((self.popup_width, self.popup_height), pg.SRCALPHA)
        popup_surface.fill((0, 0, 0, 0))
        pg.draw.rect(popup_surface, TRANSPARENT_GREY, (0, 0, self.popup_width, self.popup_height), border_radius=10)
        pg.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 3, border_radius=10)
        self.screen.blit(popup_surface, (self.popup_x, self.popup_y))

        # Draw title
        title_font = pg.font.Font(None, int(self.popup_width * 0.05))
        title_text = title_font.render(self.shop.name, True, WHITE)
        title_rect = title_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 30))
        self.screen.blit(title_text, title_rect)

        # Draw player gold
        gold_text = self.font.render(f"Gold: {self.player.gold}", True, YELLOW)
        self.screen.blit(gold_text, (self.popup_x + self.popup_width - 150, self.popup_y + 70))

        for button in self.tab_buttons + self.item_buttons:
            button.draw(self.screen)

        self.close_button.draw(self.screen)

        if self.item_popup:
            self.item_popup.draw()


class ShopItemPopup:
    """
    
    """
    def __init__(self, screen, item, price, player, confirm_callback, cancel_callback):
        self.screen = screen
        self.item = item
        self.price = price
        self.player = player
        self.confirm_callback = confirm_callback
        self.cancel_callback = cancel_callback
        self.font = pg.font.Font(None, 28)
        self.gold = self.player.gold
        self.feedback_text = ""

        self.update_layout()

    def update_layout(self):
        screen_width, screen_height = self.screen.get_size()
        self.width = screen_width * 0.45
        self.height = screen_height * 0.4
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

        button_width = (self.width - 3 * 20) // 2
        button_height = 40
        y_offset = self.y + self.height - button_height - 20

        # Confirm (Buy)
        self.confirm_button = Button(
            "Buy",
            28,
            self.x + 20,
            y_offset,
            button_width,
            button_height,
            6,
            self.confirm_callback if self.player.gold >= self.price else None
        )

        # Cancel
        self.cancel_button = Button(
            "Cancel",
            28,
            self.x + 20 + button_width + 20,  # space between
            y_offset,
            button_width,
            button_height,
            6,
            self.cancel_callback
        )
    
    def update_gold(self):
        """Updates the players available gold in the popup."""
        self.gold = self.player.gold
    
    def handle_event(self, event):
        """
        Handles events for the item popup.

        Parameters:
            event (pygame.event.Event): The event to handle.
        """
        self.confirm_button.handle_event(event, False)
        self.cancel_button.handle_event(event, False)
    
    def draw(self):
        """Draw the shop popup UI."""
        surface = pg.Surface((self.width, self.height), pg.SRCALPHA)
        pg.draw.rect(surface, (30, 30, 30, 230), (0, 0, self.width, self.height), border_radius = 10)
        pg.draw.rect(surface, WHITE, surface.get_rect(), 2, border_radius = 10)
        self.screen.blit(surface, (self.x, self.y))

        title_font = pg.font.Font(None, 32)
        title = title_font.render(self.item.name, True, WHITE)
        self.screen.blit(title, (self.x + 20, self.y + 20))

        desc_font = pg.font.Font(None, 28)
        lines = getattr(self.item, "description", "No description").split("\n")
        y_text = self.y + 60
        for line in lines:
            self.screen.blit(desc_font.render(line, True, WHITE), (self.x + 20, y_text))
            y_text += 24

        gold_text = self.font.render(f"Price: {self.price} gold", True, WHITE)
        player_gold = self.font.render(f"Your Gold: {self.player.gold}", True, YELLOW)
        self.screen.blit(gold_text, (self.x + 20, y_text + 10))
        self.screen.blit(player_gold, (self.x + 20, y_text + 35))

        if self.feedback_text:
            feedback_color = YELLOW if "not enough" not in self.feedback_text.lower() else (255, 100, 100)
            feedback_render = self.font.render(self.feedback_text, True, feedback_color)
            self.screen.blit(feedback_render, (self.x + 20, y_text + 65))

        self.confirm_button.draw(self.screen)
        self.cancel_button.draw(self.screen)