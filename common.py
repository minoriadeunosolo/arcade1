SPRITE_SCALING = 0.5

BASE_RESOURCES = "resources/images/isometric_arcade/"
REPAIRED_STONE = "stoneUneven_{}.png"
ORIENTATIONS = ["N","S","E","W"]
MAX_INDEX_ORIENTATIONS = len(ORIENTATIONS)-1
RES_RAPAIRED_STONE = BASE_RESOURCES + REPAIRED_STONE
xxx_RES_MAP = 'resources/tmx_maps/dungeon_little.tmx'
RES_MAP = 'resources/tmx_maps/dungeon_final.tmx'

RES_BACKGROUND = BASE_RESOURCES + "abstract_1.jpg"

STATUS_YOUWIN = 1
STATUS_GAMEOVER = 2
STATUS_PLAYING = 3

RES_SOUNDS = "resources/sounds/"
RES_BACKGROUND_MUSIC = RES_SOUNDS + "FallidoIndianaJam.wav"

RES_REPAIRING_SOUND_1 = RES_SOUNDS + "hit1.wav"
RES_REPAIRING_SOUND_4 = RES_SOUNDS + "hit4.wav"
RES_REPAIRING_SOUND_5 = RES_SOUNDS + "hit5.wav"
RES_REPAIRING_SOUND_LIST = [RES_REPAIRING_SOUND_1, RES_REPAIRING_SOUND_4, RES_REPAIRING_SOUND_5]


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