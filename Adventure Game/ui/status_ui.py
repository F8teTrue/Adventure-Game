import pygame as pg
from ui.button import CloseButton

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_GREY = (30, 30, 30, 200)

class StatusUI:
    """
    Displays the player's status in a pop-up window.

    Parameters:
        screen (pygame.Surface): The game display surface.
        ui_manager (UIManager): The UI manager to handle opening/closing UIs.
    """
    def __init__(self, screen, ui_manager):
        self.screen = screen
        self.ui_manager = ui_manager
        self.font = pg.font.Font(None, 36)
        self.status_text = ""
        self.close_button = None
        self.is_open = False
        self.last_screen_size = screen.get_size()

    def toggle(self, player):
        """Toggles UI on/off using UIManager."""
        self.is_open = True
        self.status_text = (
            f"Name: {player.name}\n"
            f"Level: {player.level} ({player.xp}/{player.calculate_xp_needed()})\n"
            f"Health: {player.health}/{player.max_health}\n"
            f"Attack: {player.attack}\n"
            f"Defense: {player.base_defence}\n"
            f"Gold: {player.gold}"
        )
        self.create_close_button()

    def create_close_button(self):
        """Creates the close button."""
        popup_width, popup_height = 400, 250
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2
        button_size = 30
        button_x = popup_x + popup_width - button_size - 10
        button_y = popup_y + 10
        
        if self.close_button is None:
            self.close_button = CloseButton(button_x, button_y, button_size, self.ui_manager)
        else:
            self.close_button.update_position(button_x, button_y)

    def update_on_resize(self):
        """Updates button positions if screen size changes."""
        if self.screen.get_size() != self.last_screen_size:
            self.create_close_button()
            self.last_screen_size = self.screen.get_size()

    def handle_event(self, event, ui_manager):
        """Handles button clicks."""
        if self.close_button:
            if self.close_button.handle_event(event, disable_clicks=False):
                ui_manager.close_ui()

    def draw(self):
        """Draws the UI if it's active."""
        if not self.is_open:
            return

        self.update_on_resize()

        popup_width, popup_height = 400, 250
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        popup_surface = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
        popup_surface.fill((0, 0, 0, 0))
        pg.draw.rect(popup_surface, TRANSPARENT_GREY, (0, 0, popup_width, popup_height), border_radius=10)
        pg.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 3, border_radius=10)
        self.screen.blit(popup_surface, (popup_x, popup_y))

        y_offset = 15
        for line in self.status_text.split("\n"):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (popup_x + 20, popup_y + y_offset))
            y_offset += 40

        if self.close_button:
            self.close_button.draw(self.screen)
