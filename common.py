SPRITE_SCALING = 0.5

BASE_RESOURCES = "resources/images/isometric_arcade/"
REPAIRED_STONE = "stoneUneven_{}.png"
ORIENTATIONS = ["N","S","E","W"]
MAX_INDEX_ORIENTATIONS = len(ORIENTATIONS)-1
RES_RAPAIRED_STONE = BASE_RESOURCES + REPAIRED_STONE
xxRES_MAP = 'resources/tmx_maps/isometric_dungeon_quick.tmx'
RES_MAP = 'resources/tmx_maps/dungeon_final.tmx'

RES_BACKGROUND = BASE_RESOURCES + "abstract_1.jpg"

STATUS_YOUWIN = 1
STATUS_GAMEOVER = 2
STATUS_PLAYING = 3

RES_MUSIC = "resources/sounds/"
RES_BACKGROUND_MUSIC = RES_MUSIC + "FallidoIndianaJam.wav"


SCREEN_WIDTH = 1024 # 800
SCREEN_HEIGHT = 768 # 600
SCREEN_TITLE = "MinoriadeUnoSolo: Indie-Ana Jones"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 200

ENEMY_FASTEST_SPEED = 6
ENEMY_SLOWEST_SPEED = 2

MOV_Y = 0.4
MOV_X = 0.8

VIEWMODE_MENU = "menu"
VIEWMODE_GAME = "game"
VIEWMODE_YOUWIN = "youwin"
VIEWMODE_GAMEOVER = "gameover"