"""
Example of displaying an isometric map.

Isometric maps aren't fully supported, and needs some additional work.

Isometric map created with Tiled Map Editor: https://www.mapeditor.org/
Tiles by Kenney: http://kenney.nl/assets/isometric-dungeon-tiles

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.isometric_example
"""

import arcade
import os
from physics_engine import PhysicsEngineIsometric
from player_character import PlayerCharacter
from enemy_character import EnemyCharacter
from dummycharacter_menu import DummyCharacter
from common import SPRITE_SCALING
from common import BASE_RESOURCES
from common import RES_MAP
from common import RES_BACKGROUND
from common import STATUS_GAMEOVER, STATUS_YOUWIN, STATUS_PLAYING, STATUS_INITIATING, STATUS_MENU
from common import RES_BACKGROUND_MUSIC



SCREEN_WIDTH = 1024 #800
SCREEN_HEIGHT = 768 #600
SCREEN_TITLE = "Pain in the back"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200

MOVEMENT_SPEED = 5

ENEMY_FASTEST_SPEED = 6
ENEMY_SLOWEST_SPEED = 2

MOV_Y = 0.4
MOV_X = 0.8

RADIUS_VIEW = 100
RADIUS_VIEW2 = 4*RADIUS_VIEW*RADIUS_VIEW


special_hit_box = []



def do_special_things():
    if special_hit_box:
        for l in special_hit_box:
            arcade.draw_polygon_outline(l, arcade.color.WHITE, 3)


def read_sprite_list(grid, sprite_list, default_alpha=0, show_details=False):
    for row in grid:
        for grid_location in row:
            if grid_location.tile is not None:
                head, tail = os.path.split(grid_location.tile.source)
                tile_sprite = arcade.Sprite(BASE_RESOURCES + tail, SPRITE_SCALING)
                tile_sprite.alpha = default_alpha
                tile_sprite.center_x = grid_location.center_x * SPRITE_SCALING
                tile_sprite.center_y = grid_location.center_y * SPRITE_SCALING
                sprite_list.append(tile_sprite)
                if tail == "stoneStep_W.png":
                    print("x:{} y:{}".format(tile_sprite.center_x,tile_sprite.center_y))


                # print(f"{grid_location.tile.source} -- ({tile_sprite.center_x:4}, {tile_sprite.center_y:4})")
                if show_details:
                    newpoints_onlytoprint = []
                    for p in tile_sprite.hit_box:
                        px, py = p

                        if py<0:
                            if py<-150:
                                ny = py + 50
                            else:
                                ny = py - 50

                            if px<0:
                                nx = px + 50
                            else:
                                nx = px - 50
                        else:
                            nx,ny = px, py
                        newpoints_onlytoprint.append([nx,ny])
                    #sprite_list.hit_box = newpoints_onlytoprint
                    tile_sprite._point_list_cache = None
                    #special_hit_box.append([(tile_sprite.center_x + p[0], tile_sprite.center_y + p[1]) for p in newpoints_onlytoprint])
                    tile_sprite.hit_box = newpoints_onlytoprint


                    #print("New points:{}".format(special_hit_box))


