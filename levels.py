def first_level():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append((speed, hp, (start_pos[0] + 100, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 800, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "sword", shot_delay))
    return enemies, enemy_respawn, player_pos


def second_level():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append((speed, hp, (start_pos[0] + 100, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 800, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos


def third_level():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append((speed, hp, (start_pos[0] + 100, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 300, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 800, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    enemies.append((speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos