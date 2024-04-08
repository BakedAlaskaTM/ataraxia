# Quick note:
# Try-Excepts are used in this program to prevent
# errors, where if an error occurs the layer must not exist
# in the scene, and all code relating to it can be ignored.

# Import all modules/libraries required to run the code.
import arcade, os, math

# Defining constants
# This specifies the absolute path to the game folder on the user's
# machine. This will prevent any path errors caused by using relative
# paths.
MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

# Window Settings
# Constants that store window dimensions and window name.
# ONE_BLOCK refers to cases where a distance of one ingame block is
# needed.
# HALF_BLOCK is the same concept but when half a block is needed,
# or half of a full length.
# INTERACT_TEXT_POS refers to the percentage along the screen the
# "Can interact" text should be placed. 
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Ataraxia"
HALF_BLOCK = 0.5
ONE_BLOCK = 1
INTERACT_TEXT_POS = 0.8

# Colours
# These constants store the various colours needed in the game.
# These include uses such as background colour and text colour.
# MAX_OPACITY is used as a standard to adjust the opacity of certain
# tiles based on distance later.
SKY_BLUE = (99, 245, 255)
STONE_GREY = (158, 158, 158)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MENU_BACKGROUND = (188, 188, 255)
MAX_OPACITY = 255

# Font sizes
# These constants store the font of the various texts that are drawn
# on the screen.
# CHAR_WIDTH refers to the approximate width of each character in the
# font range 14-18
TIPS_FONT = 14
DIALOGUE_FONT = 15
INTERACT_FONT = 18
QUEST_FONT = 20
CHAR_WIDTH = 10

# Background rectangle sizes
# These constants determine the dimensions and features of the
# background rectangles behind the popup texts.
# The purpose of these rectangles is to improve contrast and thus
# readability between the text and the background, by applying a solid
# directly contrasting background colour behind the text.
# RECT_HEIGHT is the height of the rectangle which can fit one line
# of text.
# INTERACT_Y_OFFSET is the y-position of the "can interact" text and
# the background rectangle behind it.
# QUEST_OFFSET is the distance (in tiles) from the right edge and
# top edge of the screen respectively of the first line of quest 
# criteria.
# QUEST_Y_GAP is the distance (in tiles) between each quest criteria
# line.
RECT_HEIGHT = 25
QUEST_RECT_HEIGHT = 30
QUEST_COMPLETE_RECT_WIDTH = 280
QUEST_INCOMPLETE_RECT_WIDTH = 380
KEY_MISSING_RECT_WIDTH = 125
SECRET_FOUND_RECT_WIDTH = 125
INTERACT_RECT_WIDTH = 200
INTERACT_Y_OFFSET = 50
QUEST_RECT_WIDTH = 250
QUEST_OFFSET = [24, 60]
QUEST_Y_GAP = 9

# Sprite Scaling
# These constants scale the various sprites in the game,
# such as characters (player, enemies, villagers),
# tiles, collectibles (quest items, orbs, keys),
# and the knife sprite in particular.
CHARACTER_SCALING = 5
TILE_SCALING = 5
COLLECTIBLE_SCALING = 2
KNIFE_SCALING = 3

# Sprite facing direction
# These sprites are used to determine the facing direction of the
# sprites.
# The specific numbers are the indices of the list returned by the 
# load_texture_pair function, which returns the original image
# (usually right-facing) first, and the mirrored image second.
RIGHT_FACING = 0
LEFT_FACING = 1

# Sprite animation multipliers
# These determine how many frames it takes to update the texture once
# for each sprite and animation specified in the dictionary.
ANIM_MULT = {
    "Player1": {
        "Idle": 8,
        "Walk": 4,
        "Climb": 4,
        "Death": 6
    },
    "Player2": {
        "Idle": 8,
        "Walk": 4,
        "Death": 6
    },
    "Player3": {
        "Idle": 4,
        "Walk": 4,
        "Jump": 4,
        "Fall": 4,
        "Death": 6
    },
    "Orb": {
        "Idle": 12,
    },
    "Enemy": {
        "Walk": 2
    },
    "Knife": {
        "Idle": 3
    }
}

# Miscellaneous Constants
# These are extra constants that don't really fit under the other
# categories.
# FIRST_TEXTURE is used when the first texture in an animation is
# needed. 
# UNIT_INCREMENT is used when incrementing a variable by 1, whether
# it be updating a counter, increasing inventory, or decreasing stats.
# FIRST_VALUE is similar to FIRST_TEXTURE except that it's a more
# general "initial value", such as when resetting a counter or
# accessing the first index of a non-texture list.
# INDEX_OFFSET is the conversion for list indices (0, 1, 2) to counting
# indices (1, 2, 3).
# FRAMERATE is the framerate that we want the game to run at,
# and CAMERA_TRACK_SPEED is the speed at which the camera should center
# on the player when the player moves (pixels/sec).
# NOTHING is the most versatile constant. It can mean "nothing",
# "none", "empty", or 0 in a timer.
FIRST_TEXTURE = 0
UNIT_INCREMENT = 1
FIRST_VALUE = 0
INDEX_OFFSET = 1
FRAMERATE = 1 / 60
CAMERA_TRACK_SPEED = 0.2
NOTHING = 0

# Level categories
# These constants place the levels and sublevels into two categories.
# These are used to determine the background colour of the level.
GROUND_LEVELS = ["1.1", "3.1"]
CAVE_LEVELS = ["2.1", "2.2"]

# Layer names
# Character Layers
# Fairly self explanatory.
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_VILLAGERS = "Villagers"
LAYER_NAME_ENEMIES = "Enemies"

# Object Layers
# These are the physical objects that are defined as objects in Tiled
# or are created within the program.
LAYER_NAME_ORBS = "Orbs"
LAYER_NAME_TEXT = "Text"
LAYER_NAME_COLLECTIBLES = "Collectibles"
LAYER_NAME_WARP_DOORS = "Warp Doors"
LAYER_NAME_LOCKED_DOORS = "Locked Doors"
LAYER_NAME_KNIFE = "Knife"
LAYER_NAME_GOAL = "Goal"

# Tile Layers
# These are the names of the tile layers that are read directly
# from the Tiled map files.
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_STATUES = "Statues"
LAYER_NAME_SPAWNPOINT = "Current Statue"
LAYER_NAME_CAVE = "Cave"
LAYER_NAME_DEATH = "Death"
LAYER_NAME_DOOR_BARRIERS_OPEN = "Door Barrier Open"
LAYER_NAME_DOOR_BARRIERS_CLOSED = "Door Barrier Closed"

# GUI Layers
# These are the layers which are added to the GUI scene,
# which is drawn separately from the game scene.
# These are used for the energy and health bars respectively.
LAYER_NAME_ENERGY = "Energy"
LAYER_NAME_HEALTH = "Health"

# GUI Layer info
# These specify the position of the energy and health bars relative
# to the top right corner of the screen (in tiles).
ENERGY_BAR_OFFSET = [32, 48]
HEALTH_BAR_OFFSET = [32, 27]

# Physics things
# Most are quite self-explanatory.
# PLAYER_THRUST is the flight speed of the flying player character.
# GROUND_DISTANCE is the maximum distance (in pixels) the ground can be
# from the player before they can jump.
# GRAV_MULT is the downwards acceleration multiplier of the flying
# player shape. This has been determined experimentally from playtest.
GRAVITY = 1
PLAYER_WALK_SPEED = 10
PLAYER_RUN_SPEED = 15
PLAYER_JUMP_SPEED = 20
PLAYER_THRUST = 10
GROUND_DISTANCE = 10
GRAV_MULT = 4

# Player spawnpoints
# This is where the player spawns at the start of the first level.
PLAYER_START_X = 3
PLAYER_START_Y = 18

# Player characteristics
# These are the traits of the player such as the shape,
# max health, and max energy.
PLAYER_SHAPE_HUMAN = 0
PLAYER_SHAPE_DOG = 1
PLAYER_SHAPE_BLAZE = 2
MAX_HEALTH = 3
MAX_ENERGY = 3

# Enemy characteristics
# These are the moving speeds of the enemies split by type.
WRAITH_SPEED = 5
BIRD_SPEED = 20

# Kinematic constants
# Pretty self-explanatory,
# START_CLIMB is the minimum vertical speed before the player
# starts doing the climbing animation and physics when on a ladder.
STATIONARY = 0
START_CLIMB = 1
X_POS = 0
Y_POS = 1
ORIGIN = [0, 0]

# Timing constants
# These constants determine the amount of time something occurs.
# These may be cooldowns or text popups.
KNIFE_COOLDOWN = 0.5
HIT_COOLDOWN = 1
QUEST_INCOMPLETE_TIME = 2
QUEST_COMPLETE_TIME = 2
MISSING_KEY_TIME = 2
SECRET_FOUND_TIME = 2

# Sensing constants
# These constants are the maximum distance at which interactions can
# occur, or things are revealed.
# CAVE_TRNSPT_DIST means the distance at which cave blocks become fully
# transparent.
MIN_STATUE_DIST = 2
CAVE_REVEAL_DIST = 10
CAVE_TRNSPT_DIST = 5

# Volume constants
MUSIC_VOLUME = 0.3

# Dictionary References
# QUEST_REF is the dictionary which stores all of the quest information
# corresponding to each villager id.
# Each nested dictionary contains the quest dialogue, the amount of
# time it displays for, the item and quantity required, and the
# item and quantity of the reward.
# The string concatenation is used to keep line length within standard.
QUEST_REF = {
    "000": {
        "dialogue": (
            "I'm getting too old to climb trees,"
            +" can you please pick 3 apples for me?"
            ),
        "dialogue_time": 3,
        "item": "Apple",
        "number": 3,
        "reward_item": "Energy",
        "reward_num": 1 
    },
    "001": {
        "dialogue": (
            "Heya, I dropped my card on the other side" 
            +" of that wraith over there, could you grab it for me?"
            ),
        "dialogue_time": 4,
        "item": "Card",
        "number": 1,
        "reward_item": "Energy",
        "reward_num": 1 
    },
    "002": {
        "dialogue": (
            "I've been looking for a legal document in my basement,"
            +" can you find it for me?"
            +" I'll give you this knife if you find it."
            ),
        "dialogue_time": 5,
        "item": "Document",
        "number": 1,
        "reward_item": "Knife",
        "reward_num": 1
    },
    "003": {
        "dialogue": (
            "Please kill the wraith over there,"
            +" we need to be able to access the church."
            +" I can grant you access if you kill it."
            ),
        "dialogue_time": 5,
        "item": "Ectoplasm",
        "number": 1,
        "reward_item": "Church Key",
        "reward_num": 1
    },
    "100": {
        "dialogue": (
            "Help, I've lost my helmet."+
            " Get it for me so I can keep mining and I'll give you a key."
            ),
        "dialogue_time": 5,
        "item": "Helmet",
        "number": 1,
        "reward_item": "Cave Key",
        "reward_num": 1
    },
    "200": {
        "dialogue": "I get rainbow rock. You get key of god. Deal?",
        "dialogue_time": 3,
        "item": "Rainbow Rock",
        "number": 1,
        "reward_item": "God Key",
        "reward_num": 1
    }
}

# Loading mirrored sprites
def load_texture_pair(filename):
    """
    Load a texture pair from a file path, 
    with the second being a mirror image.
    """
    # Returns a list of the image file as an arcade texture and its
    # mirror image texture.
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

def calculate_distance(pos_1, pos_2):
    """Returns distance between two positions"""

    # Uses Pythagora's Theorem to calculate straight line distance
    # between two postions. Literals have not been changed because
    # they literally just mean squaring the value in this case, no
    # other meaning contained.
    distance_x = pos_1[X_POS] - pos_2[X_POS]
    distance_y = pos_1[Y_POS] - pos_2[Y_POS]
    return math.sqrt(distance_x**2 + distance_y**2)