def play_background_music(dummy=None):
    print("Play music...")
    background_music = arcade.load_sound(RES_BACKGROUND_MUSIC)
    arcade.play_sound(background_music)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

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
        self.current_status = STATUS_MENU
        self.objects_list = None
        self.furniture_list = None
        self.holes_list = None
        self.enemies_list = None
        self.endzone_list = None
        self.dummycharacter_list = None
        self.background_music = False

    def grid_to_points(self,grid_x, grid_y):
        px, py = arcade.isometric_grid_to_screen(grid_x, grid_y,
                                                 self.my_map.width,
                                                 self.my_map.height,
                                                 self.my_map.tilewidth,
                                                 self.my_map.tileheight)

        return px,py



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
        self.dummycharacter_list = arcade.SpriteList()
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

        #Dummy characters for the MENU

        dummycharacter = DummyCharacter("female")
        dummycharacter.center_x = 2*VIEWPORT_MARGIN + 110
        dummycharacter.center_y = 2*VIEWPORT_MARGIN - 100
        self.dummycharacter_list.append(dummycharacter)

        dummycharacter = DummyCharacter("zombie")
        self.dummycharacter_list.append(dummycharacter)
        dummycharacter.center_x = VIEWPORT_MARGIN + 35
        dummycharacter.center_y = 2*VIEWPORT_MARGIN - 100


        enemy_points=[(3156,1846,"LEFT", ENEMY_FASTEST_SPEED),
                      (2808,1384, "DOWN", ENEMY_SLOWEST_SPEED),
                      (1036,1250, "RIGHT",ENEMY_FASTEST_SPEED),
                      (2508, 2502, "LEFT",ENEMY_SLOWEST_SPEED),
                      (3132, 2994, "DOWN",ENEMY_FASTEST_SPEED),
                      (3148, 2586, "DOWN",ENEMY_SLOWEST_SPEED),
                      (3592, 336, "RIGHT",ENEMY_FASTEST_SPEED),
                      (4164, 1254, "DOWN",ENEMY_FASTEST_SPEED),
                      (6004, 1610, "LEFT",ENEMY_SLOWEST_SPEED),
                      (416, 1592, "DOWN",ENEMY_SLOWEST_SPEED)]
        print(self.my_map.width, self.my_map.height)
        for ep in enemy_points:
            enemy_sprite = EnemyCharacter()
            #enemy_sprite.center_x,enemy_sprite.center_y = self.grid_to_points(ep[0], ep[1])
            enemy_sprite.center_x = ep[0]
            enemy_sprite.center_y = ep[1]
            direction = ep[2]
            mov_speed = ep[3]
            print(mov_speed)

            print(enemy_sprite.center_x, enemy_sprite.center_y)
            if direction == "UP":
                enemy_sprite.change_y = mov_speed*MOV_Y
                enemy_sprite.change_x = -mov_speed*MOV_X
            elif  direction == "DOWN":
                enemy_sprite.change_y = -mov_speed*MOV_Y
                enemy_sprite.change_x = mov_speed*MOV_X
            elif direction == "LEFT":
                enemy_sprite.change_x = -mov_speed*MOV_X
                enemy_sprite.change_y = -mov_speed*MOV_Y
            elif direction == "RIGHT":
                enemy_sprite.change_x = mov_speed*MOV_X
                enemy_sprite.change_y = mov_speed*MOV_Y
            self.enemies_list.append(enemy_sprite)


        read_sprite_list(self.my_map.layers["Floor"], self.floor_list,255)
        read_sprite_list(self.my_map.layers["Walls"], self.wall_list, 255)
        read_sprite_list(self.my_map.layers["Furniture"], self.furniture_list, 255)
        read_sprite_list(self.my_map.layers["Holes"], self.holes_list, 255, show_details=True)
        read_sprite_list(self.my_map.layers["END"], self.endzone_list,255)

        # Set the background color
        if self.my_map.backgroundcolor is None:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            arcade.set_background_color(self.my_map.backgroundcolor)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.physics_engine = PhysicsEngineIsometric(self.player_sprite, self.wall_list, self.holes_list, self.floor_list, self.enemies_list, self.endzone_list, self.dummycharacter_list)

        self.last_update_alpha_x = self.player_sprite.center_x
        self.last_update_alpha_y = self.player_sprite.center_y
        self.neighbours_to_show = []


        if not self.background_music:
            self.background_music = True
            play_background_music()
            arcade.schedule(play_background_music, 95 )#95)


    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.BLACK, 54, bold=True)

        output = "Press Enter to restart"
        arcade.draw_text(output, 310, 300, arcade.color.BLACK, 24, bold=True)



    def draw_game(self):

        # Draw all the sprites.
        self.holes_list.draw()
        self.floor_list.draw()


        self.player_list.draw()
        self.enemies_list.draw()
        self.wall_list.draw()
        self.furniture_list.draw()


    def draw_phrase(self, title, subtitle):
        posx = self.view_left + VIEWPORT_MARGIN
        posy = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        arcade.draw_text(title, posx, posy, arcade.color.WHITE, 54)
        arcade.draw_text(subtitle, posx + 70, posy - 100, arcade.color.WHITE, 24)


    def draw_youwin(self):
        self.draw_phrase("YOU WIN", "PRESS SPACE TO RESTART")

    def draw_gameover(self):
        self.draw_phrase("GAME OVER", "PRESS SPACE TO RESTART")

    def draw_initiating(self):
        try:
            self.background.draw(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,SCREEN_WIDTH, SCREEN_HEIGHT)
            #arcade.draw_lrwh_rectangle_textured(0,0,
            #                                    SCREEN_WIDTH, SCREEN_HEIGHT,
            #                                    self.background)
        except Exception as ex:
            print(ex)
        self.draw_phrase("INITIATING...", "...")

    def draw_menu(self):
        try:
            self.background.draw(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,SCREEN_WIDTH, SCREEN_HEIGHT)
        except Exception as ex:
            print(ex)
        self.draw_phrase("INDIE-ANA JONES", "Press SPACE to START")
        self.dummycharacter_list.draw()

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        if self.current_status == STATUS_PLAYING:
            self.draw_game()
        elif self.current_status == STATUS_YOUWIN:
            self.draw_youwin()
        elif self.current_status == STATUS_GAMEOVER:
            self.draw_gameover()
        elif self.current_status == STATUS_INITIATING:
            self.draw_initiating()
        elif self.current_status == STATUS_MENU:
            self.draw_menu()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.current_status==STATUS_PLAYING:
            if key == arcade.key.Q:
                exit()

            if key == arcade.key.SPACE:
                self.player_sprite.repairing = True
            if key == arcade.key.A:
                print("X:{} Y:{}".format(self.player_sprite.center_x, self.player_sprite.center_y))
            if key == arcade.key.W:
                self.current_status = STATUS_YOUWIN
            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED*MOV_Y
                self.player_sprite.change_x = -MOVEMENT_SPEED*MOV_X
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED*MOV_Y
                self.player_sprite.change_x = MOVEMENT_SPEED*MOV_X
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED*MOV_X
                self.player_sprite.change_y = -MOVEMENT_SPEED*MOV_Y
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED*MOV_X
                self.player_sprite.change_y = MOVEMENT_SPEED*MOV_Y
        elif self.current_status == STATUS_MENU:
            print("Inside STATUS MENU. key{}".format(key))
            if key == arcade.key.SPACE:
                self.current_status = STATUS_PLAYING
        elif self.current_status in (STATUS_YOUWIN, STATUS_GAMEOVER):
            #Reiniciar
            if key == arcade.key.SPACE:
                self.current_status = STATUS_INITIATING
                self.setup()
                self.current_status = STATUS_MENU

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if self.current_status == STATUS_PLAYING:
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

        self.physics_engine.update(self) #self.player_sprite.update()

        if self.current_status != STATUS_PLAYING:
            return
        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
            #print("x1{} x2{} y1{} y2{}".format(self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom))

        #Update Alpha of visible elements
        #if abs(self.last_update_alpha_x-self.player_sprite.center_x)>25 or abs(self.last_update_alpha_y-self.player_sprite.center_y)>25:
        #    self.last_update_alpha_x = self.player_sprite.center_x
        #    self.last_update_alpha_y = self.player_sprite.center_y
        #    self.expanded_sprite.center_x = self.player_sprite.center_x
        #    self.expanded_sprite.center_y = self.player_sprite.center_y
        #    self.neighbours_to_show = show_only_neighbourgh(self.expanded_sprite,self.floor_list, self.neighbours_to_show)
        #    #_circular_check(self.player_sprite, self.floor_list,self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
