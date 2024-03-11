import arcade, os, random, math

# Defining constants

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

# Window Settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Ataraxia V1"

# Sprite Scaling
CHARACTER_SCALING = 1
TILE_SCALING = 1

# Sprite facing direction
RIGHT_FACING = 0
LEFT_FACING = 1

# Layer names


# Loading mirrored sprites
def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

# Entity superclass
class Entity(arcade.Sprite):
    """Overarching things for characters"""

    def __init__(self, category_folder, sprite_folder):
        super().__init__()

        # Default right facing
        self.facing_direction = RIGHT_FACING

        # Image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        main_path = f"{MAIN_PATH}/assets/{category_folder}/{sprite_folder}"


        self.idle_textures = []
        for i in range(2):
            texture = load_texture_pair(f"{main_path}/idle/{i}.png")
            self.idle_textures.append(texture)



# Actual Game
class GameView(arcade.View):
    """
    All of the game stuff
    """

    def __init__(self):

        # Set up window with parent class (arcade.View)
        super().__init__()

        self.window.set_mouse_visible = False


        # Variables to check which key is being pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Tilemap object
        self.tile_map = None

        # Scene object
        self.scene = None

        # Player sprite variable
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Camera for GUI elements (Secondary camera)
        self.gui_camera = None

        # Level setup
        self.level = 0

        # Primary camera for scrolling the screen
        self.camera = None

    def setup(self):
        """Game setup which runs each time game is restarted."""

        # Setup camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Setup GUI camera
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Map name
        map_name = f"{MAIN_PATH}/maps/{self.level}.tmx"

        # Layer specific options for Tilemap
        layer_options = {

        }

        # Read in Tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Setup player at specific coordinates
        self.player_sprite = PlayerCharacter()


# Main Program

def main():
    """Main Function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)
    start_view = GameView()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()

# Things that run

if __name__ == "__main__":
    main()