import arcade, os, random, math

# Defining constants

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

# Window Settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Ataraxia V1"
HALF_BLOCK = 0.5

# Colours
SKY_BLUE = (99, 245, 255)
STONE_GREY = (158, 158, 158)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MENU_BACKGROUND = (188, 188, 255)

# Font sizes
TIPS_FONT = 14
DIALOGUE_FONT = 16

# Sprite Scaling
CHARACTER_SCALING = 5
TILE_SCALING = 5
COLLECTIBLE_SCALING = 2
KNIFE_SCALING = 3

# Sprite facing direction
RIGHT_FACING = 0
LEFT_FACING = 1

# Sprite animation multipliers
# These determine how many frames it takes to update texture once.
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
FIRST_TEXTURE = 0
UNIT_INCREMENT = 1
INDEX_OFFSET = 1
FRAMERATE = 1 / 60

# Level categories
GROUND_LEVELS = ["1.1", "3.1"]
CAVE_LEVELS = ["2.1", "2.2"]

# Layer names
# Character Layers
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_VILLAGERS = "Villagers"
LAYER_NAME_ENEMIES = "Enemies"

# Object Layers
LAYER_NAME_ORBS = "Orbs"
LAYER_NAME_TEXT = "Text"
LAYER_NAME_COLLECTIBLES = "Collectibles"
LAYER_NAME_WARP_DOORS = "Warp Doors"
LAYER_NAME_LOCKED_DOORS = "Locked Doors"
LAYER_NAME_KNIFE = "Knife"
LAYER_NAME_GOAL = "Goal"

# Tile Layers
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
LAYER_NAME_ENERGY = "Energy"
LAYER_NAME_HEALTH = "Health"

# GUI Layer info
ENERGY_BAR_OFFSET = [32, 48]
HEALTH_BAR_OFFSET = [32, 27]

# Physics things
GRAVITY = 1
PLAYER_WALK_SPEED = 10
PLAYER_RUN_SPEED = 15
PLAYER_JUMP_SPEED = 20
PLAYER_THRUST = 10

# Player spawnpoints
PLAYER_START_X = 3
PLAYER_START_Y = 18

# Player characteristics
PLAYER_SHAPE_HUMAN = 0
PLAYER_SHAPE_DOG = 1
PLAYER_SHAPE_BLAZE = 2
MAX_HEALTH = 3
MAX_ENERGY = 3
NOTHING = 0

# Enemy characteristics
WRAITH_SPEED = 5
BIRD_SPEED = 20

# Kinematic constants
STATIONARY = 0
START_CLIMB = 1
X_POS = 0
Y_POS = 1

# Timing constants
KNIFE_COOLDOWN = 0.5

# Volume constants
MUSIC_VOLUME = 0.3

