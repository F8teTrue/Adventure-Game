import pygame as pg
from ui.button import Button, CloseButton
from items import Weapon, Armour, Potion

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
TRANSPARENT_GREY = (30, 30, 30, 200)
HOVER_COLOR = (180, 180, 180)

class InventoryUI:
    """
    A popup window displaying the players inventory categorized with tabs.
    Allows the player to use/equip items, and close the window.

    Parameters:
        screen (pg.Surface): The main game screen.
        ui_manager (UIManager): The UI manager for handling UI elements.
        player (Player): The player object.
    """
    def __init__(self, screen, ui_manager, player):
        self.screen = screen
        self.ui_manager = ui_manager
        self.player = player

        self.font = pg.font.Font(None, 28)
        self.is_open = False
        self.active_tab = "Weapons"
        self.close_button = None
        self.tab_buttons = []
        self.item_buttons = []
        self.item_detail_popup = None


        self.last_screen_size = screen.get_size()

        self.popup_width = screen.get_width() * 0.65
        self.popup_height = screen.get_height() * 0.6
        self.popup_x = (screen.get_width() - self.popup_width) // 2
        self.popup_y = (screen.get_height() - self.popup_height - 100) // 2

    def toggle(self, player):
        """Opens the inventory UI."""
        self.is_open = True
        self.player = player
        self.active_tab = "Weapons"
        self.update_layout()

    def update_layout(self):
        """Updates the layout on resize or toggle."""
        self.popup_width = self.screen.get_width() * 0.65
        self.popup_height = self.screen.get_height() * 0.6
        self.popup_x = (self.screen.get_width() - self.popup_width) // 2
        self.popup_y = (self.screen.get_height() - self.popup_height - 100) // 2

        button_size = 30
        button_x = self.popup_x + self.popup_width - button_size - 10
        button_y = self.popup_y + 10
        self.close_button = CloseButton(button_x, button_y, button_size, self.ui_manager)

        self.tab_buttons = []
        tabs = ["Weapons", "Armours", "Potions", "Misc"]
        tab_width = (self.popup_width / len(tabs)) - 10
        total_width = tab_width * len(tabs) + 8 * (len(tabs) - 1)
        start_x = self.popup_x + (self.popup_width - total_width) // 2 

        for i, tab in enumerate(tabs):
            x = start_x + i * (tab_width + 8)
            y = self.popup_y + 50
            tab_button = Button(
                text = tab,
                font_size = 24,
                x = x,
                y = y,
                width = tab_width,
                height = 35,
                border_radius = 6,
                action = lambda tab = tab: self.switch_tab(tab),
            )
            self.tab_buttons.append(tab_button)
        
        self.generate_item_buttons()
    
    def switch_tab(self, tab_name):
        """
        Switches the active tab.
        
        Parameters:
            tab_name (str): The name of the tab to switch to.
        """
        self.active_tab = tab_name
        self.generate_item_buttons()

    def generate_item_buttons(self):
        """Create buttons to display items in the current tab."""
        self.item_buttons = []
        categories = self.player.categorise_inventory()
        items = categories.get(self.active_tab, [])

        x = self.popup_x + 30
        y = self.popup_y + 100
        button_width = self.popup_width - 60
        button_height = 40
        spacing = 10

        for item, quantity in items:
            label = f"{item.name}"
            if quantity > 1:
                label += f" x{quantity}"
            if item == self.player.weapon or item == self.player.armour:
                label += " (Equipped)"
            
            btn = Button(label, 24, x, y, button_width, button_height, 6,  lambda i=item: self.on_item_click(i))
            self.item_buttons.append(btn)
            y += button_height + spacing

    def on_item_click(self, item):
        """Opens item detail popup."""
        self.item_detail_popup = ItemDetailPopup(self.screen, item, self.player)
        self.item_detail_popup.parent_ui = self

    def close_item_popup(self):
        """Closes the item detail popup."""
        self.item_detail_popup = None
        self.generate_item_buttons()
    
    def handle_event(self, event, ui_manager):
        """Handle events for the inventory UI."""
        if self.screen.get_size() != self.last_screen_size:
            self.update_layout()
            if self.item_detail_popup:
                self.item_detail_popup.update_layout() 
            self.last_screen_size = self.screen.get_size()
        
        if self.item_detail_popup:
            self.item_detail_popup.handle_event(event)
            return
        
        if self.close_button:
            if self.close_button.handle_event(event, disable_clicks = False):
                ui_manager.close_ui()
        
        for button in self.tab_buttons + self.item_buttons:
            button.handle_event(event, disable_clicks = False)

    
    def draw(self):
        """"Draw the inventory UI."""
        if not self.is_open:
            return

        popup_surface = pg.Surface((self.popup_width, self.popup_height), pg.SRCALPHA)
        popup_surface.fill((0, 0, 0, 0))
        pg.draw.rect(popup_surface, TRANSPARENT_GREY, (0, 0, self.popup_width, self.popup_height), border_radius = 10)
        pg.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 3, border_radius = 10)
        self.screen.blit(popup_surface, (self.popup_x, self.popup_y))

        title_font = pg.font.Font(None, int(self.popup_width * 0.05))  # ← CHANGED (title feature)
        title_text = title_font.render("Inventory", True, WHITE)
        title_rect = title_text.get_rect(center=(self.popup_x + self.popup_width // 2, self.popup_y + 25))
        self.screen.blit(title_text, title_rect)

        for button in self.tab_buttons + self.item_buttons:
            button.draw(self.screen)
        if self.close_button:
            self.close_button.draw(self.screen)
        
        if self.item_detail_popup:
            self.item_detail_popup.draw()
        
class ItemDetailPopup:
    """
    Class for displaying item details in a popup window.

    Parameters:
        screen (pg.Surface): The main game screen.
        item (Item): The item to display.
        player (Player): The player object.
        close_callback (function): Function to call when the popup should close.
    """
    def __init__(self, screen, item, player,):
        self.screen = screen
        self.item = item
        self.player = player
        self.font = pg.font.Font(None, 28)

        self.parent_ui = None
        self.update_layout()
    
    def update_layout(self):
        """Update the layout of the popup based on screen size."""
        screen_width, screen_height = self.screen.get_size()
        self.width = screen_width * 0.35
        self.height = screen_height * 0.3
        self.x = (screen_width - self.width) // 2
        self.y = (screen_height - self.height) // 2

        self.setup_buttons()

        close_size = 30
        self.close_button = CloseButton(
            self.x + self.width - close_size - 8,
            self.y + 8,
            close_size,
            None 
        )
    
    def setup_buttons(self):
        """Setup buttons for the popup."""
        self.buttons = []
        y_offset = self.y + self.height - 60
        button_width = self.width - 40
        button_height = 35

        item = self.item
        label = None
        if isinstance(item, Weapon):
            label = "Unequip" if self.player.weapon == item else "Equip"
        elif isinstance(item, Armour):
            label = "Unequip" if self.player.armour == item else "Equip"
        elif isinstance(item, Potion):
            label = "Use"
        
        if label:
            if label == "Equip" or label == "Use":
                self.buttons.append(Button(label, 24, self.x + 20, y_offset, button_width, button_height, 6, lambda: self.use_item(item)))
            elif label == "Unequip":
                self.buttons.append(Button(label, 24, self.x + 20, y_offset, button_width, button_height, 6, lambda: self.unequip_item(item)))
        else:
            self.buttons.append(Button("This item can't be used or equipped.", 24, self.x + 20, y_offset, button_width, button_height, 6, None))

    def use_item(self, item):
        """Use or equip the selected item."""
        item_key = item.name.lower().replace(" ", "_")
        self.player.use_item(item_key)
        self.close_popup()
    
    def unequip_item(self, item):
        """Unequip the selected item."""
        item_key = item.name.lower().replace(" ", "_")
        self.player.unequip_item(item_key)
        self.close_popup()

    def close_popup(self):
        self.parent_ui.item_detail_popup = None
        self.parent_ui.generate_item_buttons()

    def handle_event(self, event):
        """Handle events for the item detail popup."""
        if event.type == pg.VIDEORESIZE:
            self.update_layout()
            self.setup_buttons()

        if self.close_button.handle_event(event, disable_clicks=False):
            self.close_popup()

        for button in self.buttons:
            button.handle_event(event, disable_clicks=False)

    def draw(self):
        """Draw the item detail popup."""
        surf = pg.Surface((self.width, self.height), pg.SRCALPHA)
        pg.draw.rect(surf, (30, 30, 30, 220), (0, 0, self.width, self.height), border_radius=10)
        pg.draw.rect(surf, WHITE, surf.get_rect(), 2, border_radius=10)
        self.screen.blit(surf, (self.x, self.y))

        title_font = pg.font.Font(None, 32)
        title = title_font.render(self.item.name, True, WHITE)
        self.screen.blit(title, (self.x + 20, self.y + 20))

        desc_font = pg.font.Font(None, 24)
        description = getattr(self.item, "description", "No description available.")
        y_text = self.y + 60
        for line in description.split("\n"):
            rendered = desc_font.render(line, True, WHITE)
            self.screen.blit(rendered, (self.x + 20, y_text))
            y_text += 26

        for button in self.buttons:
            button.draw(self.screen)

        self.close_button.draw(self.screen)
