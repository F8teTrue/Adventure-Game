import pygame as pg

class UIManager:
    """
    Manages multiple UI popups and ensures only one is active at a time.
    """
    def __init__(self, screen):
        self.screen = screen
        self.active_ui = None
    
    def open_ui(self, ui, player = None):
        """Open a UI popup and ensures only one is open at a time."""
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
            self.active_ui.visible = False
            self.active_ui = None
            # print("UIManager: UI closed, ready to open again.") # Debug 
    
    def handle_event(self, event):
        """Passes events to the active UI popup."""
        if self.active_ui:
            self.active_ui.handle_event(event, self)
    
    def draw(self):
        """Draws the active UI popup on the screen."""
        if self.active_ui:
            self.active_ui.draw()