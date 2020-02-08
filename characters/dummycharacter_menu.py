from characters.base_character import BaseCharacter


class DummyCharacter(BaseCharacter):
    CHARACTER_SCALING = 1.5
    def __init__(self, type_of_character):

        # Set up parent class
        super().__init__(type_of_character)

    def update_animation(self, delta_time: float = 1/60):
        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * self.UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // self.UPDATES_PER_FRAME][self.character_face_direction]
