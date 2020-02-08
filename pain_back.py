"""

"""

import arcade
import os
from view_modes.base_view import BaseView
from view_modes.game_view import GameView
from view_modes.menu_view import MenuView
from view_modes.gameover_view import GameOverView
from view_modes.youwin_view import YouWinView
from common import VIEWMODE_YOUWIN, VIEWMODE_GAMEOVER, VIEWMODE_GAME, VIEWMODE_MENU
from common import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    """ Main method """
    file_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(file_path)

    BaseView.register(VIEWMODE_MENU, MenuView)
    BaseView.register(VIEWMODE_GAME, GameView)
    BaseView.register(VIEWMODE_YOUWIN, YouWinView)
    BaseView.register(VIEWMODE_GAMEOVER, GameOverView)

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = BaseView.viewmngr.createview(VIEWMODE_MENU)
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()
