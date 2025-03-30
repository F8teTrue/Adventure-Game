import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HOVER_COLOR = (180, 180, 180)
GREY = (50, 50, 50)

class Button:
    """
    Represents an interactive button with hover effects.

    Parameters:
        text (str): The button label.
        font_size (int): Size of the text.
        x (int): X position of the button.
        y (int): Y position of the button.
        width (int): Button width.
        height (int): Button height.
        action (action): Action to execute when clicked.
    """
    def __init__(self, text, font_size, x, y, width, height, border_radius, action):
        self.text = text
        self.rect = pg.Rect(x, y, width, height)
        self.border_radius = border_radius
        self.action = action
        self.font = pg.font.Font(None, int(font_size))
        self.base_color = WHITE
        self.hover_color = HOVER_COLOR
        self.text_color = BLACK
        self.current_color = self.base_color

    def draw(self, screen):
        """Draws the button on the screen."""
        pg.draw.rect(screen, self.current_color, self.rect, border_radius = self.border_radius)
        pg.draw.rect(screen, GREY, self.rect, 3, border_radius = self.border_radius)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, disable_clicks):
        """Handles button clicks and hover effects."""
        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not disable_clicks:
                    if self.action:
                        self.action()
                        return True
        else:
            self.current_color = self.base_color
        return False

class CloseButton(Button):
    """
    A specialized button for closing UI popups.

    Parameters:
        x (int): X position of the button.
        y (int): Y position of the button.
        size (int): Button size.
        ui_manager (UIManager): The UI manager to handle closing.
    """
    def __init__(self, x, y, size, ui_manager):
        if ui_manager:
            action = lambda: ui_manager.close_ui()
        else:
            action = lambda: None

        super().__init__("X", size - 6, x, y, size, size, 10, action)
        self.ui_manager = ui_manager

    def update_position(self, x, y):
        """
        Updates the position of the close button.

        Parameters:
            x (int): New X position.
            y (int): New Y position.
        """
        self.rect.topleft = (x, y)
