import arcade


class BaseCharacter(arcade.Sprite):
    CHARACTER_SCALING = 0.5
    UPDATES_PER_FRAME = 7
    MOV_Y = 0.4
    MOV_X = 0.8
    # Constants used to track if the player is facing left or right
    RIGHT_FACING = 0
    LEFT_FACING = 1

    CHARACTER_FEMALE_ADV = "femaleAdventurer"
    CHARACTER_ZOMBIE = "zombie"
    # Images from Kenney.nl's Asset Pack 3
    assets_availables = {CHARACTER_FEMALE_ADV: ":resources:images/animated_characters/female_adventurer/femaleAdventurer",
                         "femalePerson": ":resources:images/animated_characters/female_person/femalePerson",
                         "malePerson": ":resources:images/animated_characters/male_person/malePerson",
                         "maleAdventurer": ":resources:images/animated_characters/male_adventurer/maleAdventurer",
                         CHARACTER_ZOMBIE: ":resources:images/animated_characters/zombie/zombie",
                         "robot": ":resources:images/animated_characters/robot/robot",
                        }

    def __init__(self, type_of_character):
        super().__init__()
        self.idle_texture_pair = None
        self.walk_textures = None
        self.texture = None
        # Default to face-right
        self.character_face_direction = self.RIGHT_FACING

        # Default to face-right
        self.character_face_direction = self.RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        #self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]
        self.points = [[-15, -44], [15, -44], [15, 21], [-15, 21]]
        self.scale = self.CHARACTER_SCALING
        self.load_textures(self.assets_availables[type_of_character])

    @classmethod
    def load_texture_pair(cls, filename):
        """
        Load a texture pair, with the second being a mirror image.
        """
        return [
            arcade.load_texture(filename),
            arcade.load_texture(filename, mirrored=True)
        ]

    def load_textures(self, main_path):
        # Load textures for idle standing
        self.idle_texture_pair = self.load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = self.load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)
        self.texture = self.walk_textures[0][self.character_face_direction] #just to ensure initialize texture

        self.madness_textures = []
        texture = self.load_texture_pair(f"{main_path}_jump.png")
        self.madness_textures.append(texture)
        texture = self.load_texture_pair(f"{main_path}_fall.png")
        self.madness_textures.append(texture)
        texture = self.load_texture_pair(f"{main_path}_climb0.png")
        self.madness_textures.append(texture)
        texture = self.load_texture_pair(f"{main_path}_climb1.png")
        self.madness_textures.append(texture)