# Entity superclass
class Entity(arcade.Sprite):
    """Overarching class for every sprite."""

    def __init__(self, category_folder, sprite_folder, available_anims: list):
        """
        Initialises all of the texture lists relevant to the entity.
        Default texture is the first idle texture.
        """
        # Inherit from parent class (arcade.Sprite)
        super().__init__()

        # Default right facing
        self.facing_direction = RIGHT_FACING

        # Set the current texture index to 0, which is the first
        # texture. Scale the textures by CHARACTER_SCALING by default.
        # (This can be overidden in child classes).
        self.cur_texture = FIRST_TEXTURE
        self.scale = CHARACTER_SCALING

        # Define the main path accessed in this class.
        main_path = f"{MAIN_PATH}/assets/{category_folder}/{sprite_folder}"

        # The below section loads the image files into lists
        # based on the animation they are a part of.
        # Since all of the code is essentially the same here,
        # I'll just put the explanation up here for the whole thing.
        # The program first uses the os library to find the number of
        # files in the image folder for the animation.
        # Because the only files in the folders are the images,
        # we can just count the number of files in the folder which
        # corresponds to the number of frames in the animation.
        # Then for each image in the animation folder we load the
        # texture pair generated into the animation texture list,
        # while also saving the number of frames in the animation
        # for later.
        if "Idle" in available_anims:
            # Idle frames
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/idle"):
                frame_num += UNIT_INCREMENT

            self.idle_frames = frame_num
            self.idle_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/idle/{i}.png")
                self.idle_textures.append(texture)

        if "Jump" in available_anims:
            # Jumping and falling sprites
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/jump"):
                frame_num += UNIT_INCREMENT

            self.jump_frames = frame_num
            self.jump_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/jump/{i}.png")
                self.jump_textures.append(texture)

            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/fall"):
                frame_num += UNIT_INCREMENT

            self.fall_frames = frame_num
            self.fall_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/fall/{i}.png")
                self.fall_textures.append(texture)

        if "Walk" in available_anims:
            # Walking frames
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/walk"):
                frame_num += UNIT_INCREMENT

            self.walk_frames = frame_num
            self.walk_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/walk/{i}.png")
                self.walk_textures.append(texture)

        if "Climb" in available_anims:
            # Climbing frames
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/climb"):    
                frame_num += UNIT_INCREMENT

            self.climbing_frames = frame_num
            self.climbing_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/climb/{i}.png")
                self.climbing_textures.append(texture)

        if "Wave" in available_anims:
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/wave"):
                frame_num += UNIT_INCREMENT

            self.wave_frames = frame_num
            self.wave_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/wave/{i}.png")
                self.wave_textures.append(texture)

        if "Death" in available_anims:
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/death"):
                frame_num += UNIT_INCREMENT
            
            self.death_frames = frame_num
            self.death_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/death/{i}.png")
                self.death_textures.append(texture)
        
        if "Open" in available_anims:
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/open"):
                frame_num += UNIT_INCREMENT
            
            self.open_frames = frame_num
            self.open_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/open/{i}.png")
                self.open_textures.append(texture)
        
        if "Closed" in available_anims:
            frame_num = FIRST_TEXTURE
            for path in os.listdir(f"{main_path}/closed"):
                frame_num += UNIT_INCREMENT
            
            self.closed_frames = frame_num
            self.closed_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/closed/{i}.png")
                self.closed_textures.append(texture)
            
        # Set initial texture
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

        # Set hitbox
        # Arcade creates a hitbox based on the vertices of the texture.
        self.set_hit_box(self.texture.hit_box_points)

# Collectible Objects Template class
class Collectible(Entity):
    """
    Template for collectible items like orbs,
    quest collectibles, and secrets.
    """
    def __init__(self, sprite_folder):
        """
        Initialises the relevant animations/textures which are
        the idle textures for collectibles.
        Sets the scaling of the sprites to COLLECTIBLE_SCALING.
        """
        # Inherit from parent class (Entity)
        super().__init__("InanimateObjects", sprite_folder, ["Idle"])

        # Override the CHARACTER_SCALING from the parent class with
        # COLLECTIBLE_SCALING
        self.scale = COLLECTIBLE_SCALING


# Energy Orb class
class Orb(Collectible):
    """Energy Orb Sprite"""

    def __init__(self):
        """
        Loads the specific EnergyOrb textures from the sprite folder
        in assets. Initialises the type attribute and sets it to None.
        """
        # Inherit from parent class (Collectible)
        super().__init__("EnergyOrb")

        # The type attribute is used to figure out what kind of
        # collectible the player has collided with.
        self.type = None

    def update_animation(self, delta_time: float = FRAMERATE):
        """
        Updates the texture of the orb every frame.
        """
        # For every frame, increase the current texture index by one.
        # However, the texture only changes every n frame indexes,
        # where n is the animation rate multiplier defined in the
        # ANIM_MULT dictionary.
        # Once the current texture index reaches its maximum,
        # where the last texture in the loop has displayed for the
        # correct number of frames, it is reset to 0.
        self.cur_texture += UNIT_INCREMENT
        if (
            self.cur_texture 
            > 
            self.idle_frames*ANIM_MULT["Orb"]["Idle"]-INDEX_OFFSET
            ):
            self.cur_texture = FIRST_TEXTURE
        self.texture = self.idle_textures[
            self.cur_texture // ANIM_MULT["Orb"]["Idle"]
            ][RIGHT_FACING]
        return

# All of the collectible classes below have the same format so I will
# only comment and explain one of them.
# Apple class
class Apple(Collectible):
    """Apple collectible sprite"""

    def __init__(self):
        """
        Initialises the apple texture and type attribute.
        The type attribute identifies the sprite during collisions.
        """
        # Inherit from parent class (Collectible)    
        super().__init__("Apple")

        # The type attribute is used to figure out what kind of
        # collectible the player has collided with.
        self.type = None

        # Sets initial texture to the idle texture.
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Lost card class
class Card(Collectible):
    """Card collectible sprite"""

    def __init__(self):
        """
        Initialises the card texture and type attribute.
        The type attribute identifies the sprite during collisions.
        """
        # Inherit from parent class (Collectible)
        super().__init__("Card")
        self.type = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Lost document class
class Document(Collectible):
    """Document collectible sprite"""

    def __init__(self):
        """
        Initialises the document texture and type attribute.
        The type attribute identifies the sprite during collisions.
        """
        # Inherit from parent class (Collectible)
        super().__init__("Document")
        self.type = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Lost helmet class
class Helmet(Collectible):
    """Quest collectible helmet sprite"""
    def __init__(self):
        """
        Initialises the helmet texture and type attribute.
        The type attribute identifies the sprite during collisions.
        """
        # Inherit from parent class (Collectible)
        super().__init__("Helmet")
        self.type = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Rainbow Rock class
class RainbowRock(Collectible):
    """Quest collectible rainbow rock"""
    def __init__(self):
        """
        Initialises the rainbow rock texture and type attribute.
        The type attribute identifies the sprite during collisions.
        """
        # Inherit from parent class (Collectible)
        super().__init__("RainbowRock")
        self.type = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Key class
class Key(Collectible):
    """Collectible key sprite"""

    def __init__(self):
        """
        Initialises the key texture, type attribute, and id attribute.
        The type attribute identifies the sprite during collisions.
        The id attribute determines which doors can be opened with
        the key.
        """
        # Inherit from parent class (Collectible)
        super().__init__("Key")
        self.type = None
        self.id = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Secrets sprite classes
# Constructor for secret statuette texture
# Once again the classes below all have the same format so I'll only
# comment and explain one of them.
class Statuette(Collectible):
    """Sprite for statuette (secret)"""
    def __init__(self):
        """
        Initialises the statuette texture and type and name attributes.
        The type attribute identifies the sprite during collisions.
        The name attribute differentiates the secrets.
        """

        # Inherit from parent class (Collectible)
        super().__init__("Statuette")
        self.type = None

        # Name is used to figure out which secrets the player
        # discovered once the game ends.
        self.name = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Constructor for secret diamond pickaaxe texture
class DiamondPickaxe(Collectible):
    """Sprite for diamond pickaxe (secret)"""
    def __init__(self):
        """
        Initialises the pickaxe texture and type and name attributes.
        The type attribute identifies the sprite during collisions.
        The name attribute differentiates the secrets.
        """

        # Inherit from parent class (Collectible)
        super().__init__("DiamondPickaxe")
        self.type = None
        self.name = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Constructor for secret diamond ore texture
class Diamond(Collectible):
    """Sprite for diamond (secret)"""
    def __init__(self):
        """
        Initialises the diamond texture and type and name attributes.
        The type attribute identifies the sprite during collisions.
        The name attribute differentiates the secrets.
        """

        # Inherit from parent class (Collectible)
        super().__init__("Diamond")
        self.type = None
        self.name = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Constructor for secret totem texture
class Totem(Collectible):
    """Sprite for totem (secret)"""
    def __init__(self):
        """
        Initialises the totem texture and type and name attributes.
        The type attribute identifies the sprite during collisions.
        The name attribute differentiates the secrets.
        """

        # Inherit from parent class (Collectible)
        super().__init__("Totem")
        self.type = None
        self.name = None
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]

# Other sprites
# Class for the level end portal sprite
class GoalPortal(Entity):
    """Sprite for next level portal"""
    def __init__(self):
        """
        Initialises the end portal texture.
        Also initialises the warp and dest attributes.
        Warp determines which level to setup,
        and dest determines the spawnpoint of the player.
        """

        # Inherit from parent class (Entity)
        super().__init__("InanimateObjects", "GoalPortal", ["Idle"])
        self.texture = self.idle_textures[FIRST_TEXTURE][RIGHT_FACING]
        self.warp = None
        self.dest = None

# Class for changing locked door textures
class LockedDoor(Entity):
    """Display entity for locked doors"""

    def __init__(self):
        """
        Initialises the locked door textures.
        Also initialises the id and open attributes.
        Id determines which key can open it,
        and open determines whether the player can pass through or not.
        """

        # Inherit from parent class (Entity)
        super().__init__("InanimateObjects", "LockedDoor", ["Idle", "Open", "Closed"])
        self.id = None        
        self.open = False
        self.texture = self.closed_textures[FIRST_TEXTURE][RIGHT_FACING]
        

    def update_animation(self, delta_time: float = FRAMERATE):
        """
        Procedure which updates the door texture.
        Texture can switch from closed to open depending on the parity
        of the open attribute.
        """

        # If the state of the object is 'not open', then display the
        # closed door texture. Otherwise, display the open door
        # texture.
        if self.open == False:
            self.texture = self.closed_textures[FIRST_TEXTURE][RIGHT_FACING]
        else:
            self.texture = self.open_textures[FIRST_TEXTURE][RIGHT_FACING]

# Knife class
class Knife(Entity):
    """Display knife when swung"""

    def __init__(self):
        """
        Initialises the knife textures.
        Also initialises the cur_texture and swing_finished attributes.
        Cur_texture determines the current texture to display,
        and swing_finished tells the program to whether to delete
        the knife after swinging.
        The scale factor of the texture is set to KNIFE_SCALING.
        """

        # Inherit from parent class (Entity)
        super().__init__("InanimateObjects", "Knife", ["Idle"])
        self.cur_texture = FIRST_TEXTURE
        self.swing_finished = False
        self.scale = KNIFE_SCALING
    
    def update_animation(self, delta_time: float = FRAMERATE):
        """
        Changes the knife's texture as it goes through the swing.
        Once the last texture has been reached the swing_finished
        attribute becomes true and the knife despawns.
        """

         # Change direction if needed
         # Once the last texture of the animation has been displayed
         # for the correct number of frames despawn the knife.
         # The boolean swing_finished is used to tell the program to
         # despawn the knife.
        if not self.swing_finished:
            self.texture = self.idle_textures[
                self.cur_texture // ANIM_MULT["Knife"]["Idle"]
                ][self.facing_direction]
            self.cur_texture += UNIT_INCREMENT
        if (
            self.cur_texture 
            > 
            self.idle_frames*ANIM_MULT["Knife"]["Idle"]-INDEX_OFFSET
            ):
            self.swing_finished = True
            
