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

SPRITE_SCALING = 0.5

SCREEN_WIDTH = 1024 #800
SCREEN_HEIGHT = 768 #600
SCREEN_TITLE = "Isometric Example"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200

MOVEMENT_SPEED = 5

MOV_Y = 0.4
MOV_X = 0.8

RADIUS_VIEW = 100
RADIUS_VIEW2 = 4*RADIUS_VIEW*RADIUS_VIEW


def read_sprite_list(grid, sprite_list, default_alpha=0):
    for row in grid:
        for grid_location in row:
            if grid_location.tile is not None:
                head, tail = os.path.split(grid_location.tile.source)
                tile_sprite = arcade.Sprite("resources/images/isometric_arcade/" + tail, SPRITE_SCALING)
                tile_sprite.alpha = default_alpha
                tile_sprite.center_x = grid_location.center_x * SPRITE_SCALING
                tile_sprite.center_y = grid_location.center_y * SPRITE_SCALING
                # print(f"{grid_location.tile.source} -- ({tile_sprite.center_x:4}, {tile_sprite.center_y:4})")
                sprite_list.append(tile_sprite)

def _check_visible_elements_in_radius(px, py, sprite2, x1, x2, y1, y2):
    """
    Check for collision between two sprites.

    :param Sprite sprite1: Sprite 1
    :param Sprite sprite2: Sprite 2

    :returns: Boolean
    """

    #sloooooooooooooooooow
    x = sprite2.position[0]
    y = sprite2.position[1]
    if x < x1 or x>x2 or y<y1 or y>y2:
        return False


    diff_x = px - x
    diff_x2 = diff_x * diff_x

    if diff_x2 > RADIUS_VIEW2:
        return False

    diff_y = py - y
    diff_y2 = diff_y * diff_y
    if diff_y2 > RADIUS_VIEW2:
        return False

    distance = diff_x2 + diff_y2
    if distance > RADIUS_VIEW2:
        return False

    return True

def show_only_neighbourgh(expanded_sprite, list_all_sprites, previous_visible_sprites):
    if list_all_sprites.use_spatial_hash:
        sprite_list_to_show = list_all_sprites.spatial_hash.get_objects_for_box(expanded_sprite)
        for s in sprite_list_to_show:
                if s.alpha == 0:
                    s.alpha = 255

        for s in previous_visible_sprites:
            if s not in sprite_list_to_show:
                if s.alpha == 255:
                    s.alpha = 0

        return sprite_list_to_show



def _circular_check(player, sprite_list_to_check, x1, x2, y1, y2):
    """
    This is a horrible kludge to 'guess' our way out of a collision
    Returns:

    """

    px = player.position[0]
    py = player.position[1]
    for sprite2 in sprite_list_to_check:
        if _check_visible_elements_in_radius(px,py, sprite2, x1, x2, y1, y2):
            sprite2.alpha=255
        else:
            sprite2.alpha=0



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

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.floor_list = arcade.SpriteList(use_spatial_hash=True)
        self.objects_list = arcade.SpriteList()

        # noinspection PyDeprecation
        self.my_map = arcade.read_tiled_map('resources/tmx_maps/isometric_dungeon_test2.tmx', SPRITE_SCALING)

        # Set up the player
        #self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.4)
        self.player_sprite = PlayerCharacter()
        px, py = arcade.isometric_grid_to_screen(self.my_map.width // 2,
                                                 self.my_map.height // 2,
                                                 self.my_map.width,
                                                 self.my_map.height,
                                                 self.my_map.tilewidth,
                                                 self.my_map.tileheight)

        self.player_sprite.center_x = px * SPRITE_SCALING
        self.player_sprite.center_y = py * SPRITE_SCALING
        self.player_list.append(self.player_sprite)

        read_sprite_list(self.my_map.layers["Floor"], self.floor_list)
        read_sprite_list(self.my_map.layers["Walls"], self.wall_list, 255)
        read_sprite_list(self.my_map.layers["Furniture"], self.wall_list)

        # Set the background color
        if self.my_map.backgroundcolor is None:
            arcade.set_background_color(arcade.color.BLACK)
        else:
            arcade.set_background_color(self.my_map.backgroundcolor)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.physics_engine = PhysicsEngineIsometric(self.player_sprite, self.wall_list)

        self.last_update_alpha_x = self.player_sprite.center_x
        self.last_update_alpha_y = self.player_sprite.center_y
        self.neighbours_to_show = []
        self.expanded_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.4*10,
                                        center_x = self.player_sprite.center_x,
                                        center_y = self.player_sprite.center_y,
                                        )

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()



        # Draw all the sprites.
        self.floor_list.draw()
        self.player_list.draw()
        #_circular_check(self.player_sprite, self.wall_list).draw()
        self.wall_list.draw()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == "Q":
            exit()

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


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
            self.player_sprite.change_x = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update() #self.player_sprite.update()

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
        if abs(self.last_update_alpha_x-self.player_sprite.center_x)>25 or abs(self.last_update_alpha_y-self.player_sprite.center_y)>25:
            self.last_update_alpha_x = self.player_sprite.center_x
            self.last_update_alpha_y = self.player_sprite.center_y
            self.expanded_sprite.center_x = self.player_sprite.center_x
            self.expanded_sprite.center_y = self.player_sprite.center_y
            self.neighbours_to_show = show_only_neighbourgh(self.expanded_sprite,self.floor_list, self.neighbours_to_show)
            #_circular_check(self.player_sprite, self.floor_list,self.view_left, SCREEN_WIDTH + self.view_left, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
