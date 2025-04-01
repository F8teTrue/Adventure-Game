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
    
    def update_popup_size(self):
        """Updates popup size based on screen dimensions."""
        screen_width, screen_height = self.screen.get_size()
        self.popup_width = int(screen_width * 0.25)
        self.popup_height = int(screen_height * 0.3)
        self.popup_x = (self.screen.get_width() - self.popup_width) // 2
        self.popup_y = (self.screen.get_height() - self.popup_height) // 2

    def toggle(self, player):
        """Opens the status UI."""
        self.is_open = True
        self.status_text = (
            f"Name: {player.name}\n"
            f"Level: {player.level} ({player.xp}/{player.calculate_xp_needed()})\n"
            f"Health: {player.health}/{player.max_health}\n"
            f"Attack: {player.base_attack}\n"
            f"Defense: {player.base_defence}\n"
            f"Gold: {player.gold}"
        )
        self.update_popup_size()
        self.create_close_button(force_update = True)

    def create_close_button(self, force_update = False):
        """Creates or updates the close button position based on popup size."""
        button_size = 30
        button_x = self.popup_x + self.popup_width - button_size - 8
        button_y = self.popup_y + 8

        if self.close_button is None or force_update:
            self.close_button = CloseButton(button_x, button_y, button_size, self.ui_manager)
        else:
            self.close_button.update_position(button_x, button_y)

    def update_on_resize(self):
        """Updates UI elements when the screen is resized."""
        if self.screen.get_size() != self.last_screen_size:
            self.update_popup_size()
            self.create_close_button(force_update = True)
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

        screen_width, screen_height = self.screen.get_size()
        popup_width = int(screen_width * 0.25)
        popup_height = int(screen_height * 0.3)
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2


        popup_surface = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
        popup_surface.fill((0, 0, 0, 0))
        pg.draw.rect(popup_surface, TRANSPARENT_GREY, (0, 0, popup_width, popup_height), border_radius=10)
        pg.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 3, border_radius=10)
        self.screen.blit(popup_surface, (popup_x, popup_y))

        font_size = int(screen_width * 0.025)
        self.font = pg.font.Font(None, font_size)

        y_offset = font_size * 0.45
        for line in self.status_text.split("\n"):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (popup_x + int(screen_width * 0.02), popup_y + y_offset))
            y_offset += font_size * 0.9

        if self.close_button:
            self.close_button.draw(self.screen)
