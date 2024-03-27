import arcade, os, random, math

# Defining constants

MAIN_PATH = os.path.dirname(os.path.abspath(__file__))

# Window Settings
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Ataraxia V1"

# Sprite Scaling
CHARACTER_SCALING = 5
TILE_SCALING = 5
COLLECTIBLE_SCALING = 2

# Sprite facing direction
RIGHT_FACING = 0
LEFT_FACING = 1

# Layer names
# Character Layers
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_VILLAGERS = "Villagers"

# Object Layers
LAYER_NAME_ORBS = "Orbs"
LAYER_NAME_TEXT = "Text"

# Tile Layers
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_STATUES = "Statues"
LAYER_NAME_SPAWNPOINT = "Current Statue"
LAYER_NAME_GOAL = "Goal"
LAYER_NAME_CAVE = "Cave"

# Physics things
GRAVITY = 1
PLAYER_WALK_SPEED = 10
PLAYER_RUN_SPEED = 15
PLAYER_JUMP_SPEED = 20

# Player spawnpoints
PLAYER_START_X = 3
PLAYER_START_Y = 18

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
    distance_x = pos_1[0] - pos_2[0]
    distance_y = pos_1[1] - pos_2[1]
    return math.sqrt(distance_x**2 + distance_y**2)


# Entity superclass
class Entity(arcade.Sprite):
    """Overarching things for characters"""

    def __init__(self, category_folder, sprite_folder, available_anims: list):
        super().__init__()

        # Default right facing
        self.facing_direction = RIGHT_FACING

        # Image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        main_path = f"{MAIN_PATH}/assets/{category_folder}/{sprite_folder}"

        if "Idle" in available_anims:
            # Idle frames
            frame_num = 0
            for path in os.listdir(f"{main_path}/idle"):
                frame_num += 1

            self.idle_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/idle/{i}.png")
                self.idle_textures.append(texture)

        if "Jump" in available_anims:
            # Jumping and falling sprites
            frame_num = 0
            for path in os.listdir(f"{main_path}/jump"):
                frame_num += 1

            self.jump_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/jump/{i}.png")
                self.jump_textures.append(texture)

            frame_num = 0
            for path in os.listdir(f"{main_path}/fall"):
                frame_num += 1

            self.fall_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/fall/{i}.png")
                self.fall_textures.append(texture)

        if "Walk" in available_anims:
            # Walking frames
            frame_num = 0
            for path in os.listdir(f"{main_path}/walk"):
                frame_num += 1

            print(frame_num)
            self.walk_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/walk/{i}.png")
                self.walk_textures.append(texture)

        if "Climb" in available_anims:
        # Climbing frames
            frame_num = 0
            for path in os.listdir(f"{main_path}/climb"):    
                frame_num += 1


            self.climbing_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/climb/{i}.png")
                self.climbing_textures.append(texture)

        if "Wave" in available_anims:
            frame_num = 0
            for path in os.listdir(f"{main_path}/wave"):
                frame_num += 1

            self.wave_textures = []
            for i in range(frame_num):
                texture = load_texture_pair(f"{main_path}/wave/{i}.png")
                self.wave_textures.append(texture)

        # Set initial texture
        self.texture = self.idle_textures[0][0]

        # Set hitbox
        self.set_hit_box(self.texture.hit_box_points)

# Collectible Objects Template class

class Collectible(Entity):
    """Template for collectible items like orbs and potions and
weapons and stuff."""
    def __init__(self, sprite_folder):
        # Inherit from parent class (Entity)
        super().__init__("InanimateObjects", sprite_folder, ["Idle"])
        self.scale = COLLECTIBLE_SCALING


# Energy Orb class

class Orb(Collectible):
    """Energy Orb Sprite"""

    def __init__(self):
        # Inherit from parent class (Collectible)
        super().__init__("EnergyOrb")
        self.type = None

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 23:
            self.cur_texture = 0
        self.texture = self.idle_textures[self.cur_texture // 12][0]
        return



# Player Class

class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self, shape):

        if shape == 0:
            available_anims = ["Idle", "Walk", "Jump", "Climb"]
        else:
            available_anims = ["Idle", "Walk", "Jump"]
        # Inherit from parent class (Entity)
        super().__init__("Friendly", f"Player{shape+1}", available_anims)

        # Track state
        self.shape = shape
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        if shape == 1:
            self.set_hit_box([[-7, -7], [7, -7], [7, -1], [-7, -1]])
            print(self.get_hit_box())

    def update_animation(self, delta_time: float = 1 / 60):

        # Change direction if needed
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Hierarchy of animations:
        # Climbing, Jumping, Idle, Walking

        # Climbing animation
        if self.shape == 0:
            if self.is_on_ladder:
                self.climbing = True
            if not self.is_on_ladder and self.climbing:
                self.climbing = False
            if self.climbing and abs(self.change_y) > 1:
                self.cur_texture += 1
                if self.cur_texture > 31:
                    self.cur_texture = 0
            if self.climbing:
                print(len(self.climbing_textures))
                self.texture = self.climbing_textures[self.cur_texture // 4][self.facing_direction]
                return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            if self.shape == 2:
                self.cur_texture += 1
                if self.cur_texture > 23:
                    self.cur_texture = 0
                self.texture = self.jump_textures[self.cur_texture // 4][self.facing_direction]
            else:
                self.texture = self.jump_textures[0][self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            if self.shape == 2:
                self.cur_texture += 1
                if self.cur_texture > 23:
                    self.cur_texture = 0
                self.texture = self.fall_textures[self.cur_texture // 4][self.facing_direction]
            else:
                self.texture = self.fall_textures[0][self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.cur_texture += 1
            if self.shape == 2:
                if self.cur_texture > 23:
                    self.cur_texture = 0
                self.texture = self.idle_textures[self.cur_texture // 4][self.facing_direction]
            else:

                if self.cur_texture > 15:
                    self.cur_texture = 0
                self.texture = self.idle_textures[self.cur_texture // 8][self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.shape == 2:
            if self.cur_texture > 23:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture // 4][self.facing_direction]
        else:
            if self.cur_texture > 15:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture // 4][self.facing_direction]

# Villager NPC

class DefaultVillager(Entity):
    """Basic Villager Sprite"""
    def __init__(self, villager_id):

        # Inherit from parent class (Entity)
        super().__init__("Friendly", f"Villager{villager_id}", ["Idle", "Wave"])

        # Track states
        self.id = villager_id
        self.wave = False
        self.interactable = False

    def update_animation(self, delta_time: float = 1 / 60):
        #print(self.wave_textures)
        # Idle animation

        if self.wave == False:
            self.texture = self.idle_textures[0][self.facing_direction]

        # Wave animation

        elif self.wave == True:
            self.texture = self.wave_textures[0][self.facing_direction]
        return

    def update(self, player_pos, tile_map, delta_time: float = 1 / 60):
        if abs(self.center_x - player_pos[0]) < 1*TILE_SCALING*tile_map.tile_width and abs(self.center_y-player_pos[1]) < 0.5*TILE_SCALING*tile_map.tile_height:
            self.interactable = True
        else:
            self.interactable = False
        return

# Menu Screen
class MainMenu(arcade.View):
    """
    The main menu screen displayed at the beginning.
    """

    def on_show_view(self):
        """Called when showing this view."""
        arcade.set_background_color((188, 188, 255))

    def on_draw(self):
        """Display the menu"""
        self.clear()
        arcade.draw_text(
            "Click to start game",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            (0, 0, 0),
            font_size = 30,
            anchor_x = "center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the actual game view."""
        game_view = GameView()
        self.window.show_view(game_view)



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
        self.running = False
        self.jump_needs_reset = False
        self.interact = False

        # Player stats (health, energy, etc)
        self.health = 100
        self.energy = 0
        self.shape = 0
        self.fly_speed = 0
        self.thrust = 10

        # Sensing variables
        self.can_interact = False
        self.is_flying = False

        # Control variables
        self.delta_time = 0
        self.time_since_ground = 0

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
        self.level = 1.1

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
        }

        # Read in Tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        
        # Initialise new scene with the tilemap
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Add in villagers
        villagers_layer = self.tile_map.object_lists[LAYER_NAME_VILLAGERS]
        for villager_object in villagers_layer:
            cartesian = self.tile_map.get_cartesian(
                villager_object.shape[0], villager_object.shape[1]
            )
            villager = DefaultVillager(int(villager_object.properties["id"][2])+1)
            villager.center_x = math.floor(
                (cartesian[0]+0.5) * TILE_SCALING * self.tile_map.tile_width
            )
            villager.center_y = math.floor(
                (cartesian[1]+0.5) * (self.tile_map.tile_height * TILE_SCALING)-TILE_SCALING
            )

            self.scene.add_sprite(LAYER_NAME_VILLAGERS, villager)

        # Add in energy orbs
        orbs_layer = self.tile_map.object_lists[LAYER_NAME_ORBS]
        for orb_object in orbs_layer:
            cartesian = self.tile_map.get_cartesian(
                orb_object.shape[0], orb_object.shape[1]
            )
            orb = Orb()
            orb.center_x = math.floor(
                (cartesian[0]+0.5) * TILE_SCALING * self.tile_map.tile_width
            )
            orb.center_y = math.floor(
                (cartesian[1]+0.5) * (self.tile_map.tile_height * TILE_SCALING)-TILE_SCALING
            )
            orb.type = orb_object.properties["type"]
            self.scene.add_sprite(LAYER_NAME_ORBS, orb)
        
        self.text_layer = self.tile_map.object_lists[LAYER_NAME_TEXT]

        #text_layer = self.tile_map.object_lists[LAYER_NAME_TEXT]
        #for text_object in text_layer:
        #    cartesian = self.tile_map.get_cartesian(
        #        text_object.shape[0], text_object.shape[1]
        #    )


        # Setup player at specific coordinates
        self.player_sprite = PlayerCharacter(self.shape)
        self.player_sprite.center_x = (
            self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y
        )

        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Add in enemies


        arcade.set_background_color((99, 245, 255))

        # Set background colour
        #if self.tile_map.background_color:
        #    arcade.set_background_color(self.tile_map.background_color)

        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        """Render the screen"""

        # Clear screen contents (only background remains)
        self.clear()

        # Activate game camera
        self.camera.use()
        
        
        # Draw the scene
        self.scene.draw(pixelated=True)

        for text in self.text_layer:
            cartesian = self.tile_map.get_cartesian(
                text.shape[0], text.shape[1]
            )
            if text.properties["colour"] == "1":
                colour = (255, 255, 255)
            else:
                colour = (0, 0, 0)
            arcade.draw_text(
                text.properties["text"],
                cartesian[0]*TILE_SCALING*self.tile_map.tile_width,
                cartesian[1]*TILE_SCALING*self.tile_map.tile_height,
                colour,
                14,
            )

        # Activate the GUI camera to draw GUI elements
        self.gui_camera.use()

        # Draw GUI content

        # Display current energy
        current_energy = f"Energy: {self.energy}/3"
        arcade.draw_text(
            current_energy,
            10,
            50,
            (255, 255, 255),
            18,
        )

        # If interact is possible then draw this text
        if self.can_interact:
            arcade.draw_text(
                "Press 'f' to interact",
                SCREEN_WIDTH*0.8,
                50,
                (255, 255, 255),
                18,

            )
        
        
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
            if self.running:
                self.player_sprite.change_x = PLAYER_RUN_SPEED
            else:
                self.player_sprite.change_x = PLAYER_WALK_SPEED
        elif self.left_pressed and not self.right_pressed:
            if self.running:
                self.player_sprite.change_x = -PLAYER_RUN_SPEED
            else:
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

        if key == arcade.key.LSHIFT:
            self.running = True

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
                self.physics_engine = arcade.PhysicsEnginePlatformer(
                    self.player_sprite,
                    platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
                    gravity_constant=GRAVITY,
                    walls=self.scene[LAYER_NAME_PLATFORMS],
                )

        if key == arcade.key.Q:
            self.energy += 1
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

        if key == arcade.key.LSHIFT:
            self.running = False

        if key == arcade.key.F:
            self.interact = False

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

    def on_update(self, delta_time):
        """Movement and game logic"""

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

        # Update animations for other things
        self.scene.update_animation(
            delta_time,
            [
                LAYER_NAME_PLAYER,
                LAYER_NAME_BACKGROUND,
                LAYER_NAME_VILLAGERS,
                LAYER_NAME_ORBS
            ],
        )

        # Update moving platforms
        self.scene.update(
            [
                LAYER_NAME_MOVING_PLATFORMS,
                #LAYER_NAME_VILLAGERS,
            ],
        )

        # Update villagers
        for villager in self.scene[LAYER_NAME_VILLAGERS]:
            villager.update(player_pos=(self.player_sprite.center_x, self.player_sprite.center_y), tile_map=self.tile_map)

        if self.shape == 0:
            interactable_villager = None
            # Check if in range of villager
            for villager in self.scene[LAYER_NAME_VILLAGERS]:
                if villager.interactable:
                    self.can_interact = True
                    interactable_villager = villager.id
                    break
                else:
                    villager.wave = False
                    self.can_interact = False

            # Check for interaction with villager
            if self.interact:
                for villager in self.scene[LAYER_NAME_VILLAGERS]:
                    if villager.id == interactable_villager:
                        villager.wave = True
                        self.energy += 1
                        print("please")

        # Check for collisions with the statue
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
                    print(f"New spawnpoint at {self.spawnpoint}")
                    self.energy = 3
            self.interact = False

        # Check for collisions with energy orbs
        player_collision_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_ORBS])
        for collision in player_collision_list:
            if collision.type == "Energy":
                self.energy += 1
                self.scene[LAYER_NAME_ORBS].remove(collision)
        
        # Reveal tunnels/cave when player approaches
        for tile in self.scene[LAYER_NAME_CAVE]:
            distance_to_player = calculate_distance([self.player_sprite.center_x, self.player_sprite.center_y], [tile.center_x, tile.center_y])
            if distance_to_player < 10*TILE_SCALING*self.tile_map.tile_width:
                tile.alpha = 255*(max(distance_to_player-5*TILE_SCALING*self.tile_map.tile_width, 0)) / (10*TILE_SCALING*self.tile_map.tile_width)

        # Check for collision with goal/warp portal
        if len(arcade.check_for_collision_with_list(self.player_sprite, self.scene[LAYER_NAME_GOAL])) > 0:
            self.level += 1
            self.setup()

        if self.player_sprite.center_y < 0:
            self.player_sprite.center_x = self.tile_map.tile_width * TILE_SCALING * self.spawnpoint[0]
            self.player_sprite.center_y = self.tile_map.tile_height * TILE_SCALING * self.spawnpoint[1]

            print(f"({self.player_sprite.center_x}, {self.player_sprite.center_y})")
        self.center_camera_to_player()

# Main Program

def main():
    """Main Function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    #start_view.setup()
    arcade.run()

# Things that run

if __name__ == "__main__":
    main()