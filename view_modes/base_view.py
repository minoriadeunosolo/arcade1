import os
import arcade
from uuid import uuid4
from common import VIEWPORT_MARGIN
from common import SCREEN_WIDTH
from common import SCREEN_HEIGHT
from common import SPRITE_SCALING
from common import BASE_RESOURCES
from view_modes.view_manager import ViewManager

class BaseView(arcade.View):
    viewmngr = ViewManager()

    def __init__(self):
        super().__init__()
        self.view_bottom = 0
        self.view_left = 0
        self.myid = uuid4()
        self.reset_viewport()

    @classmethod
    def register(cls, viewname, viewmodeclass):
        cls.viewmngr.register(viewname, viewmodeclass)

    def changeviewmode(self, viewname):
        menu = BaseView.viewmngr.createview(viewname)
        self.window.show_view(menu)

    def draw_phrase(self, title, subtitle):
        posx = self.view_left + VIEWPORT_MARGIN
        posy = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        arcade.draw_text(title, posx, posy, arcade.color.WHITE, 54)
        arcade.draw_text(subtitle, posx + 70, posy - 100, arcade.color.WHITE, 24)

    def read_sprite_list(self, grid, sprite_list, default_alpha=0, show_details=False):
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

    def grid_to_points(self,grid_x, grid_y):
        px, py = arcade.isometric_grid_to_screen(grid_x, grid_y,
                                                 self.my_map.width,
                                                 self.my_map.height,
                                                 self.my_map.tilewidth,
                                                 self.my_map.tileheight)

        return px, py

    def update_viewport(self, reference_sprite):
        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if reference_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if reference_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if reference_sprite.top > top_bndry:
            self.view_bottom += reference_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if reference_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - reference_sprite.bottom
            changed = True

        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

    def reset_viewport(self):
        arcade.set_viewport(self.view_left,
                            SCREEN_WIDTH + self.view_left,
                            self.view_bottom,
                            SCREEN_HEIGHT + self.view_bottom)