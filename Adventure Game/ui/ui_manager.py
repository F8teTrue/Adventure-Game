import pygame as pg

class UIManager:
    """
    Manages multiple UI popups and makes sure only 1 is active at a time.

    Parameters:
        screen (pygame.Surface): The game display surface.
    """
    def __init__(self, screen):
        self.screen = screen
        self.active_ui = None
    
    def open_ui(self, ui, player = None):
        """
        Open a UI popup and makes sure only one is open at a time.

        Parameters:
            ui (object): The UI popup object to open.
            player (object, optional): The player object to pass to the UI popup.
        """
        if self.active_ui:
            return
        
        # print(f"UIManager: Opening {ui.__class__.__name__}")  # Debug
        
        self.active_ui = ui
        if player:
            self.active_ui.toggle(player)
    
    def close_ui(self):
        """Closes the current UI popup."""
        if self.active_ui:
            # print(f"UIManager: Closing {self.active_ui.__class__.__name__}") # Debug
            self.active_ui.is_open = False
            self.active_ui = None
            # print("UIManager: UI closed, ready to open again.") # Debug 
    
    def toggle_ui(self, ui, player = None):
        """
        Toggles the UI window on or off.

        Parameters:
            ui (object): The UI popup object to toggle.
            player (object, optional): The player object (if needed for UI data).
        """
        if self.active_ui:
            self.close_ui()
        else:
            self.open_ui(ui, player)
    
    def handle_event(self, event):
        """
        Passes events to the active UI popup.

        Parameters:
            event (pygame.event): The Pygame event to process.
        """
        if self.active_ui:
            self.active_ui.handle_event(event, self)
    
    def draw(self):
        """Draws the active UI popup on the screen."""
        if self.active_ui:
            self.active_ui.draw()