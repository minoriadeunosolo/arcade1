import arcade

from view_modes.base_view import BaseView
from characters.dummycharacter_menu import DummyCharacter

from common import RES_BACKGROUND
from common import VIEWPORT_MARGIN
from common import SCREEN_WIDTH
from common import SCREEN_HEIGHT
from common import VIEWMODE_GAME


class MenuView(BaseView):
    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture(RES_BACKGROUND)

        # Dummy characters for the MENU
        self.menucharacters = arcade.SpriteList()

        base_x_ana = 2 * VIEWPORT_MARGIN + 110
        self.indie_ana = DummyCharacter(DummyCharacter.CHARACTER_FEMALE_ADV, base_x_ana, base_x_ana + 150, 3)

        self.indie_ana.center_x = base_x_ana
        self.indie_ana.center_y = 2*VIEWPORT_MARGIN - 100
        self.menucharacters.append(self.indie_ana)

        base_x_zombi = VIEWPORT_MARGIN + 35
        self.zombie = DummyCharacter(DummyCharacter.CHARACTER_ZOMBIE, base_x_zombi, base_x_zombi + 150, 3)

        self.zombie.center_x = base_x_zombi
        self.zombie.center_y = 2*VIEWPORT_MARGIN - 100
        self.menucharacters.append(self.zombie)

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        #try:
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        #self.background.draw(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.draw_phrase("INDIE-ANA JONES", "Press SPACE to START")
        self.menucharacters.draw()
        #except Exception as ex:
        #    print("{id} : {ex} ".format(id=self.myid, ex=ex))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            exit()

        if key == arcade.key.SPACE:
            self.changeviewmode(VIEWMODE_GAME)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.indie_ana.update_position()
        self.zombie.update_position()

        self.menucharacters.update_animation()

