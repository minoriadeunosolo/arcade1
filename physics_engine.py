"""
Physics engines for isometric dungeon.
"""
# pylint: disable=too-many-arguments, too-many-locals, too-few-public-methods
from functools import partial

from arcade import check_for_collision_with_list
from arcade import check_for_collision
from arcade import Sprite
from arcade import SpriteList
from arcade import play_sound, load_sound
from pyglet.clock import schedule_once

from util import repair_nearby_tiles
from common import (STATUS_YOUWIN, STATUS_GAMEOVER, STATUS_PLAYING, RES_REPAIRING_SOUND_LIST, RES_REPAIRING_SOUND_1,
                    RES_REPAIRING_SOUND_4, RES_REPAIRING_SOUND_5)


def play_physics_sound(*args):
    if args:
        play_sound(args[0])


class PhysicsEngineIsometric:
    """
    Simplistic physics engine for use in games without gravity, such as top-down
    games. It is easier to get
    started with this engine than more sophisticated engines like PyMunk. Note, it
    does not currently handle rotation.
    """

    def __init__(self, player_sprite: Sprite, walls: SpriteList, holes: SpriteList, floor: SpriteList, enemies: SpriteList, endzone: SpriteList):
        """
        Create a simple physics engine.

        :param Sprite player_sprite: The moving sprite
        :param SpriteList walls: The sprites it can't move through
        """
        assert(isinstance(player_sprite, Sprite))
        assert(isinstance(walls, SpriteList))
        self.player_sprite = player_sprite
        self.walls = walls
        self.holes = holes
        self.floor = floor
        self.enemies = enemies
        self.endzone = endzone
        
        self.expanded_sprite = Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.4*5,
                                                center_x = self.player_sprite.center_x,
                                                center_y = self.player_sprite.center_y,
                                                )
        self.sounds_repairing = [load_sound(res) for res in RES_REPAIRING_SOUND_LIST]

    def update(self, mygame):
            """
            Move everything and resolve collisions.

            :Returns: (STATUS, SpriteList) SpriteList with all sprites contacted. Empty list if no sprites.
            """

            # Save previous position

            prev_x = self.player_sprite.center_x
            prev_y = self.player_sprite.center_y
            # --- Move in the x direction
            self.player_sprite.center_x += self.player_sprite.change_x
            self.player_sprite.center_y += self.player_sprite.change_y

            endhit_list = check_for_collision_with_list(self.player_sprite, self.endzone)
            if endhit_list:
                print('HIT END')
                mygame.current_status = STATUS_YOUWIN
                return STATUS_YOUWIN, endhit_list

            enemyhit_list = check_for_collision_with_list(self.player_sprite, self.enemies)
            if enemyhit_list:
                print('HIT ENEMY')
                mygame.current_status = STATUS_GAMEOVER
                return STATUS_GAMEOVER, enemyhit_list

            # Check for wall hit
            hit_list = check_for_collision_with_list(self.player_sprite, self.walls)

            if not hit_list:
                hit_list = check_for_collision_with_list(self.player_sprite, self.holes)

                if hit_list:
                    if self.player_sprite.repairing:
                        ds = None
                        DELAY_TIME = 0.1
                        for m in self.sounds_repairing:
                            if not ds:
                                play_physics_sound(m)
                                ds = DELAY_TIME
                            else:
                                schedule_once(partial(play_physics_sound, m), ds)
                                ds += DELAY_TIME

                        self.player_sprite.repairing = False
                        self.expanded_sprite.center_x = self.player_sprite.center_x
                        self.expanded_sprite.center_y = self.player_sprite.center_y
                        repair_nearby_tiles(self.expanded_sprite, self.floor, self.holes)
                else:
                    self.player_sprite.repairing = False

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                self.player_sprite.center_x = prev_x
                self.player_sprite.center_y = prev_y

            self.player_sprite.update_animation()
            for enemy in self.enemies:
                e_x = enemy.center_x
                e_y = enemy.center_y
                enemy.center_x += enemy.change_x
                enemy.center_y += enemy.change_y
                hit_list = check_for_collision_with_list(enemy, self.walls)
                if hit_list:
                    enemy.center_x = e_x
                    enemy.center_y = e_y
                    enemy.change_x *= -1
                    enemy.change_y *= -1

                enemy.update_animation()


            # Return list of encountered sprites
            return STATUS_PLAYING, hit_list
