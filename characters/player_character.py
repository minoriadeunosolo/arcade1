from characters.base_character import BaseCharacter


class PlayerCharacter(BaseCharacter):
    CHARACTER_SCALING = 0.5
    MOVEMENT_SPEED = 5

    def __init__(self):
        # Set up parent class
        super().__init__("femaleAdventurer")
        self.repairing = False

    def update_animation(self, delta_time: float = 1/60):
        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == self.RIGHT_FACING:
            self.character_face_direction = self.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == self.LEFT_FACING:
            self.character_face_direction = self.RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * self.UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // self.UPDATES_PER_FRAME][self.character_face_direction]
