import random
import datetime

from characters.base_character import BaseCharacter


class EnemyCharacter(BaseCharacter):
    CHARACTER_SCALING = 0.5
    ENEMY_FASTEST_SPEED = 6
    ENEMY_SLOWEST_SPEED = 2
    INITIAL_DIRECTION_UP = 0
    INITIAL_DIRECTION_RIGHT = 1
    INITIAL_DIRECTION_DOWN = 2
    INITIAL_DIRECTION_LEFT = 3

    coef_directions = [(-1.0, 1.0), (1.0, 1.0), (1.0, -1.0), (-1.0, - 1.0)]

    def __init__(self, mov_speed,  initial_direction):
        # Set up parent class
        if mov_speed == self.ENEMY_SLOWEST_SPEED:
            super().__init__("zombie")
        else:
            super().__init__("robot")

        self.direction = initial_direction
        self.mov_speed = mov_speed
        c = self.coef_directions[initial_direction]
        self.change_x = c[0] * mov_speed * self.MOV_X
        self.change_y = c[1] * mov_speed * self.MOV_Y

        self.madness = False
        self.madness_prob = 0.5
        self.current_base_textures = self.walk_textures
        self.last_madness_time = datetime.datetime.now()

    def try_madness(self):
        now = datetime.datetime.now()
        time_from_madness = (now - self.last_madness_time).seconds
        if self.madness:
            if time_from_madness > 1.5:
                self.madness = False
                self.last_madness_time = now
                self.current_base_textures = self.walk_textures
                self.cur_texture = -1
                self.direction = (self.direction + 1) % len(self.coef_directions)
                c = self.coef_directions[self.direction]
                self.change_x = c[0] * self.mov_speed * self.MOV_X
                self.change_y = c[1] * self.mov_speed * self.MOV_Y
        else:
            if time_from_madness > 5:
                if random.uniform(0, 1) < self.madness_prob:
                    self.madness = True
                    self.current_base_textures = self.madness_textures
                    self.cur_texture = -1
                    self.change_x = 0.0
                    self.change_y = 0.0
                self.last_madness_time = now


    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == self.RIGHT_FACING:
            self.character_face_direction = self.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == self.LEFT_FACING:
            self.character_face_direction = self.RIGHT_FACING

        self.cur_texture = (self.cur_texture + 1) % ((len(self.current_base_textures)-1) * self.UPDATES_PER_FRAME)
        self.texture = self.current_base_textures[self.cur_texture // self.UPDATES_PER_FRAME][self.character_face_direction]