# Dictionary References
QUEST_REF = {
    "000": {
        "dialogue": "I'm getting too old to climb trees, can you please pick 3 apples for me?",
        "dialogue_time": 3,
        "item": "Apple",
        "number": 3,
        "reward_item": "Energy",
        "reward_num": 1 
    },
    "001": {
        "dialogue": "Heya, I dropped my card on the other side of that wraith over there, could you grab it for me?",
        "dialogue_time": 4,
        "item": "Card",
        "number": 1,
        "reward_item": "Energy",
        "reward_num": 1 
    },
    "002": {
        "dialogue": "I've been looking for a legal document in my basement, can you find it for me? I'll give you this knife if you find it.",
        "dialogue_time": 5,
        "item": "Document",
        "number": 1,
        "reward_item": "Knife",
        "reward_num": 1
    },
    "003": {
        "dialogue": "Please kill the wraith over there, we need to be able to access the church. I can grant you access if you kill it.",
        "dialogue_time": 5,
        "item": "Ectoplasm",
        "number": 1,
        "reward_item": "Church Key",
        "reward_num": 1
    },
    "100": {
        "dialogue": "Help, I've lost my helmet. Get it for me so I can keep mining and I'll give you a key.",
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
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

def calculate_distance(pos_1, pos_2):
    """Returns distance between two positions"""
    distance_x = pos_1[0] - pos_2[0]
    distance_y = pos_1[1] - pos_2[1]
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

        # Image sequences
        self.cur_texture = FIRST_TEXTURE
        self.scale = CHARACTER_SCALING

        main_path = f"{MAIN_PATH}/assets/{category_folder}/{sprite_folder}"

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
        self.type = None

    def update_animation(self, delta_time: float = FRAMERATE):
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
        self.type = None
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
        self.shape = shape
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_dead = False
        self.dying = False

    def update_animation(self, delta_time: float = FRAMERATE):

        # Change direction if needed
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

        # Death animation
        if self.is_dead:
            if not self.dying:
                self.cur_texture = FIRST_TEXTURE
                self.dying = True
            if (
                self.cur_texture 
                > 
                self.death_frames*ANIM_MULT["Player1"]["Death"]-INDEX_OFFSET
                ):
                self.cur_texture = FIRST_TEXTURE
                self.is_dead = False
                  
            self.texture = self.death_textures[
                self.cur_texture // ANIM_MULT["Player1"]["Death"]
                ][self.facing_direction]
            self.cur_texture += UNIT_INCREMENT
            return

        # Climbing animation
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
            self.idle_frames*ANIM_MULT["Player1"]["Walk"]
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
        if self.wave == False:
            self.texture = self.idle_textures[
                FIRST_TEXTURE
                ][self.facing_direction]

        # Wave animation
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
        Also initalises the drop attribute is the item the enemy drops
        upon death.
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
        super().__init__()
        self.background = arcade.load_texture()
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

        self.window.set_mouse_visible = False


        # Variables to check which key is being pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.interact = False
        self.swing_knife = False

        # Player stats (health, energy, etc)
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
        self.quests = {}
        self.in_quest = False
        self.not_complete_time = NOTHING
        self.finished_quest = None
        self.latest_quest = None
        self.check_quest = None
        self.completed_quests = []
        self.quest_ended = False

        # Sensing variables
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
                if "boundary_left" in enemy_object.properties:
                    enemy.boundary_left = enemy_object.properties[
                        "boundary_left"]
                    
                if "boundary_right" in enemy_object.properties:
                    enemy.boundary_right = enemy_object.properties[
                        "boundary_right"
                        ]
                if "drop" in enemy_object.properties:
                    enemy.drop = enemy_object.properties["drop"]
                if "can_kill" in enemy_object.properties:
                    enemy.can_kill = enemy_object.properties["can_kill"]
                self.map_has_enemies = True
                self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)
        except:
            self.map_has_enemies = False
            

        # Add inanimate objects
        # Try to add in end portal/s
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
                orb.type = orb_object.properties["type"]
                self.map_has_orbs = True
                self.scene.add_sprite(LAYER_NAME_ORBS, orb)
        except:
            self.map_has_orbs = False

        # Try to add in collectibles which include quests and secrets
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
                if collectible_type == "Apple":
                    collectible = Apple()
                if collectible_type == "Card":
                    collectible = Card()
                if collectible_type == "Document":
                    collectible = Document()
                if collectible_type == "Key":
                    collectible = Key()
                    collectible.id = collectible_object.properties["unlocks"]
                if collectible_type == "Helmet":
                    collectible = Helmet()
                if collectible_type == "Rainbow Rock":
                    collectible = RainbowRock()
                if collectible_type == "Secret":
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
        try:
            self.text_layer = self.tile_map.object_lists[LAYER_NAME_TEXT]
        except:
            pass

        # Add all warp doors into the a list of door information
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
                locked_door.id = locked_door_object.properties["id"]
                self.map_has_locked_doors = True
                self.scene.add_sprite(LAYER_NAME_LOCKED_DOORS, locked_door)
        except:
            self.map_has_locked_doors = False

        # Setup GUI Layers

        # Setup energy bar
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
        self.scene.draw(pixelated=True)

        # Actually draw the floating text
        
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
        if self.in_quest:
            try:
                if self.latest_quest["dialogue_time"] > NOTHING:
                    arcade.draw_rectangle_filled(
                        self.latest_quest["villager_pos"][0],
                        self.latest_quest["villager_pos"][1]+1.5*TILE_SCALING*self.tile_map.tile_width,
                        len(self.start_dialogue)*10+10,
                        20,
                        WHITE,
                    )
                    arcade.draw_text(
                        self.start_dialogue,
                        self.latest_quest["villager_pos"][0],
                        self.latest_quest["villager_pos"][1]+1.5*TILE_SCALING*self.tile_map.tile_width,
                        BLACK,
                        15,
                        anchor_x="center",
                        anchor_y="center",
                    )
            except KeyError:
                pass
        
        # If quest not complete then draw this
        if self.not_complete_time > 0:
            arcade.draw_rectangle_filled(
                self.check_quest["villager_pos"][0],
                self.check_quest["villager_pos"][1]+1.5*TILE_SCALING*self.tile_map.tile_width,
                380,
                20,
                WHITE
            )
            arcade.draw_text(
                "Bruh you're not done yet",
                self.check_quest["villager_pos"][0],
                self.check_quest["villager_pos"][1]+1.5*TILE_SCALING*self.tile_map.tile_width,
                BLACK,
                15,
                anchor_x="center",
                anchor_y="center",
            )

        # If quest complete draw this
        if self.finished_quest != None:
            if self.finished_quest["dialogue_time"] > 0:
                arcade.draw_rectangle_filled(
                    self.finished_quest["villager_pos"][0],
                    self.finished_quest["villager_pos"][1]+1.5*TILE_SCALING*self.tile_map.tile_width,
                    280,
                    35,
                    WHITE,
                )
                arcade.draw_text(
                    "Thanks, here is your reward",
                    self.finished_quest["villager_pos"][0],
                    self.finished_quest["villager_pos"][1]+1.5*TILE_SCALING*self.tile_map.tile_width,
                    BLACK,
                    15,
                    anchor_x="center",
                    anchor_y="center",
                )

        # If key missing draw this
        if self.missing_key_text > 0:
            arcade.draw_rectangle_filled(
                self.player_sprite.center_x,
                self.player_sprite.center_y+1.5*TILE_SCALING*self.tile_map.tile_height,
                125,
                20,
                WHITE,
            )
            arcade.draw_text(
                "Missing key",
                self.player_sprite.center_x,
                self.player_sprite.center_y+1.5*TILE_SCALING*self.tile_map.tile_height,
                BLACK,
                15,
                anchor_x = "center",
                anchor_y="center"
            )

        # If secret found then draw this
        if self.secret_found_text > 0:
            arcade.draw_rectangle_filled(
                self.player_sprite.center_x,
                self.player_sprite.center_y+1.5*TILE_SCALING*self.tile_map.tile_height,
                125,
                20,
                WHITE,
            )
            arcade.draw_text(
                "Secret Found",
                self.player_sprite.center_x,
                self.player_sprite.center_y+1.5*TILE_SCALING*self.tile_map.tile_height,
                BLACK,
                15,
                anchor_x = "center",
                anchor_y="center"
            )

        # Activate the GUI camera to draw GUI elements
        self.gui_camera.use()

        # Draw GUI content

        # Display current energy
        self.gui_scene.draw(pixelated=True)

        # If interact is possible then draw this text
        if self.can_interact:
            arcade.draw_rectangle_filled(
                SCREEN_WIDTH*0.8,
                50,
                200,
                20,
                BLACK,
            )
            arcade.draw_text(
                "Press 'f' to interact",
                SCREEN_WIDTH*0.8,
                50,
                WHITE,
                18,
                anchor_x="center",
                anchor_y="center"
            )
        
        # If in quest then draw the current quest progress
        if self.in_quest:
            count = 0
            for id, info in self.quests.items():
                arcade.draw_rectangle_filled(
                    SCREEN_WIDTH-24*TILE_SCALING,
                    SCREEN_HEIGHT-(60+count*9)*TILE_SCALING,
                    250,
                    30,
                    WHITE
                )
                arcade.draw_text(
                    f"{info['quest_item']}: {self.inventory_quest[id]['number']}/{info['num_needed']}",
                    SCREEN_WIDTH-24*TILE_SCALING,
                    SCREEN_HEIGHT-(60+count*9)*TILE_SCALING,
                    BLACK,
                    20,
                    anchor_x="center",
                    anchor_y="center"
                )
                count += 1
        
        
        
        
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_WALK_SPEED
            elif self.shape == 2:
                self.fly_speed += (self.thrust - GRAVITY)*self.delta_time
            else:
                if (
                    self.physics_engine.can_jump(y_distance=10)
                    and not self.jump_needs_reset
                ):
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
                    self.jump_needs_reset = True
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_WALK_SPEED
            elif self.shape == 2:
                self.fly_speed -= (self.thrust + 4*GRAVITY)*self.delta_time

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_WALK_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_WALK_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
            if self.shape == 2:
                self.is_flying = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
            if self.shape == 2:
                self.is_flying = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.F:
            self.interact = True

        if self.energy >= 3:
            if key == arcade.key.KEY_1 and self.shape != 0:
                player_pos = (self.player_sprite.center_x, self.player_sprite.center_y)
                self.shape = 0
                self.energy -= 3
                self.scene[LAYER_NAME_PLAYER].remove(self.player_sprite)
                self.player_sprite = PlayerCharacter(self.shape)
                self.player_sprite.center_x = player_pos[0]
                self.player_sprite.center_y = player_pos[1]

                self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
                try:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        ladders=self.scene[LAYER_NAME_LADDERS],
                        walls=[self.scene[LAYER_NAME_PLATFORMS], self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]],
                    )
                except:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        ladders=self.scene[LAYER_NAME_LADDERS],
                        walls=self.scene[LAYER_NAME_PLATFORMS],
                    )
            if key == arcade.key.KEY_2 and self.shape != 1:
                player_pos = (self.player_sprite.center_x, self.player_sprite.center_y)
                self.shape = 1
                self.energy -= 3
                self.scene[LAYER_NAME_PLAYER].remove(self.player_sprite)
                self.player_sprite = PlayerCharacter(self.shape)
                self.player_sprite.center_x = player_pos[0]
                self.player_sprite.center_y = player_pos[1]

                self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
                try:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=[self.scene[LAYER_NAME_PLATFORMS], self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]],
                    )
                except:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=self.scene[LAYER_NAME_PLATFORMS],
                    )
            if key == arcade.key.KEY_3 and self.shape != 2:
                player_pos = (self.player_sprite.center_x, self.player_sprite.center_y)
                self.shape = 2
                self.energy -= 3
                self.scene[LAYER_NAME_PLAYER].remove(self.player_sprite)
                self.player_sprite = PlayerCharacter(self.shape)
                self.player_sprite.center_x = player_pos[0]
                self.player_sprite.center_y = player_pos[1]

                self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)
                try:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=[self.scene[LAYER_NAME_PLATFORMS], self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]],
                    )
                except:
                    self.physics_engine = arcade.PhysicsEnginePlatformer(
                        self.player_sprite,
                        platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                        gravity_constant=GRAVITY,
                        walls=self.scene[LAYER_NAME_PLATFORMS],
                    )

        if key == arcade.key.Q:
            if self.energy < 3:
                self.energy += 1

        if key == arcade.key.R:
            self.player_sprite.center_x = self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
            self.player_sprite.center_y = self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y
        
        if key == arcade.key.Z and self.inventory_other["002"]["number"] > 0 and self.can_knife:
            self.swing_knife = True
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
            if self.shape == 2:
                self.is_flying = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            if self.shape == 2:
                self.is_flying = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.F:
            self.interact = False

        if key == arcade.key.Z and self.inventory_other["002"]["number"] > 0:
            self.swing_knife = False

        self.process_keychange()

    def center_camera_to_player(self, speed=0.2):
        screen_center_x = self.camera.scale * (self.player_sprite.center_x - (self.camera.viewport_width / 2))
        screen_center_y = self.camera.scale * (self.player_sprite.center_y - (self.camera.viewport_height / 2))
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = (screen_center_x, screen_center_y)

        self.camera.move_to(player_centered, speed)

    def activate_quest(self, villager):
        """Function which handles the quest activation."""
        quest = QUEST_REF[villager.id]
        self.start_dialogue = quest["dialogue"]
        self.quests[villager.id] = {
            "quest_id": villager.id,
            "villager_pos": [villager.center_x, villager.center_y],
            "quest_item": quest["item"],
            "num_needed": quest["number"],
            "dialogue_time": quest["dialogue_time"],
        }
        self.latest_quest = self.quests[villager.id]

    def check_quest_complete(self, villager):
        if self.inventory_quest[villager.id]["number"] < self.quests[villager.id]["num_needed"]:
            self.check_quest = self.quests[villager.id]
            self.not_complete_time = 2
        else:
            self.end_quest(villager)
    
    def end_quest(self, villager):
        self.finished_quest = self.quests.pop(villager.id)
        self.finished_quest["dialogue_time"] = 2
        self.quest_ended = True
        self.completed_quests.append(villager.id)
        self.inventory_quest[villager.id]["number"] -= self.finished_quest["num_needed"]
        if QUEST_REF[villager.id]["reward_item"] != "Energy":
            self.inventory_other[villager.id]["number"] += QUEST_REF[villager.id]["reward_num"]
        else:
            if self.energy < 3:
                self.energy += QUEST_REF[villager.id]["reward_num"]

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Reset the interactable text
        self.can_interact = False

        self.delta_time = delta_time
        # Move the player
        self.physics_engine.update()

        # If blaze shape then do helicopter physics
        if self.shape == 2:
            self.player_sprite.change_y = self.fly_speed
            if not self.is_flying:
                self.fly_speed -= 4*GRAVITY*delta_time
            if self.physics_engine.can_jump() and self.time_since_ground > 1:
                self.fly_speed = 0
                self.time_since_ground = 0
            self.time_since_ground += delta_time
                

        # Update animations for the player
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        # Check if knife is being swung
        if self.can_knife:
            if self.swing_knife:
                knife = Knife()
                if self.player_sprite.facing_direction == RIGHT_FACING:
                    knife.center_x = self.player_sprite.center_x + 0.5*TILE_SCALING*self.tile_map.tile_width
                    knife.facing_direction = RIGHT_FACING
                else:
                    knife.center_x = self.player_sprite.center_x - 0.5*TILE_SCALING*self.tile_map.tile_width
                    knife.facing_direction = LEFT_FACING
                knife.center_y = self.player_sprite.center_y
                    
                self.scene.add_sprite(LAYER_NAME_KNIFE, knife)
                self.swing_knife = False
                self.can_knife = False
        else:
            self.knife_timer += delta_time
            if self.knife_timer >= KNIFE_COOLDOWN:
                self.can_knife = True
                self.knife_timer = 0    

        # Remove knife after it has finished its swing
        # If an error occurs that just means the knife doesn't exist and we can ignore.
        try:
            for knife in self.scene[LAYER_NAME_KNIFE]:
                if self.player_sprite.facing_direction == RIGHT_FACING:
                    knife.center_x = self.player_sprite.center_x + 0.5*TILE_SCALING*self.tile_map.tile_width
                    knife.facing_direction = RIGHT_FACING
                else:
                    knife.center_x = self.player_sprite.center_x - 0.5*TILE_SCALING*self.tile_map.tile_width
                    knife.facing_direction = LEFT_FACING
                knife.center_y = self.player_sprite.center_y
                knife.update_animation(delta_time)
                if knife.swing_finished:
                    self.scene[LAYER_NAME_KNIFE].remove(knife)
        except:
            pass

        # Update animations for other things
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_PLAYER,
                LAYER_NAME_BACKGROUND,
            ] + self.available_layers
        )

        # Update moving platforms and enemies
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


        # Update villagers
        try:
            for villager in self.scene[LAYER_NAME_VILLAGERS]:
                villager.update(player_pos=(self.player_sprite.center_x, self.player_sprite.center_y), tile_map=self.tile_map)
        except:
            pass

        # See if the enemy hit a boundary and needs to reverse direction.
        try:
            for enemy in self.scene[LAYER_NAME_ENEMIES]:
                if (
                    enemy.boundary_right
                    and enemy.right > enemy.boundary_right*TILE_SCALING*self.tile_map.tile_width
                    and enemy.change_x > 0
                ):
                    enemy.change_x *= -1

                if (
                    enemy.boundary_left
                    and enemy.left < enemy.boundary_left*TILE_SCALING*self.tile_map.tile_width
                    and enemy.change_x < 0
                ):
                    enemy.change_x *= -1
        except:
            pass
        

        # Only try to check interaction with villagers if in human shape
        if self.shape == 0:
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
                    if self.interact:
                        for villager in self.scene[LAYER_NAME_VILLAGERS]:
                            if villager.id == interactable_villager:
                                if villager.id not in self.completed_quests:
                                    if villager.id not in self.quests.keys():
                                        villager.wave = True
                                        self.activate_quest(villager)
                                    elif self.latest_quest["dialogue_time"] <= 0:
                                        self.check_quest_complete(villager)
                                else:
                                    villager.wave = True
            except:
                pass

        # Check if interaction possible with door
        for id, info in self.doors.items():
            if calculate_distance(self.player_sprite.position, info["pos"]) < 1*TILE_SCALING*self.tile_map.tile_width:
                self.interactable_door = id
                self.can_interact = True
                break
            self.interactable_door = None
        
        # Level changing mechanics
        # Check if actually interacting with door
        if self.interact and self.can_interact and self.interactable_door != None:
            if self.doors[self.interactable_door]["key_req"] == "None":
                self.level = self.doors[self.interactable_door]["warp"]
                self.spawnpoint = self.doors[self.interactable_door]["dest"]
                self.interact = False
                self.setup()
                return
            else:
                has_key = False
                for item in self.inventory_other.values():
                    if item["name"] == self.doors[self.interactable_door]["key_req"] and item["number"] > 0:
                        has_key = True
                        break
                if has_key:
                    self.level = self.doors[self.interactable_door]["warp"]
                    self.spawnpoint = self.doors[self.interactable_door]["dest"]
                    self.interact = False
                    self.setup()
                    return
                else:
                    self.missing_key_text = 2
                            
        # Check if interaction possible with statue
        try:
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_STATUES])) > 0:
                self.can_interact = True
        except:
            pass
        

        # Check for collisions with the statue
        try:
            if self.interact:
                player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_STATUES])
                for collision in player_collision_list:
                    if self.prev_spawnpoint != None:
                        self.scene[LAYER_NAME_STATUES].append(self.prev_spawnpoint)
                        self.scene[LAYER_NAME_SPAWNPOINT].clear()
                    if abs(collision.center_x - self.player_sprite.center_x) < self.tile_map.tile_width * TILE_SCALING * 2:
                        self.spawnpoint = (collision.center_x / (self.tile_map.tile_width * TILE_SCALING), collision.center_y / (self.tile_map.tile_width * TILE_SCALING) - 1)
                        self.scene[LAYER_NAME_SPAWNPOINT].append(collision)
                        self.scene[LAYER_NAME_STATUES].remove(collision)
                        self.prev_spawnpoint = collision
                        self.energy = 3
                self.interact = False
        except:
            pass

        # Check for collisions with energy orbs
        try:
            if self.energy < 3:
                player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_ORBS])
                for collision in player_collision_list:
                    if collision.type == "Energy":
                        self.energy += 1
                        self.scene[LAYER_NAME_ORBS].remove(collision)
        except:
            pass
        
        # Check for collisions with keys or secrets
        try:
            player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_COLLECTIBLES])
            for collision in player_collision_list:
                if collision.type == "Key":
                    self.keys_obtained.append(collision.id)
                    self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
                if collision.type == "Secret":
                    self.secret_found_text = 2
                    print("This works")
                    self.secrets_found.append(collision.name)
                    print("This doesn't")
                    self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)   

        except:
            pass

        # Check for collisions with locked door
        try:
            player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_LOCKED_DOORS])
            for collision in player_collision_list:
                if str(collision.id) in self.keys_obtained:
                    for door_barrier in self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED]:
                        self.scene[LAYER_NAME_DOOR_BARRIERS_OPEN].append(door_barrier)
                        self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED].remove(door_barrier)
                    collision.open = True
                else:
                    self.missing_key_text = 2
                    for door_barrier in self.scene[LAYER_NAME_DOOR_BARRIERS_OPEN]:
                        self.scene[LAYER_NAME_DOOR_BARRIERS_CLOSED].append(door_barrier)
                        self.scene[LAYER_NAME_DOOR_BARRIERS_OPEN].remove(door_barrier)

        except:
            pass

        # Quest item collision processing
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
                player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_COLLECTIBLES])
                for collision in player_collision_list:
                    if quest_req_apples:
                        # Check for collisions with apples
                        if collision.type == "Apple":
                            self.inventory_quest[quest_id_apples]["number"] += 1
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
                    if quest_req_cards:
                        # Check for collisions with cards
                        if collision.type == "Card":
                            self.inventory_quest[quest_id_cards]["number"] += 1
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
                    if quest_req_documents:
                        # Check for collisions with documents
                        if collision.type == "Document":
                            self.inventory_quest[quest_id_documents]["number"] += 1
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
                    if quest_req_helmets:
                        # Check for collisions with helmets
                        if collision.type == "Helmet":
                            self.inventory_quest[quest_id_helmets]["number"] += 1
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
                    if quest_req_rainbow_rocks:
                        # Check for collisions with rainbow rocks
                        if collision.type == "Rainbow Rock":
                            self.inventory_quest[quest_id_rainbow_rocks]["number"] += 1
                            self.scene[LAYER_NAME_COLLECTIBLES].remove(collision)
            except:
                pass


        # Update energy bar
        try:
            for energy_bar in self.gui_scene[LAYER_NAME_ENERGY]:
                energy_bar.texture = arcade.load_texture(f"{MAIN_PATH}/assets/GUI/Energy/{self.energy}.png")
        except:
            pass

        # Check for stabbing of enemy
        try:
            knife_collision_list = arcade.check_for_collision_with_list(self.scene[LAYER_NAME_KNIFE][0], self.scene[LAYER_NAME_ENEMIES])
            for collision in knife_collision_list:
                if collision.can_kill:
                    for id, info in self.inventory_quest.items():
                        if collision.drop == info["name"]:
                            self.inventory_quest[id]["number"] += 1
                    self.scene[LAYER_NAME_ENEMIES].remove(collision)
        
        except:
            pass

        # Check for collisions with enemies
        try:
            player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_ENEMIES])
            if len(player_collision_list) > 0:
                if self.cooldown <= 0:
                    self.health -= 1
                    self.cooldown = 1
                    self.player_sprite.change_y = PLAYER_JUMP_SPEED
        except:
            pass

        # Update health bar
        try:
            for health_bar in self.gui_scene[LAYER_NAME_HEALTH]:
                health_bar.texture = arcade.load_texture(f"{MAIN_PATH}/assets/GUI/Health/{self.health}.png")
        except:
            pass

        # Reveal tunnels/cave when player approaches
        try:
            for tile in self.scene[LAYER_NAME_CAVE]:
                distance_to_player = calculate_distance([self.player_sprite.center_x, self.player_sprite.center_y], [tile.center_x, tile.center_y])
                if distance_to_player < 10*TILE_SCALING*self.tile_map.tile_width:
                    tile.alpha = 255*(max(distance_to_player-5*TILE_SCALING*self.tile_map.tile_width, 0)) / (10*TILE_SCALING*self.tile_map.tile_width)
        except:
            pass
        

        # Once death animation over respawn
        if self.player_sprite.dying and self.player_sprite.dying != self.player_sprite.is_dead:
            self.player_sprite.center_x = self.tile_map.tile_width * TILE_SCALING * self.spawnpoint[0]
            self.player_sprite.center_y = self.tile_map.tile_height * TILE_SCALING * self.spawnpoint[1]
            
            self.player_sprite.dying = False

        # Check for collision with death layer (spikes etc)
        try:
            if len(arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_DEATH])) > 0 and not self.player_sprite.is_dead:
                self.player_sprite.is_dead = True
        except:
            pass
        
        # Run player death animation
        if self.player_sprite.center_y < 0 or self.health <= 0 and not self.player_sprite.is_dead:
            
            self.player_sprite.is_dead = True
        
        if self.player_sprite.is_dead:
            self.health = 3
            self.energy = 3
            self.fly_speed = 0

            
        if len(self.quests) > 0:
            self.in_quest = True
        else:
            self.in_quest = False

        # Reducing all of the timer variables
        if self.cooldown > 0:
            self.cooldown -= delta_time
        else:
            self.cooldown = 0
        
        if self.not_complete_time > 0:
            self.not_complete_time -= delta_time
        else:
            self.not_complete_time = 0

        if self.missing_key_text > 0:
            self.missing_key_text -= delta_time
        else:
            self.missing_key_text = 0
        
        if self.secret_found_text > 0:
            self.secret_found_text -= delta_time
        else:
            self.secret_found_text = 0

        # If these variables exist, i.e. after a quest has been started,
        # Run the timer code
        # Otherwise, just ignore it
        try:
            if self.latest_quest["dialogue_time"] > 0:
                self.latest_quest["dialogue_time"] -= delta_time
            else:
                self.latest_quest["dialogue_time"] = 0
            
            if self.finished_quest["dialogue_time"] > 0:
                self.finished_quest["dialogue_time"] -= delta_time
            else:
                self.finished_quest["dialogue_time"] = 0

            # Once the timer for the quest end dialogue goes to 0, 
            # delete the finished quest.
            if self.finished_quest["dialogue_time"] <= 0 and self.quest_ended:
                self.finished_quest = None
                self.quest_ended = False
  
        except:
            pass

        # Check for collision with goal/warp portal
        try:
            player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_GOAL])
            for collision in player_collision_list:
                if collision.warp == "4":
                    end_view = EndScreen()
                    self.window.show_view(end_view)
                else:
                    self.level = collision.warp
                    self.spawnpoint = collision.dest
                    self.setup()
                return
        except:
            pass
        self.center_camera_to_player()

# Main Program

def main():
    """Main Function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    #start_view.setup()
    arcade.run()

# Things that run

if __name__ == "__main__":
    main()