# Player Class
class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self, shape):
        """
        Initialises all of the textures of the various player shapes
        available. For each shape different animations are available.
        The attributes which are initialised are:
        shape:          This is the form of the player sprite, and 
                        determines which set of textures to use.
        jumping:        States whether the player is jumping or not.
                        Used to determine when to start doing certain
                        animations.
        is_on_ladder:   States whether the player is on a ladder.
                        Used to determine when to start doing certain
                        animations and physics movements.
        is_dead:        Whether the player is dead. Used to start the
                        death animation.
        dying:          States if the player is in the death animation.
                        Used to determine when to stop the animation
                        and respawn the player.
        """

        if shape == PLAYER_SHAPE_HUMAN:
            available_anims = ["Idle", "Walk", "Jump", "Climb", "Death"]
        else:
            available_anims = ["Idle", "Walk", "Jump", "Death"]
        # Inherit from parent class (Entity)
        super().__init__(
            "Friendly", f"Player{shape+INDEX_OFFSET}", available_anims
            )

        # Track state
        # The various states are quite self-explanatory,
        # though the difference between is_dead and dying is that
        # during the death animation both is_dead and dying are True,
        # but after the animation finishes dying becomes False.
        self.shape = shape
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_dead = False
        self.dying = False

    def update_animation(self, delta_time: float = FRAMERATE):
        """
        Changes the player sprite's texture every frame
        depending on its current state.
        """
        # Change direction if needed
        # If the player is moving left but facing right make it face
        # left and vice versa.
        if (
            self.change_x < STATIONARY 
            and 
            self.facing_direction == RIGHT_FACING
            ):
            self.facing_direction = LEFT_FACING
        elif (
            self.change_x > STATIONARY 
            and 
            self.facing_direction == LEFT_FACING
            ):
            self.facing_direction = RIGHT_FACING

        # Hierarchy of animations:
        # Death, Climbing, Jumping, Idle, Walking
        # Each frame the player can only be doing one of these actions.
        # Once the animation with the highest rank in the hierarchy
        # plays for that frame, the method ends and no other animations
        # will run.
        # The reason for this specific hierarchy is because if the
        # player is dead they should not be able to do any other
        # actions.
        # Otherwise, if there's movement in the y-direction regardless
        # of x-movement the player must be jumping, unless they're on a
        # ladder in which they are climbing instead.
        # Finally, if the player has no y-movement or x-movement they
        # must be idle, which leaves the walking animation where there
        # is x-movement as the lowest rank in the hierarchy.
        # The animations themselves work on the same basis as all of
        # the previous ones so I won't go into detail about how it
        # works.
        # Different player shapes also have different animations and
        # rates of animation so there are if statements checking player
        # shape and playing corresponding animations.

        # Death animation
        # If the player is dead start the death animation.
        # However, the animation should only play once then the player
        # should respawn, so after one cycle the 'dying' and 'is_dead'
        # attributes will no longer match and the animation ends,
        # triggering the player respawn.
        if self.is_dead:
            if not self.dying:
                self.cur_texture = FIRST_TEXTURE
                self.dying = True
            if (
                self.cur_texture 
                > 
                (
                    self.death_frames*ANIM_MULT["Player1"]["Death"]
                    -INDEX_OFFSET
                )
                ):
                self.cur_texture = FIRST_TEXTURE
                self.is_dead = False
                  
            self.texture = self.death_textures[
                self.cur_texture // ANIM_MULT["Player1"]["Death"]
                ][self.facing_direction]
            self.cur_texture += UNIT_INCREMENT
            return

        # Climbing animation
        # If the player is on a ladder and their y-speed
        # is greater than START_CLIMB play the climbing animation.
        if self.shape == PLAYER_SHAPE_HUMAN:
            if self.is_on_ladder:
                self.climbing = True
            if not self.is_on_ladder and self.climbing:
                self.climbing = False
            if self.climbing and abs(self.change_y) > START_CLIMB:
                self.cur_texture += UNIT_INCREMENT
                if (
                    self.cur_texture 
                    > 
                    self.climbing_frames*ANIM_MULT["Player1"]["Climb"]
                    -INDEX_OFFSET
                    ):
                    self.cur_texture = FIRST_TEXTURE
            if self.climbing:
                self.texture = self.climbing_textures[
                    self.cur_texture // ANIM_MULT["Player1"]["Climb"]
                    ][self.facing_direction]
                return

        # Jumping animation
        if self.change_y > STATIONARY and not self.is_on_ladder:
            if self.shape == PLAYER_SHAPE_BLAZE:
                self.cur_texture += UNIT_INCREMENT
                if (
                    self.cur_texture 
                    > self.jump_frames*ANIM_MULT["Player3"]["Jump"]
                    -INDEX_OFFSET
                    ):
                    self.cur_texture = FIRST_TEXTURE
                self.texture = self.jump_textures[
                    self.cur_texture // ANIM_MULT["Player3"]["Jump"]
                    ][self.facing_direction]
            else:
                self.texture = self.jump_textures[
                    FIRST_TEXTURE
                    ][self.facing_direction]
            return
        elif self.change_y < STATIONARY and not self.is_on_ladder:
            if self.shape == PLAYER_SHAPE_BLAZE:
                self.cur_texture += UNIT_INCREMENT
                if (
                    self.cur_texture 
                    > self.jump_frames*ANIM_MULT["Player3"]["Jump"]
                    -INDEX_OFFSET
                    ):
                    self.cur_texture = FIRST_TEXTURE
                self.texture = self.fall_textures[
                    self.cur_texture // ANIM_MULT["Player3"]["Jump"]
                    ][self.facing_direction]
            else:
                self.texture = self.fall_textures[
                    FIRST_TEXTURE
                    ][self.facing_direction]
            return

        # Idle animation
        if self.change_x == STATIONARY:
            self.cur_texture += UNIT_INCREMENT
            if self.shape == PLAYER_SHAPE_BLAZE:
                if (
                    self.cur_texture 
                    > 
                    self.idle_frames*ANIM_MULT["Player3"]["Idle"]
                    -INDEX_OFFSET
                    ):
                    self.cur_texture = FIRST_TEXTURE
                self.texture = self.idle_textures[
                    self.cur_texture // ANIM_MULT["Player3"]["Idle"]
                    ][self.facing_direction]
            else:
                if (
                    self.cur_texture 
                    > 
                    self.idle_frames*ANIM_MULT["Player1"]["Idle"]
                    -INDEX_OFFSET
                    ):
                    self.cur_texture = FIRST_TEXTURE
                self.texture = self.idle_textures[
                    self.cur_texture // ANIM_MULT["Player1"]["Idle"]
                    ][self.facing_direction]
            return

        # Walking animation
        self.cur_texture += UNIT_INCREMENT
        if (
            self.cur_texture 
            > 
            self.walk_frames*ANIM_MULT["Player1"]["Walk"]
            -INDEX_OFFSET
            ):
            self.cur_texture = FIRST_TEXTURE
        self.texture = self.walk_textures[
            self.cur_texture // ANIM_MULT["Player1"]["Walk"]
            ][self.facing_direction]


# Villager NPC
class DefaultVillager(Entity):
    """Villager Sprite template class"""
    def __init__(self, villager_texture_id):
        """
        Initialises all of the villager textures.
        Also initialises the attributes:
        id:         Unique id for each villager for quest management.
        wave:       Whether the villager is waving or not.
        interactable: Whether the player can interact with the villager

        Parameters:
        villager_texture_id: This determines which villager texture
                             pack to choose from the sprite folders.
        """
        # Inherit from parent class (Entity)
        super().__init__(
            "Friendly", f"Villager{villager_texture_id}", ["Idle", "Wave"]
            )

        # Track states
        self.id = None
        self.wave = False
        self.interactable = False

    def update_animation(self, delta_time: float = FRAMERATE):
        """
        Updates the texture of the villager every frame.
        Textures can also change depending on the state of the
        villager.
        """
        # Idle animation
        # If the villager is not waving play the idle animation.
        if self.wave == False:
            self.texture = self.idle_textures[
                FIRST_TEXTURE
                ][self.facing_direction]

        # Wave animation
        # If the villager is waving play the wave animation.
        elif self.wave == True:
            self.texture = self.wave_textures[
                FIRST_TEXTURE
                ][self.facing_direction]
        return

    def update(self, player_pos, tile_map, delta_time: float = FRAMERATE):
        """
        Every frame this checks whether the player
        is close enough to the villager to interact.
        Parameters:
        player_pos: Player position
        tile_map: The tilemap so the tile dimensions can be found.
        delta_time: Framerate basically.
        If the player is close to the villager the interactable
        attribute changes.
        """

        # Once the player is within 1 block horizontally and half a 
        # block vertically of the villager it is able to be 
        # interacted with.
        if (
            abs(self.center_x - player_pos[X_POS]) 
            < 
            TILE_SCALING*tile_map.tile_width 
            and 
            abs(self.center_y-player_pos[Y_POS]) 
            < 
            HALF_BLOCK*TILE_SCALING*tile_map.tile_height
            ):
            self.interactable = True
        else:
            self.interactable = False
        return

# Default enemy class
class Enemy(Entity):
    """Template class for all enemies"""
    def __init__(self, category_folder, sprite_folder):
        """
        Initialises the textures for the enemy for the available
        animations/actions.
        Also initalises the drop attribute which is the item the
        enemy drops upon death.
        """
        # Inherit from parent class (Entity)
        # Available textures are idle and walking.
        super().__init__(category_folder, sprite_folder, ["Idle", "Walk"])
        self.drop = None
    
    def update_animation(self, delta_time: float = FRAMERATE):
        """
        Updates the textures every frame for enemies.
        This creates the walking animation.
        """
        # Changing facing directions
        # This works the same as the player so no explanation.
        # However, because I accidentally created all the enemy sprites
        # facing left by default, the LEFT_FACING and RIGHT_FACING
        # constants are swapped for this class.
        if (
            self.change_x < STATIONARY 
            and 
            self.facing_direction == LEFT_FACING
            ):
            self.facing_direction = RIGHT_FACING
        elif (
            self.change_x > STATIONARY 
            and 
            self.facing_direction == RIGHT_FACING
            ):
            self.facing_direction = LEFT_FACING
        
        # Walking animation
        # Same as before so no explanation.
        self.cur_texture += UNIT_INCREMENT
        if (
            self.cur_texture 
            > 
            self.walk_frames*ANIM_MULT["Enemy"]["Walk"]
            -INDEX_OFFSET
            ):
            self.cur_texture = FIRST_TEXTURE
        self.texture = self.walk_textures[
            self.cur_texture // ANIM_MULT["Enemy"]["Walk"]
            ][self.facing_direction]
        

# Wraith enemy class
class Wraith(Enemy):
    """Wraith enemy texture class"""
    def __init__(self):
        """
        Initialises the textures for the wraith enemy class.
        Takes the textures from the Wraith folder in assets.
        Sets the walking speed to WRAITH_SPEED.
        """

        # Inherit from parent class (Enemy)
        super().__init__("Enemies", "Wraith")
        self.change_x = WRAITH_SPEED

# Bird enemy class
class Bird(Enemy):
    """Bird enemy texture class"""
    def __init__(self):
        """
        Initialises the textures for the bird enemy class.
        Takes the textures from the Wraith folder in assets.
        Sets the moving speed to BIRD_SPEED.
        """
        super().__init__("Enemies", "Bird")
        self.change_x = BIRD_SPEED

