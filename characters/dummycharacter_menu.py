import random
from characters.base_character import BaseCharacter


class DummyCharacter(BaseCharacter):
    CHARACTER_SCALING = 1.5

    def __init__(self, type_of_character, min_pos_x=0, max_pos_x=0, change_x=0):
        # Set up parent class
        super().__init__(type_of_character)

        self.min_pos_x = min_pos_x
        self.max_pos_x = max_pos_x
        self.change_x = change_x
        self.current_direction = "RIGHT"
        self.mov_salt = random.randint(0, 2)

    def update_animation(self, delta_time: float = 1/60):
        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * self.UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // self.UPDATES_PER_FRAME][self.character_face_direction]

    def update_position(self):

        if self.current_direction == "LEFT":
            if self.center_x < self.min_pos_x:
                self.current_direction = "RIGHT"
                self.mov_salt = random.randint(0, 2)
                self.center_x += self.change_x + self.mov_salt
            else:
                self.center_x -= self.change_x + self.mov_salt
            return

        if self.current_direction == "RIGHT":
            if self.center_x > self.max_pos_x:
                self.current_direction = "LEFT"
                self.mov_salt = random.randint(0, 2)
                self.center_x -= self.change_x + self.mov_salt
            else:
                self.center_x += self.change_x + self.mov_salt
