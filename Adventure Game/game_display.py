import pygame as pg
import sys
from ui.ui_manager import UIManager
from ui.button import Button
from ui.status_ui import StatusUI


pg.init()

infoObject = pg.display.Info()
SCREEN_WIDTH = min(infoObject.current_w, 800)
SCREEN_HEIGHT = min(infoObject.current_h, 600)
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TRANSPARENT_GREY = (30, 30, 30, 200)

BACKGROUND_IMAGES = {
    "home": "Adventure Game/images/home_bg.webp",
    "village": "Adventure Game/images/village_bg.jpg",
    "exploration": "Adventure Game/images/exploration_bg.jpg",
    "quest hall": "Adventure Game/images/blocked.jpg"
}

UI_MAPPING = {
    "Check Status": "status_ui",
}

class GameDisplay:
    """
    Manages the main game window, UI elements, and transitions between screens.
    """
    def __init__(self):
        """Initializes the game window and starts the UI."""
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption("Adventure Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.fullscreen = False

        self.disable_clicks = False
        self.locations = None
        self.choice_box_height = 150
        self.buttons = []

        self.ui_manager = UIManager(self.screen)
        self.status_ui = StatusUI(self.screen, self.ui_manager)

    def initialize_game(self, player, locations):
        """Starts the main game after initialization."""
        self.player = player
        self.locations = locations
        self.current_location = self.locations["home"]
        self.update_background("home")
        self.update_ui()
        self.game_loop()

    def load_background(self, location_key):
        """Loads and scales the background image for the current location."""
        try:
            bg = pg.image.load(BACKGROUND_IMAGES.get(location_key, BACKGROUND_IMAGES["home"])).convert()
            return pg.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except pg.error:
            print(f"Error loading background for {location_key}")
            return None

    def update_background(self, location_name):
        """Updates the background image when the screen resizes or location changes."""
        location_name = location_name.lower()

        if location_name in BACKGROUND_IMAGES:
            self.current_background = self.load_background(location_name)
        else:
            print(f"No background found for {location_name}, using default.")
            self.current_background = self.load_background("home")  # Default to home background
 
    def update_ui(self):
        """Updates the buttons dynamically based on the current location."""
        self.buttons.clear()
        choices = self.current_location.choices

        button_width = self.current_location.ui_config["button_width"]
        button_height = self.current_location.ui_config["button_height"]
        button_spacing_x = self.current_location.ui_config["button_spacing_x"]
        button_spacing_y = self.current_location.ui_config["button_spacing_y"]
        columns = self.current_location.ui_config["columns"]

        start_x = (SCREEN_WIDTH - (columns * (button_width + button_spacing_x))) // 2
        start_y = SCREEN_HEIGHT - self.choice_box_height - 15

        for index, choice in enumerate(choices):
            row = index // columns
            col = index % columns
            x = start_x + col * (button_width + button_spacing_x)
            y = start_y + row * (button_height + button_spacing_y)

            # print(f"Creating button: {choice.description}") # Debug

            if choice.description in UI_MAPPING:
                ui_name = UI_MAPPING[choice.description]
                ui_instance = getattr(self, ui_name, None)
                # print(f"Mapping {choice.description} to UI: {ui_name}")  # Debug

                action = lambda ui = ui_instance, player = self.player: self.ui_manager.open_ui(ui, player)
            else:
                action = lambda ch = choice: self.handle_choice(ch)

            self.buttons.append(Button(choice.description, 48, x, y, button_width, button_height, 8,action))

    def handle_choice(self, choice):
        """Handles player choices and location changes dynamically."""
        self.disable_clicks = True

        # print(f"Handling choice: {choice.description}")  #Debug

        #UI Button Handling
        if choice.description in UI_MAPPING:
            ui_name = UI_MAPPING[choice.description]
            ui_instance = getattr(self, ui_name, None)

            # print(f"Opening UI: {ui_name}")  # Debug
            if ui_instance:
                self.ui_manager.open_ui(ui_instance, self.player)
                self.disable_clicks = False
            return

        # print(f"Executing choice: {choice.description}") # Debug

        result = choice.execute(self.locations)

        if isinstance(result, str) and result in self.locations:
            # print(f"Changing location to {result}...")  # Debug
            self.current_location = self.locations[result]
            self.update_background(self.current_location.name)
            self.update_ui()
            self.draw()

        pg.time.set_timer(pg.USEREVENT, 200)

    def draw(self):
        """Handles rendering all game elements on the screen."""
        self.screen.fill(BLACK)

        # Draw background
        if self.current_background:
            self.screen.blit(self.current_background, (0, 0))

        # Draw UI box at the bottom
        choice_box = pg.Surface((SCREEN_WIDTH, 190), pg.SRCALPHA)
        choice_box.fill(TRANSPARENT_GREY)
        self.screen.blit(choice_box, (0, SCREEN_HEIGHT - 190))

        # Draw buttons inside the choice box
        for button in self.buttons:
            button.draw(self.screen)
        
        self.ui_manager.draw()

        pg.display.flip()

    def game_loop(self):
        """Main game loop to update and render everything."""
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False

                elif event.type == pg.VIDEORESIZE:
                    global SCREEN_WIDTH, SCREEN_HEIGHT
                    SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
                    self.update_background(self.current_location.name)
                    self.update_ui()

                elif self.ui_manager.active_ui:
                    self.ui_manager.handle_event(event)
                    if not self.ui_manager.active_ui:
                        self.disable_clicks = False
                        self.update_ui()
                    continue

                elif event.type == pg.USEREVENT:
                    self.disable_clicks = False
                    continue

                for button in self.buttons:
                    button.handle_event(event, self.disable_clicks)

            self.draw()
            self.clock.tick(FPS)

        pg.quit()
        sys.exit()