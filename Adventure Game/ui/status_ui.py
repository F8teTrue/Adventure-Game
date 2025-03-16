import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (180, 180, 180)
TRANSPARENT_GREY = (30, 30, 30, 200)

class StatusUI:
    """
    Displays the player's status in a pop-up window.
    """
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 36)
        self.visible = False
        self.status_text = ""
        self.close_button = None
        self.close_button_hover = False
    
    def toggle(self, player):
        """Toggles the status UI on/off."""
        self.visible = not self.visible
        if self.visible:
            # print("StatusUI: Opened")  # Debug
            self.status_text = (
                f"Name: {player.name}\n"
                f"Level: {player.level} ({player.xp}/{player.calculate_xp_needed()})\n"
                f"Health: {player.health}/{player.max_health}\n"
                f"Attack: {player.attack}\n"
                f"Defense: {player.base_defence}\n"
                f"Gold: {player.gold}"
            )
            self.create_close_button()
        else:
            # print("StatusUI: Closed") # Debug 
            self.close_button = None 

    def create_close_button(self):
        """Creates the close button."""
        popup_width, popup_height = 400, 250
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2
        button_size = 30
        button_x = popup_x + popup_width - button_size - 10
        button_y = popup_y + 10

        self.close_button = pg.Rect(button_x, button_y, button_size, button_size)
    
    def handle_event(self, event, ui_manager):
        """Handles mouse click events for the close button."""
        mouse_pos = pg.mouse.get_pos()

        if self.close_button and self.close_button.collidepoint(mouse_pos):
            self.close_button_hover = True
        else:
            self.close_button_hover = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.close_button and self.close_button.collidepoint(mouse_pos):
                # print("StatusUI: Close button clicked") # Debug
                ui_manager.close_ui()


    def draw(self):
        """Draws the status UI on the screen if visible."""
        if not self.visible:
            return
        
        self.create_close_button()

        popup_width, popup_height = 400, 250
        popup_x = (self.screen.get_width() - popup_width) // 2
        popup_y = (self.screen.get_height() - popup_height) // 2

        popup_surface = pg.Surface((popup_width, popup_height), pg.SRCALPHA)
        popup_surface.fill((0, 0, 0, 0))
        pg.draw.rect(popup_surface, TRANSPARENT_GREY, (0, 0, popup_width, popup_height), border_radius=10)
        pg.draw.rect(popup_surface, WHITE, popup_surface.get_rect(), 3, border_radius = 10)

        self.screen.blit(popup_surface, (popup_x, popup_y))

        y_offset = 15
        for line in self.status_text.split("\n"):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (popup_x + 20, popup_y + y_offset))
            y_offset += 40

        if self.close_button:
            button_color = WHITE if not self.close_button_hover else HOVER_COLOR
            pg.draw.rect(self.screen, button_color, self.close_button, border_radius=8)
            text_surface = self.font.render("X", True, BLACK)
            text_rect = text_surface.get_rect(center=self.close_button.center)
            self.screen.blit(text_surface, text_rect)

