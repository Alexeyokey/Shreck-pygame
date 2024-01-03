player_pos = (600, 400)


def level_1():
    speed = 100
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("swordsman", speed, hp, (player_pos[0], player_pos[1] + 200), enemy_shape, "sword", shot_delay))
    return enemies, enemy_respawn, player_pos


def level_2():
    speed = 100
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("swordsman", speed, hp, (player_pos[0] - 150, player_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("swordsman", speed, hp, (player_pos[0] + 150, player_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("swordsman", speed, hp, (player_pos[0], player_pos[1] + 150), enemy_shape, "sword", shot_delay))
    return enemies, enemy_respawn, player_pos


def level_3():
    speed = 100
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("swordsman", speed, hp, (player_pos[0] + 250, player_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("swordsman", speed, hp, (player_pos[0] - 250, player_pos[1]), enemy_shape, "sword", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0], player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos


def level_4():
    speed = 100
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("archer", speed, hp, (player_pos[0] - 200, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] - 200, player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] + 200, player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] + 200, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos


def level_5():
    speed = 400
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("green_swordsman", speed, hp, (player_pos[0] - 300, player_pos[1]), enemy_shape, "hands", shot_delay))
    enemies.append(("green_swordsman", speed, hp, (player_pos[0] + 300, player_pos[1]), enemy_shape, "hands", shot_delay))
    return enemies, enemy_respawn, player_pos

def level_6():
    speed_arch = 200
    green_swordsman_speed = 400
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("green_swordsman", green_swordsman_speed, hp, (player_pos[0] - 300, player_pos[1]), enemy_shape, "hands", shot_delay))
    enemies.append(("green_swordsman", green_swordsman_speed, hp, (player_pos[0] + 300, player_pos[1]), enemy_shape, "hands", shot_delay))
    enemies.append(("green_swordsman", green_swordsman_speed, hp, (player_pos[0], player_pos[1] + 250), enemy_shape, "hands", shot_delay))
    enemies.append(("archer", speed_arch, hp, (player_pos[0] - 150, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed_arch, hp, (player_pos[0], player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed_arch, hp, (player_pos[0] + 150, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos

def level_7():
    speed = 100
    hp = 100
    enemy_shape = (40, 40)
    enemy_respawn = 100
    shot_delay = 2.5
    enemies = []
    enemies.append(("archer", speed, hp, (player_pos[0] - 200, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] - 50, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] + 100, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] + 250, player_pos[1] + 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] - 200, player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] - 50, player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] + 100, player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    enemies.append(("archer", speed, hp, (player_pos[0] + 250, player_pos[1] - 250), enemy_shape, "bow", shot_delay))
    return enemies, enemy_respawn, player_pos
