"""
Physics engines for isometric dungeon.
"""
# pylint: disable=too-many-arguments, too-many-locals, too-few-public-methods

from arcade import check_for_collision_with_list
from arcade import check_for_collision
from arcade import Sprite
from arcade import SpriteList

class PhysicsEngineIsometric:
    """
    Simplistic physics engine for use in games without gravity, such as top-down
    games. It is easier to get
    started with this engine than more sophisticated engines like PyMunk. Note, it
    does not currently handle rotation.
    """

    def __init__(self, player_sprite: Sprite, walls: SpriteList):
        """
        Create a simple physics engine.

        :param Sprite player_sprite: The moving sprite
        :param SpriteList walls: The sprites it can't move through
        """
        assert(isinstance(player_sprite, Sprite))
        assert(isinstance(walls, SpriteList))
        self.player_sprite = player_sprite
        self.walls = walls

    def update(self):
            """
            Move everything and resolve collisions.

            :Returns: SpriteList with all sprites contacted. Empty list if no sprites.
            """

            # Save previous position

            prev_x = self.player_sprite.center_x
            prev_y = self.player_sprite.center_y
            # --- Move in the x direction
            self.player_sprite.center_x += self.player_sprite.change_x
            self.player_sprite.center_y += self.player_sprite.change_y

            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player_sprite,
                                              self.walls)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                self.player_sprite.center_x = prev_x
                self.player_sprite.center_y = prev_y
                #for sp in hit_list:
                #    print(sp.texture)

            self.player_sprite.update_animation()
            # Return list of encountered sprites
            return hit_list