# Menu Screen
class MainMenu(arcade.View):
    """
    The main menu screen displayed at the beginning.
    """

    def on_show_view(self):
        """Called when showing this view."""
        arcade.set_background_color(MENU_BACKGROUND)

    def on_draw(self):
        """Display the menu"""
        self.clear()
        arcade.draw_text(
            "Click to start game",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            BLACK,
            font_size = 30,
            anchor_x = "center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the actual game view."""
        game_view = GameView()
        self.window.show_view(game_view)

# End Screen
class EndScreen(arcade.View):
    """
    The screen displayed when the game is finished.
    """
    def __init__(self, secrets_found):
        """
        Initialises the background image of the end screen.
        This is chosen by working out which secrets the player found
        and displaying the corresponding image from the folder.
        Takes in the parameter secrets_found, which is the list of
        secrets the player managed to find.
        """
        super().__init__()
        self.background = arcade.load_texture()

        # Using by checking which secrets are present in the found list
        # a unique string of numbers can be created for each
        # combination of secrets. This is subsequently the file name
        # for each background image.
        self.secrets_to_display = ""
        self.secrets_found = secrets_found
        if "Statuette" in self.secrets_found:
            self.secrets_to_display += "1"
        else:
            self.secrets_to_display += "0"
        if "Diamond Pickaxe" in self.secrets_found:
            self.secrets_to_display += "1"
        else:
            self.secrets_to_display += "0"
        if "Diamond" in self.secrets_found:
            self.secrets_to_display += "1"
        else:
            self.secrets_to_display += "0"
        if "Totem" in self.secrets_found:
            self.secrets_to_display += "1"
        else:
            self.secrets_to_display += "0"

    def on_show_view(self):
        """Called when showing this view."""
        arcade.draw_lrwh_rectangle_textured(
            0,
            0,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            self.background
        )
        arcade.draw_lrwh_rectangle_textured(
            0,
            0,
            SCREEN_WIDTH,
            0.5*SCREEN_HEIGHT,
            f"{self.secrets_to_display}.png"
        )


# Actual Game
class GameView(arcade.View):
    """
    The actual game class.
    """

    def __init__(self):
        """
        Initialises every attribute needed in the game.
        These include attributes for detecting key presses,
        info and stats on the player,
        quest management,
        sensing whether the player can interact,
        the layers contained in a tilemap and timer variables,
        sound, level changing variables, and the actual functionality
        variables like tilemap and physics engine.
        The music also starts playing on loop.
        """
        # Set up window with parent class (arcade.View)
        super().__init__()

        # Make the mouse pointer invisible.
        self.window.set_mouse_visible = False


        # Variables to check which key is being pressed,
        # as well as different states related to key presses.
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.interact = False
        self.swing_knife = False

        # Player stats (health, energy, etc)
        # Also contains the quest required items inventory and
        # the quest reward and other items inventory.
        # The inventories use the ID of the quest they belong to
        # as a key.
        # The rest are fairly self explanatory.
        self.health = MAX_HEALTH
        self.energy = NOTHING
        self.shape = PLAYER_SHAPE_HUMAN
        self.fly_speed = STATIONARY
        self.thrust = PLAYER_THRUST
        self.can_knife = True
        self.inventory_quest = {
            "000": {"name": "Apples", "number": 0},
            "001": {"name": "Cards", "number": 0},
            "002": {"name": "Documents", "number": 0},
            "003": {"name": "Ectoplasm", "number": 0},
            "100": {"name": "Helmet", "number": 0},
            "200": {"name": "Rainbow Rock", "number": 0}
        }

        self.inventory_other = {
            "002": {"name": "Knife", "type": "Weapon", "number": 0},
            "003": {"name": "Church Key", "type": "Key", "number": 0},
            "100": {"name": "Cave Key", "type": "Key", "number": 0},
            "200": {"name": "God Key", "type": "Key", "number": 0}
        }
        self.keys_obtained = []
        self.secrets_found = []

        # Quest variables
        # These variables are all related to the quest system,
        # and are fairly self explanatory.
        # not_complete_time is a timer which dictates how long to
        # display the pop up text when attempting to hand in an
        # unfinished quest.
        self.quests = {}
        self.in_quest = False
        self.not_complete_time = NOTHING
        self.finished_quest = None
        self.latest_quest = None
        self.check_quest = None
        self.completed_quests = []
        self.quest_ended = False

        # Sensing variables
        # Fairly self explanatory, interactable_door is the
        # warp door (door that goes to a sublevel) which the player is
        # able to interact with. (Standing close enough)
        self.can_interact = False
        self.is_flying = False
        self.interactable_door = None
       
        # Control variables
        # These include timing variables which decrease by
        # delta_time every frame, as well as variables to control
        # what layers are loaded in front the tilemaps.
        self.delta_time = NOTHING
        self.time_since_ground = NOTHING
        self.cooldown = NOTHING
        self.knife_timer = NOTHING
        self.map_has_villagers = None
        self.map_has_orbs = None
        self.map_has_enemies = None
        self.available_layers = []
        self.missing_key_text = NOTHING
        self.secret_found_text = NOTHING

        # Sound effects and audio
        self.bg_music = arcade.load_sound(
            f"{MAIN_PATH}/assets/Audio/Background.mp3"
            )

        # Warp variables
        # This dictionary records the positions of where the 
        # warp doors are.
        self.doors = {}

        # Variables to change player spawnpoint
        self.spawnpoint = (PLAYER_START_X, PLAYER_START_Y)
        self.prev_spawnpoint = None

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
        # Starts with the first main level.
        self.level = "1.1"

        # Primary camera for scrolling the screen
        self.camera = None

        # Play background music
        arcade.play_sound(self.bg_music, MUSIC_VOLUME, looping=True)

    def setup(self):
        """
        Game setup which runs each time game is restarted.
        When this runs all variables are reset except for the music,
        and inventories, which include quest, rewards, secrets,
        and keys.
        """

        # Setup camera
        self.camera = arcade.Camera(self.window.width, self.window.height)

        # Setup GUI camera
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Map name
        map_name = f"{MAIN_PATH}/maps/{self.level}.tmx"

        # Update control variables
        self.map_has_villagers = False
        self.map_has_orbs = False
        self.map_has_enemies = False
        self.map_has_locked_doors = False
        self.available_layers = []
        self.text_layer = None

        # Update sensing variables
        self.interactable_door = None

        # Reset player sprite
        self.player_sprite = None

        # Layer specific options for Tilemap
        # These determine whether a tile layer acts as a wall or not.
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_STATUES: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": False,
            },
            LAYER_NAME_DEATH: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DOOR_BARRIERS_OPEN: {
                "use_spatial_hash": False
            },
            LAYER_NAME_DOOR_BARRIERS_CLOSED: {
                "use_spatial_hash": True
            },
            LAYER_NAME_COLLECTIBLES: {
                "use_spatial_hash": True
            },
            LAYER_NAME_WARP_DOORS: {
                "use_spatial_hash": True
            },
            LAYER_NAME_LOCKED_DOORS: {
                "use_spatial_hash": True
            },
        }

        # Read in Tiled map
        self.tile_map = arcade.load_tilemap(
            map_name, TILE_SCALING, layer_options
            )
        
        # Initialise new scene with the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Setup player at specific coordinates
        self.player_sprite = PlayerCharacter(self.shape)
        self.player_sprite.center_x = (
            self.tile_map.tile_width * TILE_SCALING * self.spawnpoint[X_POS]
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * TILE_SCALING * self.spawnpoint[Y_POS]
        )

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Set the background colour to sky or stone colour depending
        # on whether the level is above ground or not.
        if str(self.level) in GROUND_LEVELS:
            arcade.set_background_color(SKY_BLUE)
        elif str(self.level) in CAVE_LEVELS:
            arcade.set_background_color(STONE_GREY)
        else:
            arcade.set_background_color(BLACK)

        # Create the physics engine
        # The try except is used to check if the "Door Barriers Closed"
        # layer is present in the tilemap.
        # If an error occurs that means the layer is not present and
        # the except block runs, which contains all of the base layers.
        try:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                gravity_constant=GRAVITY,
                ladders=self.scene[LAYER_NAME_LADDERS],
                walls=[
                    self.scene[LAYER_NAME_PLATFORMS], 
                    self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]
                    ],
            )
        except:
            self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite,
                platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                gravity_constant=GRAVITY,
                ladders=self.scene[LAYER_NAME_LADDERS],
                walls=self.scene[LAYER_NAME_PLATFORMS],
            )

        # Make a scene for the GUI
        self.gui_scene = arcade.Scene()

        # Add in NPCs
        # Add in villagers
        # If an error occurs there are no villagers in the layer
        # and the control variable is updated to reflect that.
        try:
            villagers_layer = self.tile_map.object_lists[LAYER_NAME_VILLAGERS]
            for villager_object in villagers_layer:
                cartesian = self.tile_map.get_cartesian(
                    villager_object.shape[X_POS], villager_object.shape[Y_POS]
                )
                # The villager variant used is found by adding 1 to the
                # last digit of the villager id. This is passed on as
                # an argument into the villager constructor.
                villager = DefaultVillager(
                    int(villager_object.properties["id"][-INDEX_OFFSET])
                    +INDEX_OFFSET
                    )
                villager.id = villager_object.properties["id"]
                villager.center_x = math.floor(
                    (cartesian[X_POS]+HALF_BLOCK) 
                    * 
                    TILE_SCALING 
                    * 
                    self.tile_map.tile_width
                )
                villager.center_y = math.floor(
                    (cartesian[Y_POS]+HALF_BLOCK) 
                    * 
                    (self.tile_map.tile_height * TILE_SCALING)
                    -TILE_SCALING
                )

                # Update the control variable which tells the program
                # that the tilemap contains the villager layer.
                self.map_has_villagers = True
                self.scene.add_sprite(LAYER_NAME_VILLAGERS, villager)
        except:
            self.map_has_villagers = False
            

        # Try to add in Enemies
        try:
            enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

            for enemy_object in enemies_layer:
                cartesian = self.tile_map.get_cartesian(
                    enemy_object.shape[X_POS], enemy_object.shape[Y_POS]
                )

                # The enemy type is determined by the custom property
                # "type" from the tilemap.
                enemy_type = enemy_object.properties["type"]
                if enemy_type == "Wraith":
                    enemy = Wraith()
                if enemy_type == "Bird":
                    enemy = Bird()
                enemy.center_x = math.floor(
                    (cartesian[X_POS]) * 
                    TILE_SCALING * 
                    self.tile_map.tile_width
                )
                enemy.center_y = math.floor(
                    (cartesian[Y_POS]+HALF_BLOCK) 
                    * (self.tile_map.tile_height * TILE_SCALING)
                )

                # These setup the left and right limits of the enemy
                # movement.
                if "boundary_left" in enemy_object.properties:
                    enemy.boundary_left = enemy_object.properties[
                        "boundary_left"]
                    
                if "boundary_right" in enemy_object.properties:
                    enemy.boundary_right = enemy_object.properties[
                        "boundary_right"
                        ]
                
                # Sets up the dropped item when the enemy is killed.
                if "drop" in enemy_object.properties:
                    enemy.drop = enemy_object.properties["drop"]
                
                # Sets up whether the enemy is actually killable.
                if "can_kill" in enemy_object.properties:
                    enemy.can_kill = enemy_object.properties["can_kill"]

                # Updates control variable to reflect presence of enemy
                # layer.
                self.map_has_enemies = True
                self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)
        except:
            # If error occurs tilemap does not have enemy layer
            # and control variable is updated to reflect this.
            self.map_has_enemies = False
            

        # Add inanimate objects
        # Try to add in end portal/s
        # Same logic with the try-except here as before,
        # except that because this layer does not need to be updated
        # later it does not need a control variable, so if it doesn't
        # exist in a level it can just ignored.
        try:
            goal_layer = self.tile_map.object_lists[LAYER_NAME_GOAL]
            for goal_object in goal_layer:
                cartesian = self.tile_map.get_cartesian(
                    goal_object.shape[X_POS], goal_object.shape[Y_POS]
                )
                goal = GoalPortal()
                goal.center_x = math.floor(
                    (cartesian[X_POS]+HALF_BLOCK) 
                    * 
                    TILE_SCALING 
                    * 
                    self.tile_map.tile_width
                )
                goal.center_y = math.floor(
                    cartesian[Y_POS]+HALF_BLOCK 
                    * 
                    (self.tile_map.tile_height * TILE_SCALING)
                )

                # Setup the destination level and position from the
                # custom properties.
                warp = goal_object.properties["warp"]
                dest = [
                    goal_object.properties["dest_x"], 
                    goal_object.properties["dest_y"]
                    ]
                goal.warp = warp
                goal.dest = dest
                self.scene.add_sprite(LAYER_NAME_GOAL, goal)
        except:
            pass
                
        
        # Try to add in energy orbs
        # Once again same logic with the try-except.
        try:
            orbs_layer = self.tile_map.object_lists[LAYER_NAME_ORBS]
            for orb_object in orbs_layer:
                cartesian = self.tile_map.get_cartesian(
                    orb_object.shape[X_POS], orb_object.shape[Y_POS]
                )
                orb = Orb()
                orb.center_x = math.floor(
                    (cartesian[X_POS]+HALF_BLOCK) 
                    * 
                    TILE_SCALING 
                    * 
                    self.tile_map.tile_width
                )
                orb.center_y = math.floor(
                    (cartesian[Y_POS]+HALF_BLOCK) 
                    * (self.tile_map.tile_height * TILE_SCALING)
                    -TILE_SCALING
                )
                # Setup the type of the orb object from the custom
                # properties.
                orb.type = orb_object.properties["type"]
                self.map_has_orbs = True
                self.scene.add_sprite(LAYER_NAME_ORBS, orb)
        except:
            self.map_has_orbs = False

        # Try to add in collectibles which include quests and secrets
        # Try-except system works the same, though collectibles don't
        # need to be updated later so no control variable is needed.
        try:
            collectible_layer = self.tile_map.object_lists[
                LAYER_NAME_COLLECTIBLES
                ]
            for collectible_object in collectible_layer:
                cartesian = self.tile_map.get_cartesian(
                    collectible_object.shape[X_POS], 
                    collectible_object.shape[Y_POS]
                )
                collectible_type = collectible_object.properties["type"]

                # Load in the various collectible sprites based on the
                # custom "type" property.
                if collectible_type == "Apple":
                    collectible = Apple()
                if collectible_type == "Card":
                    collectible = Card()
                if collectible_type == "Document":
                    collectible = Document()
                if collectible_type == "Key":
                    collectible = Key()
                    # Set the id (the door matching the key) to the
                    # custom property "unlocks".
                    collectible.id = collectible_object.properties["unlocks"]
                if collectible_type == "Helmet":
                    collectible = Helmet()
                if collectible_type == "Rainbow Rock":
                    collectible = RainbowRock()
                if collectible_type == "Secret":
                    # Load in the secret collectibles, differentiated
                    # based on the custom property "name".
                    collectible_name = collectible_object.properties["name"]
                    if collectible_name == "Statuette":
                        collectible = Statuette()
                        collectible.name = collectible_name
                    if collectible_name == "Diamond Pickaxe":
                        collectible = DiamondPickaxe()
                        collectible.name = collectible_name
                    if collectible_name == "Diamond":
                        collectible = Diamond()
                        collectible.name = collectible_name
                    if collectible_name == "Totem":
                        collectible = Totem()
                        collectible.name = collectible_name
                collectible.type = collectible_type

                # Place the collectible at the center of the tile.
                collectible.center_x = math.floor(
                    (cartesian[X_POS]+HALF_BLOCK) 
                    * 
                    TILE_SCALING 
                    * 
                    self.tile_map.tile_width
                )
                collectible.center_y = math.floor(
                    (cartesian[Y_POS]+HALF_BLOCK) 
                    * 
                    (self.tile_map.tile_height * TILE_SCALING)-TILE_SCALING
                )
                self.scene.add_sprite(LAYER_NAME_COLLECTIBLES, collectible)
        except:
            pass
        
        # Try to add in the guiding text in the air
        # Try except works the same as before.
        try:
            self.text_layer = self.tile_map.object_lists[LAYER_NAME_TEXT]
        except:
            pass

        # Add all warp doors positions into the a dictionary of door 
        # information, with the order of the doors added as the key.
        # "key_req" checks if the door needs a key to use.
        door_layer = self.tile_map.object_lists[LAYER_NAME_WARP_DOORS]
        count = NOTHING
        for door in door_layer:
            cartesian = self.tile_map.get_cartesian(
                door.shape[X_POS], door.shape[Y_POS]
            )
            warp = door.properties["warp"]
            dest = [door.properties["dest_x"], door.properties["dest_y"]]
            key = door.properties["key_req"]
            self.doors[count] = {
                "warp": warp,
                "dest": dest,
                "key_req": key,
                "pos": [
                    cartesian[X_POS]*TILE_SCALING*self.tile_map.tile_width,
                    cartesian[Y_POS]*TILE_SCALING*self.tile_map.tile_width
                    ]
            }
            count += UNIT_INCREMENT

        # Try to add in locked doors
        # Locked doors are barriers in the same level requiring a key.
        # The try-except still works the same as before,
        # preventing errors where there are no locked door layers in
        # the tilemap.
        try:
            locked_door_layer = self.tile_map.object_lists[
                LAYER_NAME_LOCKED_DOORS
                ]
            for locked_door_object in locked_door_layer:
                cartesian = self.tile_map.get_cartesian(
                    locked_door_object.shape[X_POS], 
                    locked_door_object.shape[Y_POS]
                )
                locked_door = LockedDoor()
                locked_door.center_x = math.floor(
                    (cartesian[X_POS]+HALF_BLOCK) 
                    * 
                    TILE_SCALING 
                    * 
                    self.tile_map.tile_width
                )
                locked_door.center_y = math.floor(
                    (cartesian[Y_POS]+HALF_BLOCK) 
                    * self.tile_map.tile_height * TILE_SCALING
                )
                # Matching IDs with the key that unlocks the door.
                locked_door.id = locked_door_object.properties["id"]
                self.map_has_locked_doors = True
                self.scene.add_sprite(LAYER_NAME_LOCKED_DOORS, locked_door)
        except:
            self.map_has_locked_doors = False

        # Setup GUI Layers

        # Setup energy bar
        # This is an image in the top right of the screen,
        # which changes depending on the amount of energy possessed.
        # The default quantity is 0, so the default texture is also
        # 0.png.
        self.gui_scene.add_sprite(
            LAYER_NAME_ENERGY,
            arcade.Sprite(
                texture=arcade.load_texture(
            f"{MAIN_PATH}/assets/GUI/Energy/0.png"
            ), 
                scale=TILE_SCALING,
                center_x=SCREEN_WIDTH-TILE_SCALING*ENERGY_BAR_OFFSET[X_POS],
                center_y=SCREEN_HEIGHT-TILE_SCALING*ENERGY_BAR_OFFSET[Y_POS],
                )
            )

        # Setup health bar
        # This works the same as the energy bar, except the default is
        # 3 rather than 0.
        self.gui_scene.add_sprite(
            LAYER_NAME_HEALTH,
            arcade.Sprite(
                texture=arcade.load_texture(
            f"{MAIN_PATH}/assets/GUI/Health/3.png"
            ),
                scale=TILE_SCALING,
                center_x=SCREEN_WIDTH-TILE_SCALING*HEALTH_BAR_OFFSET[X_POS],
                center_y=SCREEN_HEIGHT-TILE_SCALING*HEALTH_BAR_OFFSET[Y_POS],
            )
        )

        # If these layers exist on the tilemap add them into the
        # "available_layers" list, which will be added into the
        # physics engine update function later.
        if self.map_has_villagers:
            self.available_layers.append(LAYER_NAME_VILLAGERS)
        if self.map_has_orbs:
            self.available_layers.append(LAYER_NAME_ORBS)
        if self.map_has_enemies:
            self.available_layers.append(LAYER_NAME_ENEMIES)
        if self.map_has_locked_doors:
            self.available_layers.append(LAYER_NAME_LOCKED_DOORS)
        

    def on_show_view(self):
        """
        Runs when the window first appears. 
        (Sets up the first level)
        """
        self.setup()

    def on_draw(self):
        """Render the screen"""

        # Clear screen contents (only background remains)
        self.clear()

        # Activate game camera
        self.camera.use()
        
        # Draw the scene 
        # (the pixelated property makes the lines sharper).
        self.scene.draw(pixelated=True)

        # Actually draw the floating text from the layer.
        # If the text colour property is 1 make the text white,
        # otherwise if it is 0 make it black. This is done to increase
        # contrast and thus readability against the background.
        # The try-except works similarly to before where if the layer
        # exists then there are no issues and the code runs normally.
        # If the layer doesn't exist then there will be errors and thus
        # this block of code can be ignored.
        try:
            for text in self.text_layer:
                cartesian = self.tile_map.get_cartesian(
                    text.shape[X_POS], text.shape[Y_POS]
                )
                if text.properties["colour"] == "1":
                    colour = WHITE
                else:
                    colour = BLACK
                arcade.draw_text(
                    text.properties["text"],
                    cartesian[X_POS]*TILE_SCALING*self.tile_map.tile_width,
                    cartesian[Y_POS]*TILE_SCALING*self.tile_map.tile_height,
                    colour,
                    TIPS_FONT,
                    anchor_x="center",
                    anchor_y="center"
                )
        except:
            pass

        # Start quest dialogue
        # If there is an available quest that the player is in,
        # draw the starting dialogue on top of the quest villager.
        # To increase readability also draw a matching white rectangle
        # behind the black text.
        # This will be drawn as long as the timer for that specific
        # quest dialogue is above 0.
        if self.in_quest:
            try:
                if self.latest_quest["dialogue_time"] > NOTHING:
                    arcade.draw_rectangle_filled(
                        self.latest_quest["villager_pos"][X_POS],
                        (self.latest_quest["villager_pos"][Y_POS]
                         +(ONE_BLOCK+HALF_BLOCK)
                         *TILE_SCALING*self.tile_map.tile_width),
                        len(self.start_dialogue)*CHAR_WIDTH+CHAR_WIDTH,
                        RECT_HEIGHT,
                        WHITE,
                    )
                    arcade.draw_text(
                        self.start_dialogue,
                        self.latest_quest["villager_pos"][X_POS],
                        (self.latest_quest["villager_pos"][Y_POS]
                         +(ONE_BLOCK+HALF_BLOCK)
                         *TILE_SCALING*self.tile_map.tile_width),
                        BLACK,
                        DIALOGUE_FONT,
                        anchor_x="center",
                        anchor_y="center",
                    )
            except:
                # If there's no available quest at the moment
                # just ignore this block.
                pass
        
        # If quest not complete then draw this
        # The rectangle and text works the same as before.
        # This is also drawn above the villager that the user
        # is interacting with.
        if self.not_complete_time > NOTHING:
            arcade.draw_rectangle_filled(
                self.check_quest["villager_pos"][X_POS],
                (self.check_quest["villager_pos"][Y_POS]
                 +(ONE_BLOCK+HALF_BLOCK)
                 *TILE_SCALING*self.tile_map.tile_width),
                QUEST_INCOMPLETE_RECT_WIDTH,
                RECT_HEIGHT,
                WHITE
            )
            arcade.draw_text(
                "Bruh you're not done yet",
                self.check_quest["villager_pos"][X_POS],
                (self.check_quest["villager_pos"][Y_POS]
                 +(ONE_BLOCK+HALF_BLOCK)
                 *TILE_SCALING*self.tile_map.tile_width),
                BLACK,
                DIALOGUE_FONT,
                anchor_x="center",
                anchor_y="center",
            )

        # If quest complete draw this
        # The logic here is that self.finished_quest is a temporary
        # store of the latest finished quest. During the period where
        # the latest finished quest still exists, draw the quest
        # complete dialogue on top of the villager being interacted with.
        # Rectangle and text still work the same.
        if self.finished_quest != None:
            if self.finished_quest["dialogue_time"] > NOTHING:
                arcade.draw_rectangle_filled(
                    self.finished_quest["villager_pos"][X_POS],
                    (self.finished_quest["villager_pos"][Y_POS]
                     +(ONE_BLOCK+HALF_BLOCK)
                     *TILE_SCALING*self.tile_map.tile_width),
                    QUEST_COMPLETE_RECT_WIDTH,
                    RECT_HEIGHT,
                    WHITE,
                )
                arcade.draw_text(
                    "Thanks, here is your reward",
                    self.finished_quest["villager_pos"][X_POS],
                    (self.finished_quest["villager_pos"][Y_POS]
                     +(ONE_BLOCK+HALF_BLOCK)
                     *TILE_SCALING*self.tile_map.tile_width),
                    BLACK,
                    DIALOGUE_FONT,
                    anchor_x="center",
                    anchor_y="center",
                )

        # If key missing draw this text above the player sprite.
        if self.missing_key_text > NOTHING:
            arcade.draw_rectangle_filled(
                self.player_sprite.center_x,
                (self.player_sprite.center_y+
                 (ONE_BLOCK+HALF_BLOCK)
                 *TILE_SCALING*self.tile_map.tile_height),
                KEY_MISSING_RECT_WIDTH,
                RECT_HEIGHT,
                WHITE,
            )
            arcade.draw_text(
                "Missing key",
                self.player_sprite.center_x,
                (self.player_sprite.center_y
                 +(ONE_BLOCK+HALF_BLOCK)
                 *TILE_SCALING*self.tile_map.tile_height),
                BLACK,
                DIALOGUE_FONT,
                anchor_x = "center",
                anchor_y="center"
            )

        # If secret found then draw this above the player sprite.
        if self.secret_found_text > NOTHING:
            arcade.draw_rectangle_filled(
                self.player_sprite.center_x,
                (self.player_sprite.center_y
                 +(ONE_BLOCK+HALF_BLOCK)
                 *TILE_SCALING*self.tile_map.tile_height),
                SECRET_FOUND_RECT_WIDTH,
                RECT_HEIGHT,
                WHITE,
            )
            arcade.draw_text(
                "Secret Found",
                self.player_sprite.center_x,
                (self.player_sprite.center_y
                 +(ONE_BLOCK+HALF_BLOCK)
                 *TILE_SCALING*self.tile_map.tile_height),
                BLACK,
                DIALOGUE_FONT,
                anchor_x = "center",
                anchor_y="center"
            )

        # Activate the GUI camera to draw GUI elements
        self.gui_camera.use()

        # Draw GUI content

        # Display current energy and health
        self.gui_scene.draw(pixelated=True)

        # If interact is possible then draw this text
        # This text is drawn in the bottom right of the screen.
        # The colour is white against a black rectangle to
        # increase readability.
        if self.can_interact:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH*INTERACT_TEXT_POS,
                INTERACT_Y_OFFSET,
                INTERACT_RECT_WIDTH,
                RECT_HEIGHT,
                BLACK,
            )
            arcade.draw_text(
                "Press 'f' to interact",
                SCREEN_WIDTH*INTERACT_TEXT_POS,
                INTERACT_Y_OFFSET,
                WHITE,
                INTERACT_FONT,
                anchor_x="center",
                anchor_y="center"
            )
        
        # If in quest then draw the current quest progress.
        # The current quests are taken from the current quest
        # dictionary and are drawn stacked on top of each other.
        # Once a quest is completed it disappears from the current
        # quest list so there are no gaps in the quest progress list
        # under the energy bar.
        if self.in_quest:
            count = FIRST_VALUE
            for id, info in self.quests.items():
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH-QUEST_OFFSET[X_POS]*TILE_SCALING,
                    (SCREEN_HEIGHT-(QUEST_OFFSET[Y_POS]+count*QUEST_Y_GAP)
                     *TILE_SCALING),
                    QUEST_RECT_WIDTH,
                    QUEST_RECT_HEIGHT,
                    WHITE
                )
                arcade.draw_text(
                    (f"{info['quest_item']}: "
                    +f"{self.inventory_quest[id]['number']}/"
                    +f"{info['num_needed']}"),
                    SCREEN_WIDTH-QUEST_OFFSET[X_POS]*TILE_SCALING,
                    (SCREEN_HEIGHT-(QUEST_OFFSET[Y_POS]+count*QUEST_Y_GAP)
                     *TILE_SCALING),
                    BLACK,
                    QUEST_FONT,
                    anchor_x="center",
                    anchor_y="center"
                )
                count += UNIT_INCREMENT
        
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        # There are different actions for different player shapes.
        # For the blaze shape, the down button accelerates the player
        # downwards, while the up button accelerates the player up.
        # It has no jumping mechanic, while the human and dog shapes
        # do.
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_WALK_SPEED
            elif self.shape == PLAYER_SHAPE_BLAZE:
                self.fly_speed += (self.thrust - GRAVITY)*self.delta_time
            else:
                # If the player is a certain distance above the ground
                # it can jump again.
                if (
                    self.physics_engine.can_jump(y_distance=GROUND_DISTANCE)
                    and not self.jump_needs_reset
                ):
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    self.jump_needs_reset = True
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_WALK_SPEED
            elif self.shape == PLAYER_SHAPE_BLAZE:
                self.fly_speed -= (
                    (self.thrust + GRAV_MULT*GRAVITY)
                    *self.delta_time
                    )

        # Process up/down when on a ladder. If both keys pressed
        # at the same time there is no movement.
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = STATIONARY
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = STATIONARY

        # Process left/right
        # Walking left and right when the left and right keys
        # are pressed.
        # If both keys pressed at the same time player does not move.
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_WALK_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_WALK_SPEED
        else:
            self.player_sprite.change_x = STATIONARY

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # If Up Arrow or W key pressed make self.up_pressed True.
        # If the player is in the blaze shape also make the flying
        # state to True.
        # If Down Arrow or S pressed make self.down_pressed True.
        # If in blaze shape also make flying state True.
        # Do the same for left and right states but no flying state
        # changes.
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
            if self.shape == PLAYER_SHAPE_BLAZE:
                self.is_flying = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            if self.shape == PLAYER_SHAPE_BLAZE:
                self.is_flying = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        # The key to interact is F.
        if key == arcade.key.F:
            self.interact = True

        # Shapeshifting is only possible when energy is full.
        # The way shapeshifting works is by deleting the current
        # player sprite and creating a new one in the new shape at the
        # same position and create a new physics engine for that new
        # player sprite, overriding the old one.
        if self.energy >= MAX_ENERGY:

            # If the '1' key is pressed and the player isn't already
            # in the human shape change to human shape.
            # Also consume 3 energy, bring the energy bar back down to
            # empty.
            if key == arcade.key.KEY_1 and self.shape != PLAYER_SHAPE_HUMAN:
                player_pos = (
                    self.player_sprite.center_x, 
                    self.player_sprite.center_y
                    )
                self.shape = PLAYER_SHAPE_HUMAN
                self.energy -= MAX_ENERGY
                self.scene[LAYER_NAME_PLAYER].remove(self.player_sprite)
                self.player_sprite = PlayerCharacter(self.shape)
                self.player_sprite.center_x = player_pos[X_POS]
                self.player_sprite.center_y = player_pos[Y_POS]

                self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
                # This is a repeat of the physics engine setup from 
                # the setup() method. The try-except is used for
                # the same reason.
                try:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        ladders=self.scene[LAYER_NAME_LADDERS],
                        walls=[
                            self.scene[LAYER_NAME_PLATFORMS], 
                            self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]
                            ],
                    )
                except:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        ladders=self.scene[LAYER_NAME_LADDERS],
                        walls=self.scene[LAYER_NAME_PLATFORMS],
                    )

            # If the '2' key is pressed and shape is not dog,
            # shapeshift into dog shape and consume 3 energy.
            if key == arcade.key.KEY_2 and self.shape != PLAYER_SHAPE_DOG:
                player_pos = (
                    self.player_sprite.center_x, 
                    self.player_sprite.center_y
                    )
                self.shape = PLAYER_SHAPE_DOG
                self.energy -= MAX_ENERGY
                self.scene[LAYER_NAME_PLAYER].remove(self.player_sprite)
                self.player_sprite = PlayerCharacter(self.shape)
                self.player_sprite.center_x = player_pos[X_POS]
                self.player_sprite.center_y = player_pos[Y_POS]

                self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
                try:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=[
                            self.scene[LAYER_NAME_PLATFORMS], 
                            self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]
                            ],
                    )
                except:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=self.scene[LAYER_NAME_PLATFORMS],
                    )

            # If the '3' key is pressed and shape is not blaze,
            # change into blaze shape and consume 3 energy.
            if key == arcade.key.KEY_3 and self.shape != PLAYER_SHAPE_BLAZE:
                player_pos = (
                    self.player_sprite.center_x, 
                    self.player_sprite.center_y
                    )
                self.shape = PLAYER_SHAPE_BLAZE
                self.energy -= MAX_ENERGY
                self.scene[LAYER_NAME_PLAYER].remove(self.player_sprite)
                self.player_sprite = PlayerCharacter(self.shape)
                self.player_sprite.center_x = player_pos[X_POS]
                self.player_sprite.center_y = player_pos[Y_POS]

                self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
                try:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=[
                            self.scene[LAYER_NAME_PLATFORMS], 
                            self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]
                            ],
                    )
                except:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=self.scene[LAYER_NAME_PLATFORMS],
                    )

        # If the 'R' key is pressed reset the level and 
        # respawn the player back to the start of the level.
        if key == arcade.key.R:
            self.setup()
            self.player_sprite.center_x = (
                self.tile_map.tile_width 
                * TILE_SCALING 
                * PLAYER_START_X
                )
            self.player_sprite.center_y = (
                self.tile_map.tile_height 
                * TILE_SCALING 
                * PLAYER_START_Y
                )
        
        # If 'Z' is pressed and the player can use their knife
        # then swing the knife.
        if (
            key == arcade.key.Z 
            and 
            self.inventory_other["002"]["number"] > NOTHING 
            and 
            self.can_knife
            ):
            self.swing_knife = True

        # Check for any changes in movement key presses.
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # Change movement states to False when keys are released.
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
            if self.shape == PLAYER_SHAPE_BLAZE:
                self.is_flying = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            if self.shape == PLAYER_SHAPE_BLAZE:
                self.is_flying = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        # Once the F key is released stop interacting.
        if key == arcade.key.F:
            self.interact = False

        # Once the Z key is released stop swinging the knife.
        # This enables the player to hold down Z and continuously
        # swing the knife, though with a cooldown in between.
        if (
            key == arcade.key.Z 
            and 
            self.inventory_other["002"]["number"] > NOTHING
            ):
            self.swing_knife = False

        # Check for any changes in movement key presses.
        self.process_keychange()

    def center_camera_to_player(self, speed=CAMERA_TRACK_SPEED):
        """
        Adjust the camera's position on the tilemap so that the
        player is always in the center, unless camera has already
        reached the bottom left corner, in which case the camera
        does not move further.
        """

        # Set the centre coordinates of the screen
        # relative to the player.
        screen_center_x = (
            self.camera.scale 
            * (
            self.player_sprite.center_x 
            - (self.camera.viewport_width*HALF_BLOCK)
            )
            )
        screen_center_y = (
            self.camera.scale 
            * (
            self.player_sprite.center_y 
            - (self.camera.viewport_height*HALF_BLOCK)
            )
            )
        
        # If the screen is deviated from the player place it back on
        # the player.
        if screen_center_x < ORIGIN[X_POS]:
            screen_center_x = ORIGIN[X_POS]
        if screen_center_y < ORIGIN[Y_POS]:
            screen_center_y = ORIGIN[Y_POS]
        player_centered = (screen_center_x, screen_center_y)

        self.camera.move_to(player_centered, speed)

    def activate_quest(self, villager):
        """
        Method which handles the quest activation.
        Takes the quest info from the reference
        dictionary depending on the villager interacted with.
        """
        
        # When a quest is activated record all of the details,
        # including the villager who issued the quest, and
        # all of the items needed.
        quest = QUEST_REF[villager.id]
        self.start_dialogue = quest["dialogue"]
        self.quests[villager.id] = {
            "quest_id": villager.id,
            "villager_pos": [villager.center_x, villager.center_y],
            "quest_item": quest["item"],
            "num_needed": quest["number"],
            "dialogue_time": quest["dialogue_time"],
        }

        # Set the latest quest to the new quest.
        self.latest_quest = self.quests[villager.id]

    def check_quest_complete(self, villager):
        """
        Checks if the quest in progress has been completed.
        """

        # If there are not enough required items set the current quest
        # to check to this quest and display the quest not complete
        # text above the villager in interaction.
        # Otherwise proceed to the end quest function.
        if (
            self.inventory_quest[villager.id]["number"] 
            < 
            self.quests[villager.id]["num_needed"]
            ):
            self.not_complete_time = QUEST_INCOMPLETE_TIME
            self.check_quest = self.quests[villager.id]
            
        else:
            self.end_quest(villager)
    
    def end_quest(self, villager):
        """
        Concludes the quest which has been adequately done.
        Removes the quest from the current quest list and gives
        rewards.
        """

        # Set the most recent finished quest to this one.
        # Display the quest finished text for the specified amount
        # of time.
        # Also add the completed quest to the completed quests list.
        # Subtract the required items from the quest inventory and add
        # rewards to the rewards and other things inventory, unless the
        # reward is energy in which case if the energy bar is not
        # already full the energy will increase by 1.
        self.finished_quest = self.quests.pop(villager.id)
        self.finished_quest["dialogue_time"] = QUEST_COMPLETE_TIME
        self.quest_ended = True
        self.completed_quests.append(villager.id)
        self.inventory_quest[villager.id]["number"] -= (
            self.finished_quest["num_needed"]
            )
        if QUEST_REF[villager.id]["reward_item"] != "Energy":
            self.inventory_other[villager.id]["number"] += (
                QUEST_REF[villager.id]["reward_num"]
                )
        else:
            if self.energy < MAX_ENERGY:
                self.energy += QUEST_REF[villager.id]["reward_num"]

    def on_update(self, delta_time):
        """
        Movement and game logic.
        Advances the game every frame in terms of physics,
        which includes detecting collisions, adding sprites to layers,
        removing sprites from layers,
        or calculating level changes.
        """

        # Reset the interactable text
        self.can_interact = False

        # Increase the scope of the delta_time variable
        # (frame update time) to the class level.
        self.delta_time = delta_time

        # Move the player
        self.physics_engine.update()

        # If blaze shape then do helicopter physics
        # This means accelerating the player vertically
        # and subjecting them to gravity when they're not flying.
        # If the player hits the ground after 1s the player will stop
        # having a downwards velocity into the ground.
        if self.shape == PLAYER_SHAPE_BLAZE:
            self.player_sprite.change_y = self.fly_speed
            if not self.is_flying:
                self.fly_speed -= GRAV_MULT*GRAVITY*delta_time
            if (
                self.physics_engine.can_jump() 
                and 
                self.time_since_ground > START_CLIMB
                ):
                self.fly_speed = STATIONARY
                self.time_since_ground = NOTHING
            self.time_since_ground += delta_time
                

        # Update animations for the player
        # Change the various states of the player based on
        # physics interactions.
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if (
            self.physics_engine.is_on_ladder() 
            and 
            not self.physics_engine.can_jump()
            ):
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        # Check if knife is being swung
        if self.can_knife:
            # If knife is swung then spawn knife in front of player
            # and play the animation.
            if self.swing_knife:
                knife = Knife()
                if self.player_sprite.facing_direction == RIGHT_FACING:
                    knife.center_x = (
                        self.player_sprite.center_x 
                        + HALF_BLOCK*TILE_SCALING*self.tile_map.tile_width
                        )
                    knife.facing_direction = RIGHT_FACING
                else:
                    knife.center_x = (
                        self.player_sprite.center_x 
                        - HALF_BLOCK*TILE_SCALING*self.tile_map.tile_width
                        )
                    knife.facing_direction = LEFT_FACING
                knife.center_y = self.player_sprite.center_y
                    
                self.scene.add_sprite(LAYER_NAME_KNIFE, knife)

                # Stop swinging knife and activate knife ban.
                self.swing_knife = False
                self.can_knife = False
        else:
            # If knife can't be swung increment the cooldown timer
            # until it can be swung again.
            # If the timer goes past the cooldown time reset the timer
            # and allow the knife to be swung.
            self.knife_timer += delta_time
            if self.knife_timer >= KNIFE_COOLDOWN:
                self.can_knife = True
                self.knife_timer = NOTHING

        # Remove knife after it has finished its swing
        # If an error occurs that just means the knife doesn't exist and we can ignore.
        try:
            for knife in self.scene[LAYER_NAME_KNIFE]:
                if self.player_sprite.facing_direction == RIGHT_FACING:
                    knife.center_x = (
                        self.player_sprite.center_x 
                        + HALF_BLOCK*TILE_SCALING*self.tile_map.tile_width
                    )
                    knife.facing_direction = RIGHT_FACING
                else:
                    knife.center_x = (
                        self.player_sprite.center_x 
                        - HALF_BLOCK*TILE_SCALING*self.tile_map.tile_width
                        )
                    knife.facing_direction = LEFT_FACING
                knife.center_y = self.player_sprite.center_y
                knife.update_animation(delta_time)
                if knife.swing_finished:
                    self.scene[LAYER_NAME_KNIFE].remove(knife)
        except:
            pass

        # Update animations for other layers.
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_PLAYER,
                LAYER_NAME_BACKGROUND,
            ] + self.available_layers
        )

        # Update moving platforms and enemies
        # If there are no moving enemies only update moving platforms.
        if self.map_has_enemies:
            self.scene.update(
                [
                    LAYER_NAME_MOVING_PLATFORMS,
                    LAYER_NAME_ENEMIES
                ],
            )
        else:
            self.scene.update(
                [LAYER_NAME_MOVING_PLATFORMS]
            )

        # All try-excepts beyond this point are used to prevent errors
        # where in some tilemaps certain layers do not exist and will
        # cause an error when attempting to access.

        # Update villagers' interaction possible sensing.
        try:
            for villager in self.scene[LAYER_NAME_VILLAGERS]:
                villager.update(
                    player_pos=(
                    self.player_sprite.center_x, 
                    self.player_sprite.center_y
                    ), 
                    tile_map=self.tile_map
                    )
        except:
            pass

        # See if the enemy hit a boundary and needs to reverse direction.
        try:
            for enemy in self.scene[LAYER_NAME_ENEMIES]:
                if (
                    enemy.boundary_right
                    and enemy.right > (
                    enemy.boundary_right
                    *TILE_SCALING*self.tile_map.tile_width
                    )
                    and enemy.change_x > STATIONARY
                ):
                    # No need for a constant here, this just
                    # reverses the horizontal speed.
                    enemy.change_x *= -1

                if (
                    enemy.boundary_left
                    and enemy.left < (
                    enemy.boundary_left
                    *TILE_SCALING*self.tile_map.tile_width
                    )
                    and enemy.change_x < STATIONARY
                ):
                    # No need for a constant here, this just
                    # reverses the horizontal speed.
                    enemy.change_x *= -1
        except:
            pass
        

        # Only try to check interaction with villagers if in human shape
        if self.shape == PLAYER_SHAPE_HUMAN:
            # If the villager is close enough assign the ID of the
            # villager as the interactable_villager variable.
            try:
                interactable_villager = None
                # Check if in range of villager
                for villager in self.scene[LAYER_NAME_VILLAGERS]:
                    if villager.interactable:
                        self.can_interact = True
                        interactable_villager = villager.id
                        break
                    else:
                        villager.wave = False
            except:
                pass
            try:        
                # Check for interaction with villager
                # If interacted and quest not started yet start
                # the quest. Otherwise check if the quest is done
                # or if the quest is done just wave instead.
                    if self.interact:
                        for villager in self.scene[LAYER_NAME_VILLAGERS]:
                            if villager.id == interactable_villager:
                                if villager.id not in self.completed_quests:
                                    if villager.id not in self.quests.keys():
                                        villager.wave = True
                                        self.activate_quest(villager)
                                    elif (
                                        self.latest_quest["dialogue_time"] 
                                        <= NOTHING
                                        ):
                                        self.check_quest_complete(villager)
                                else:
                                    villager.wave = True
            except:
                pass

        # Check if interaction possible with door
        # If close enough to door interaction is possible.
        # Set the interactable_door variable to whatever door position
        # is the closed to the player.
        for id, info in self.doors.items():
            if (
                calculate_distance(self.player_sprite.position, info["pos"])
                < TILE_SCALING*self.tile_map.tile_width
                ):
                self.interactable_door = id
                self.can_interact = True
                break
            self.interactable_door = None
        
        # Level changing mechanics
        # Check if actually interacting with door
        if (
            self.interact 
            and self.can_interact 
            and self.interactable_door != None
            ):
            # If the door requires no key, setup the level,
            # spawnpoint, disable the interact action and setup the
            # sublevel.
            if self.doors[self.interactable_door]["key_req"] == "None":
                self.level = self.doors[self.interactable_door]["warp"]
                self.spawnpoint = self.doors[self.interactable_door]["dest"]
                self.interact = False
                self.setup()
                return
            else:
                # Check if the player has the key.
                has_key = False
                for item in self.inventory_other.values():
                    if (
                        item["name"] == self.doors[
                            self.interactable_door
                            ]["key_req"] 
                        and item["number"] > NOTHING
                        ):
                        has_key = True
                        break
                if has_key:
                    # If the player has the key also setup the
                    # spawnpoint, spawn position, and stop interacting.
                    self.level = self.doors[self.interactable_door]["warp"]
                    self.spawnpoint = self.doors[
                        self.interactable_door
                        ]["dest"]
                    self.interact = False
                    self.setup()
                    return
                else:
                    # Otherwise the key is missing and the key missing
                    # text is drawn above the player.
                    self.missing_key_text = MISSING_KEY_TIME
                            
        # Check if interaction possible with statue (not current).
        try:
            if (
                len(
                arcade.check_for_collision_with_list(
                self.player_sprite, 
                self.scene[LAYER_NAME_STATUES]
                )
                ) 
                > NOTHING
                ):
                self.can_interact = True
        except:
            pass
        

        # Check for collisions with the statue.
        # The player can only interact with the statue if they're
        # colliding.
        # If there are no statues in the scene ignore this code.
        try:
            if self.interact:
                player_collision_list = arcade.check_for_collision_with_list(
                    self.player_sprite, self.scene[LAYER_NAME_STATUES]
                    )
                for collision in player_collision_list:
                    # If there is an available statue, set the
                    # spawnpoint to that statue and set energy up to
                    # three. (Must be within a certain distance to
                    # interact)
                    # The spawnpoint works by storing the previous
                    # spawnpoint statue in the self.prev_spawnpoint,
                    # and after interacting with a new statue that
                    # statue is moved back to the "Statues" layer,
                    # while the new statue is moved from the "Statues"
                    # layer into the "Current Statue" layer.
                    if self.prev_spawnpoint != None:
                        self.scene[LAYER_NAME_STATUES].append(
                            self.prev_spawnpoint
                            )
                        self.scene[LAYER_NAME_SPAWNPOINT].clear()
                    if (
                        abs(collision.center_x - self.player_sprite.center_x)
                        < 
                        (
                        self.tile_map.tile_width * TILE_SCALING 
                        * MIN_STATUE_DIST
                        )
                        ):
                        self.spawnpoint = (
                            (
                            collision.center_x / 
                            (self.tile_map.tile_width * TILE_SCALING)
                            ), 
                            (
                            collision.center_y / 
                            (
                            self.tile_map.tile_width * TILE_SCALING
                            ) 
                            - ONE_BLOCK)
                            )
                        self.scene[LAYER_NAME_SPAWNPOINT].append(collision)
                        self.scene[LAYER_NAME_STATUES].remove(collision)
                        self.prev_spawnpoint = collision
                        self.energy = MAX_ENERGY
                self.interact = False
        except:
            pass

        # Check for collisions with energy orbs.
        # Only register if the player still has room to gain energy.
        # Try except still works the same as before.
        try:
            if self.energy < MAX_ENERGY:
                player_collision_list = arcade.check_for_collision_with_list(
                    self.player_sprite, self.scene[LAYER_NAME_ORBS]
                    )
                for collision in player_collision_list:
                    if collision.type == "Energy":
                        self.energy += UNIT_INCREMENT
                        self.scene[LAYER_NAME_ORBS].remove(collision)
        except:
            pass
        
        # Check for collisions with keys or secrets
        # All try-excepts in this general area work the same,
        # where if the layer exists in the scene the code runs,
        # but if the layer doesn't exist the code is ignored.
        try:
            player_collision_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_COLLECTIBLES]
                )
            for collision in player_collision_list:
                if collision.type == "Key":
                    # If key collected then remove key from scene and
                    # add the key ID to the lst of keys obtained.
                    self.keys_obtained.append(collision.id)
                    self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
                if collision.type == "Secret":
                    # If secret collected then remove secret from scene
                    # and add the name to the secrets found list.
                    self.secret_found_text = SECRET_FOUND_TIME
                    self.secrets_found.append(collision.name)
                    self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)

        except:
            pass

        # Check for collisions with locked door
        try:
            player_collision_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_LOCKED_DOORS]
                )
            for collision in player_collision_list:
                # If the ID of the door is in the keys obtained list,
                # open the door by moving the thin barrier from a wall
                # layer to a transparent layer and change the texture
                # of the door from closed to open.
                if str(collision.id) in self.keys_obtained:
                    for door_barrier in self.scene[
                        LAYER_NAME_DOOR_BARRIERS_CLOSED
                        ]:
                        self.scene[LAYER_NAME_DOOR_BARRIERS_OPEN].append(
                            door_barrier
                            )
                        self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED].remove(
                            door_barrier
                            )
                    collision.open = True
                else:
                    # If no door ID in the keys obtained list,
                    # display the missing key text above the player.
                    # Also move the door barrier from the transparent
                    # layer to the wall layer so that the player
                    # cannot get past.
                    self.missing_key_text = MISSING_KEY_TIME
                    for door_barrier in self.scene[
                        LAYER_NAME_DOOR_BARRIERS_OPEN
                        ]:
                        self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED].append(
                            door_barrier
                            )
                        self.scene[LAYER_NAME_DOOR_BARRIERS_OPEN].remove(
                            door_barrier
                            )

        except:
            pass

        # Quest item collision processing
        # This checks all of the current quests
        # and checks which quest items are needed.
        # Also stores the ID of the quest which needs the item
        # that is being checked.
        if self.in_quest:
            quest_req_apples = False
            quest_req_cards = False
            quest_req_documents = False
            quest_req_helmets = False
            quest_req_rainbow_rocks = False
            for id, info in self.quests.items():
                if info["quest_item"] == "Apple":
                    quest_req_apples = True
                    quest_id_apples = id
                if info["quest_item"] == "Card":
                    quest_req_cards = True
                    quest_id_cards = id
                if info["quest_item"] == "Document":
                    quest_req_documents = True
                    quest_id_documents = id
                if info["quest_item"] == "Helmet":
                    quest_req_helmets = True
                    quest_id_helmets = id
                if info["quest_item"] == "Rainbow Rock":
                    quest_req_rainbow_rocks = True
                    quest_id_rainbow_rocks = id
            
            # Try Except is used here to ensure no errors.
            # If there is an error that means the level doesn't
            # actually have any collectibles.
            try:
                player_collision_list = arcade.check_for_collision_with_list(
                    self.player_sprite, self.scene[LAYER_NAME_COLLECTIBLES]
                    )
                for collision in player_collision_list:
                    # For all quest items reference the inventory
                    # ID corresponding to that quest and add one to the
                    # quest item belonging to the quest.
                    if quest_req_apples:
                        # Check for collisions with apples
                        if collision.type == "Apple":
                            self.inventory_quest[
                                quest_id_apples
                                ]["number"] += UNIT_INCREMENT
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(
                                collision
                                )
                    if quest_req_cards:
                        # Check for collisions with cards
                        if collision.type == "Card":
                            self.inventory_quest[
                                quest_id_cards
                                ]["number"] += UNIT_INCREMENT
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(
                                collision
                                )
                    if quest_req_documents:
                        # Check for collisions with documents
                        if collision.type == "Document":
                            self.inventory_quest[
                                quest_id_documents
                                ]["number"] += UNIT_INCREMENT
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(
                                collision
                                )
                    if quest_req_helmets:
                        # Check for collisions with helmets
                        if collision.type == "Helmet":
                            self.inventory_quest[
                                quest_id_helmets
                                ]["number"] += UNIT_INCREMENT
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(
                                collision
                                )
                    if quest_req_rainbow_rocks:
                        # Check for collisions with rainbow rocks
                        if collision.type == "Rainbow Rock":
                            self.inventory_quest[
                                quest_id_rainbow_rocks
                                ]["number"] += UNIT_INCREMENT
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(
                                collision
                                )
            except:
                pass


        # Update energy bar
        # Change the texture of the energy bar to the corresponding
        # energy level.
        try:
            for energy_bar in self.gui_scene[LAYER_NAME_ENERGY]:
                energy_bar.texture = arcade.load_texture(
                    f"{MAIN_PATH}/assets/GUI/Energy/{self.energy}.png"
                    )
        except:
            pass

        # Check for stabbing of enemy
        try:
            knife_collision_list = arcade.check_for_collision_with_list(
                self.scene[LAYER_NAME_KNIFE][FIRST_VALUE], 
                self.scene[LAYER_NAME_ENEMIES]
                )
            for collision in knife_collision_list:
                if collision.can_kill:
                    # If the enemy is killable remove enemy
                    # from the scene and add one to the drop
                    # in the inventory.
                    for id, info in self.inventory_quest.items():
                        if collision.drop == info["name"]:
                            self.inventory_quest[id]["number"] += (
                                UNIT_INCREMENT
                                )
                    self.scene[LAYER_NAME_ENEMIES].remove(collision)
        
        except:
            pass

        # Check for collisions with enemies
        # If touching enemy start timer for one second immunity.
        # Also make the player jump up to extricate themself from
        # the situation.
        try:
            player_collision_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_ENEMIES]
                )
            if len(player_collision_list) > NOTHING:
                if self.cooldown <= NOTHING:
                    self.health -= UNIT_INCREMENT
                    self.cooldown = HIT_COOLDOWN
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
        except:
            pass

        # Update health bar
        # Change health bar texture to the current health level.
        try:
            for health_bar in self.gui_scene[LAYER_NAME_HEALTH]:
                health_bar.texture = arcade.load_texture(
                    f"{MAIN_PATH}/assets/GUI/Health/{self.health}.png"
                    )
        except:
            pass

        # Reveal tunnels/cave when player approaches
        try:
            for tile in self.scene[LAYER_NAME_CAVE]:
                # Calculate distance from player to each cave tile.
                distance_to_player = calculate_distance(
                    [
                        self.player_sprite.center_x, 
                        self.player_sprite.center_y
                        ], 
                    [tile.center_x, tile.center_y]
                    )
                # If the distance is less than the upper bound
                # start revealing the blocks underneath by reducing
                # the opacity based on the proportion of current
                # distance against the upper bound.
                # If the distance is less than the lower bound,
                # Make the block fully transparent.
                if (
                    distance_to_player 
                    < 
                    CAVE_REVEAL_DIST*TILE_SCALING*self.tile_map.tile_width
                    ):
                    tile.alpha = (
                        MAX_OPACITY
                        *(
                        max(
                        (
                        distance_to_player-CAVE_TRNSPT_DIST
                        *TILE_SCALING*self.tile_map.tile_width
                        ), 
                        NOTHING
                        )
                        ) 
                        / (
                        CAVE_REVEAL_DIST*TILE_SCALING*self.tile_map.tile_width
                        )
                        )
        except:
            pass
        

        # Once death animation over respawn
        if (
            self.player_sprite.dying 
            and 
            self.player_sprite.dying != self.player_sprite.is_dead
            ):
            self.player_sprite.center_x = (
                self.tile_map.tile_width 
                * TILE_SCALING * self.spawnpoint[X_POS]
                )
            self.player_sprite.center_y = (
                self.tile_map.tile_height 
                * TILE_SCALING * self.spawnpoint[Y_POS]
                )
            # This resets the dying state to not dying.
            self.player_sprite.dying = False

        # Check for collision with death layer (spikes etc)
        try:
            # If the player hits a spike immediately start the
            # death animation.
            if (
                len(
                arcade.check_for_collision_with_list(
                    self.player_sprite, 
                    self.scene[LAYER_NAME_DEATH]
                    )
                ) 
                > NOTHING and not self.player_sprite.is_dead
                ):
                self.player_sprite.is_dead = True
        except:
            pass
        
        # Run player death animation if the player jumps off the edge
        # or runs out of health.
        if (
            self.player_sprite.center_y < ORIGIN[Y_POS]
            or 
            self.health <= NOTHING 
            and 
            not self.player_sprite.is_dead
            ):
            
            self.player_sprite.is_dead = True
        
        # Once the player dies reset their speed and
        # health/energy.
        if self.player_sprite.is_dead:
            self.health = MAX_HEALTH
            self.energy = MAX_ENERGY
            self.fly_speed = STATIONARY

        # If there are quests in the current quest list
        # set the in_quest state to True,
        # otherwise set it to False.
        if len(self.quests) > NOTHING:
            self.in_quest = True
        else:
            self.in_quest = False

        # Reducing all of the timer variables
        if self.cooldown > NOTHING:
            self.cooldown -= delta_time
        else:
            self.cooldown = NOTHING
        
        if self.not_complete_time > NOTHING:
            self.not_complete_time -= delta_time
        else:
            # Once the checking quest text disappears
            # clear the check_quest variable which stores
            # the current quest being checked.
            self.not_complete_time = NOTHING
            self.check_quest = None

        if self.missing_key_text > NOTHING:
            self.missing_key_text -= delta_time
        else:
            self.missing_key_text = NOTHING
        
        if self.secret_found_text > NOTHING:
            self.secret_found_text -= delta_time
        else:
            self.secret_found_text = NOTHING

        # If these variables exist, i.e. after a quest has been started,
        # Run the timer code
        # Otherwise, just ignore it
        try:
            if self.latest_quest["dialogue_time"] > NOTHING:
                self.latest_quest["dialogue_time"] -= delta_time
            else:
                self.latest_quest["dialogue_time"] = NOTHING
            
            if self.finished_quest["dialogue_time"] > NOTHING:
                self.finished_quest["dialogue_time"] -= delta_time
            else:
                self.finished_quest["dialogue_time"] = NOTHING

            # Once the timer for the quest end dialogue goes to 0, 
            # delete the finished quest.
            if (
                self.finished_quest["dialogue_time"] 
                <= 
                NOTHING and self.quest_ended
                ):
                self.finished_quest = None
                self.quest_ended = False
  
        except:
            pass

        # Check for collision with goal/warp portal
        # This moves the player to the next main level.
        try:
            player_collision_list = arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_GOAL]
                )
            for collision in player_collision_list:
                # If the destination level is 4 end the game and show
                # the end screen.
                if collision.warp == "4":
                    end_view = EndScreen()
                    self.window.show_view(end_view)
                else:
                    # Otherwise teleport the player to the next level
                    # and run the setup, placing the player at the
                    # target position.
                    self.level = collision.warp
                    self.spawnpoint = collision.dest
                    self.setup()
                # Once this code runs the update code should stop
                # running and everything resets for the start of the
                # next level.
                return
        except:
            pass
        
        # Center the camera on the player.
        self.center_camera_to_player()

# Main Program

def main():
    """Main Function"""
    # Set the first view shown to the MainMenu() view.
    # Display the view and start the game.
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    arcade.run()

# Things that run
# Run the game only if this file is the main program.
if __name__ == "__main__":
    main()