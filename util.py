""" Utility functions

"""
from arcade import Sprite
from common import SPRITE_SCALING
from common import RES_RAPAIRED_STONE
from common import MAX_INDEX_ORIENTATIONS
from common import ORIENTATIONS

def _check_visible_elements_in_radius(px, py, sprite2, x1, x2, y1, y2):
    """
    Check for collision between two sprites.

    :param Sprite sprite1: Sprite 1
    :param Sprite sprite2: Sprite 2

    :returns: Boolean
    """

    #sloooooooooooooooooow
    x = sprite2.position[0]
    y = sprite2.position[1]
    if x < x1 or x>x2 or y<y1 or y>y2:
        return False


    diff_x = px - x
    diff_x2 = diff_x * diff_x

    if diff_x2 > RADIUS_VIEW2:
        return False

    diff_y = py - y
    diff_y2 = diff_y * diff_y
    if diff_y2 > RADIUS_VIEW2:
        return False

    distance = diff_x2 + diff_y2
    if distance > RADIUS_VIEW2:
        return False

    return True

def show_only_neighbourgh(expanded_sprite, list_all_sprites, previous_visible_sprites):
    if list_all_sprites.use_spatial_hash:
        sprite_list_to_show = list_all_sprites.spatial_hash.get_objects_for_box(expanded_sprite)
        for s in sprite_list_to_show:
                if s.alpha == 0:
                    s.alpha = 255

        for s in previous_visible_sprites:
            if s not in sprite_list_to_show:
                if s.alpha == 255:
                    s.alpha = 0

        return sprite_list_to_show

def repair_nearby_tiles(expanded_sprite, floor_sprites, holes_sprites):
    if holes_sprites.use_spatial_hash:
        nearby_sprites = holes_sprites.spatial_hash.get_objects_for_box(expanded_sprite)
        for ix,s in enumerate(nearby_sprites):
                if s in holes_sprites:
                    holes_sprites.remove(s)
                tile_sprite = Sprite(RES_RAPAIRED_STONE.format(ORIENTATIONS[ix % MAX_INDEX_ORIENTATIONS]), SPRITE_SCALING)
                tile_sprite.center_x = s.center_x
                tile_sprite.center_y = s.center_y
                floor_sprites.append(tile_sprite)

        holes_sprites._recalculate_spatial_hashes()



def _circular_check(player, sprite_list_to_check, x1, x2, y1, y2):
    """
    This is a horrible kludge to 'guess' our way out of a collision
    Returns:

    """

    px = player.position[0]
    py = player.position[1]
    for sprite2 in sprite_list_to_check:
        if _check_visible_elements_in_radius(px,py, sprite2, x1, x2, y1, y2):
            sprite2.alpha=255
        else:
            sprite2.alpha=0
