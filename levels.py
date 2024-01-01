def level_1():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("swordsman", speed, hp, (player_pos[0], player_pos[1] + 400), enemy_shape, "sword", shot_delay))
    return enemies, enemy_respawn, player_pos


def level_2():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("swordsman", speed, hp, (start_pos[0] + 100, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("swordsman", speed, hp, (start_pos[0] + 800, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("swordsman", speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "sword", shot_delay))
    return enemies, enemy_respawn, player_pos

def level_3():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("swordsman", speed, hp, (start_pos[0] + 100, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("swordsman", speed, hp, (start_pos[0] + 800, start_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("archer", speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos


def level_4():
    speed = 100
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("archer",speed, hp, (start_pos[0] + 100, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    enemies.append(("archer",speed, hp, (start_pos[0] + 300, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    enemies.append(("archer",speed, hp, (start_pos[0] + 800, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    enemies.append(("archer",speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos

def level_5():
    speed = 400
    hp = 100
    start_pos = (800, 500)
    player_pos = (1200, 450)
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("green_swordsman", speed, hp, (start_pos[0] + 100, start_pos[1]), enemy_shape, "hands", shot_delay))
    enemies.append(("green_swordsman", speed, hp, (start_pos[0] + 800, start_pos[1]), enemy_shape, "hands", shot_delay))
    enemies.append(("green_swordsman", speed, hp, (start_pos[0] + 500, start_pos[1] + 300), enemy_shape, "hands", shot_delay))
    return enemies, enemy_respawn, player_pos