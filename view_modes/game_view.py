import arcade
from view_modes.base_view import BaseView
from physics_engine import PhysicsEngineIsometric
from characters.player_character import PlayerCharacter
from characters.enemy_character import EnemyCharacter
from common import SPRITE_SCALING
from common import RES_MAP
from common import RES_BACKGROUND
from common import STATUS_GAMEOVER, STATUS_YOUWIN
from common import RES_BACKGROUND_MUSIC

from common import VIEWMODE_YOUWIN, VIEWMODE_GAMEOVER


background_music = None
def play_background_music(dummy=None):
    print("Play music...")
    global background_music
    if not background_music:
        background_music = arcade.load_sound(RES_BACKGROUND_MUSIC)
    background_music.player.loop = True
    arcade.play_sound(background_music)

def stop_background_music():
    global background_music
    if background_music:
        arcade.unschedule(play_background_music)
        background_music.player.seek(100000)


class GameView(BaseView):
    """ Main Game Mode class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.

        # Sprite lists
        self.all_sprites_list = None

        # Set up the player
        self.player_sprite = None
        self.wall_list = None
        self.floor_list = None
        self.objects_list = None
        self.player_list = None
        self.view_bottom = 0
        self.view_left = 0
        self.my_map = None
        self.setup_launched  = False

        self.objects_list = None
        self.furniture_list = None
        self.holes_list = None
        self.enemies_list = None
        self.endzone_list = None

        self.background_music = False

        self.setup()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.background = arcade.load_texture(RES_BACKGROUND)
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)
        self.objects_list = arcade.SpriteList()
        self.furniture_list = arcade.SpriteList()
        self.holes_list = arcade.SpriteList(use_spatial_hash=True)
        self.enemies_list = arcade.SpriteList()
        self.endzone_list =arcade.SpriteList(use_spatial_hash=True)
        init_positions_enemies_list = arcade.SpriteList()

        # noinspection PyDeprecation
        self.my_map = arcade.read_tiled_map(RES_MAP, SPRITE_SCALING)
        #self.my_map = arcade.read_tiled_map('resources/tmx_maps/isometric_dungeon_quick.tmx', SPRITE_SCALING)

        # Set up the player
        #self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.4)

        px, py = self.grid_to_points(self.my_map.width // 2, self.my_map.height // 2)

        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = px * SPRITE_SCALING
        self.player_sprite.center_y = py * SPRITE_SCALING
        self.player_list.append(self.player_sprite)

        enemies_DS=[(EnemyCharacter.INITIAL_DIRECTION_LEFT, EnemyCharacter.ENEMY_FASTEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_DOWN, EnemyCharacter.ENEMY_SLOWEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_RIGHT, EnemyCharacter.ENEMY_FASTEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_LEFT, EnemyCharacter.ENEMY_SLOWEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_DOWN, EnemyCharacter.ENEMY_FASTEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_DOWN, EnemyCharacter.ENEMY_SLOWEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_RIGHT, EnemyCharacter.ENEMY_FASTEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_DOWN, EnemyCharacter.ENEMY_FASTEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_LEFT, EnemyCharacter.ENEMY_SLOWEST_SPEED),
                      (EnemyCharacter.INITIAL_DIRECTION_DOWN, EnemyCharacter.ENEMY_SLOWEST_SPEED)]

        self.read_sprite_list(self.my_map.layers["Floor"], self.floor_list, 255)
        self.read_sprite_list(self.my_map.layers["Walls"], self.wall_list, 255)
        self.read_sprite_list(self.my_map.layers["Furniture"], self.furniture_list, 255)
        self.read_sprite_list(self.my_map.layers["Holes"], self.holes_list, 255)
        self.read_sprite_list(self.my_map.layers["END"], self.endzone_list, 255)
        self.read_sprite_list(self.my_map.layers["INIT_ENEMIES"], init_positions_enemies_list, 255)

        for ix in range(0, min(len(init_positions_enemies_list), len(enemies_DS))):
            direction, speed = enemies_DS[ix][0], enemies_DS[ix][1]
            center_x, center_y = init_positions_enemies_list[ix].center_x, init_positions_enemies_list[ix].center_y
            enemy_sprite = EnemyCharacter(initial_direction=direction, mov_speed=speed)
            enemy_sprite.center_x = center_x
            enemy_sprite.center_y = center_y
            self.enemies_list.append(enemy_sprite)

        # Set the background color
        if self.my_map.backgroundcolor is None:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            arcade.set_background_color(self.my_map.backgroundcolor)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.physics_engine = PhysicsEngineIsometric(self.player_sprite, self.wall_list, self.holes_list,
                                                     self.floor_list, self.enemies_list, self.endzone_list)

        self.last_update_alpha_x = self.player_sprite.center_x
        self.last_update_alpha_y = self.player_sprite.center_y
        self.neighbours_to_show = []

        if not self.background_music:
            self.background_music = True
            play_background_music()
            arcade.schedule(play_background_music, 95)#95)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        # Draw all the sprites.
        self.holes_list.draw()
        self.floor_list.draw()

        self.player_list.draw()
        self.enemies_list.draw()
        self.wall_list.draw()
        self.furniture_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.Q:
            exit()
        if key == arcade.key.W:
            self.changeviewmode(VIEWMODE_YOUWIN)

        if key == arcade.key.SPACE:
            self.player_sprite.repairing = True
        if key == arcade.key.A:
            print("X:{} Y:{}".format(self.player_sprite.center_x, self.player_sprite.center_y))

        if key == arcade.key.UP:
            self.player_sprite.change_y = PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_Y
            self.player_sprite.change_x = -PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_X
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_Y
            self.player_sprite.change_x = PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_X
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_X
            self.player_sprite.change_y = -PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_Y
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_X
            self.player_sprite.change_y = PlayerCharacter.MOVEMENT_SPEED*PlayerCharacter.MOV_Y

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        elif key == arcade.key.SPACE:
            self.player_sprite.repairing = True

    def on_update(self, delta_time):
        """ Movement and game logic """

        status, hit_list = self.physics_engine.update(self)

        # --- Manage Scrolling ---
        # Track if we need to change the viewport
        self.update_viewport(self.player_sprite)

        if status == STATUS_GAMEOVER:
            stop_background_music()
            self.changeviewmode(VIEWMODE_GAMEOVER)
            return
        elif status == STATUS_YOUWIN:
            stop_background_music()
            self.changeviewmode(VIEWMODE_YOUWIN)
            return

        for enemy in self.enemies_list:
            enemy.try_madness()