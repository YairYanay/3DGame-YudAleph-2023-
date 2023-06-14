from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socket, protocol

# DATA
# map pos
GROUND_SIZE = 50

# wall pos = MIDDLE OF THE WALL adn size
WALL_FORWARD_POS = (0, 0, 25)
WALL_BACK_POS = (0, 0, -25)
WALL_RIGHT_POS = (25, 0, 0)
WALL_LEFT_POS = (-25, 0, 0)

WALL_SIZE = 3

# Data
POINT_END_TAME = 5

# Data server/client
IP_SERVER = '127.0.0.1'
PORT_SERVER = 8220

def handle_request(data):
    #SDGC = send game capacity
    if data[:4] == "SDGC":
        protocol.send_with_size(c_sock, data)

    #PLYP = player position
    elif data[:4] == "ENMP":
        protocol.send_with_size(c_sock, f"ENMP,{name_player},{player.x},{player.y},{player.z}")

def handle_server():
    global player_health
    data = ""
    try:
        data = protocol.recv_by_size(c_sock)

    except:
        pass

    if data:
        #STGM = start game
        if data[:4] == "STGM":
            print('Connected To Server!')

        #ENMP = enemy position
        elif data[:4] == 'ENMP':
            data = data.split(',')
            if name_player != str(data[1]):
                if str(data[1]) in dict_enemy:
                    enemy_entity = dict_enemy[str(data[1])]
                    enemy_entity.x, enemy_entity.y, enemy_entity.z = float(data[2]), float(data[3]), float(data[4])
                    data = ",".join(data)
                elif str(data[1]) in team_player:
                    team_entity = team_player[str(data[1])]
                    team_entity.x, team_entity.y, team_entity.z = float(data[2]), float(data[3]), float(data[4])
                    data = ",".join(data)

            else:
                player.x, player.y, player.z = float(data[2]), float(data[3]), float(data[4])
                # wait_text = Text(text='wait to the next round!', position=(0.2,0), scale=2, color=color.blue)
                # destroy(wait_text, delay=0.5)
                player.enabled = True
                player_health = 100
                for enemy in dict_enemy.values():
                    enemy.health = 100
                    if not enemy.enabled:
                        enemy.enable()
                        print("Enabled enemy:", enemy.name)

                for players in team_player.values():
                    players.health = 100
                    if not players.enabled:
                        players.enable()
                        print("Enabled enemy:", players.name)


        elif data[:4] == 'BLTP':
            data = data.split(',')
            bullet_animation_enemy(data[1:4], data[4], data[-1])

        elif data[:4] == 'EXIT':
            print("exit!!!")
            c_sock.close()
            application.quit()

        elif data[:4] == 'NMPL':
            data = data.split(',')[1:]

        elif data[:4] == 'TMWN':
            data = data.split(',')
            print(data[1] + " win!")
            if data[1] == "police":
                win_text = Text(text=f'{data[1]} win!', position=(0, 0.2),scale=2, color=color.blue)
            else:
                win_text = Text(text=f'{data[1]} win!', position=(0, 0),scale=2, color=color.brown)
            point_police = Text(text=f'{data[2]}', position=(-0.2, 0.2),scale=2, color=color.blue)
            point_robbers = Text(text=f'{data[3]}', position=(-0.2, 0),scale=2, color=color.brown)
            point_police_small_screen.text = f'{data[2]}'
            point_robber_small_screen.text = f'{data[3]}'
            print(data[2] + ":" + data[3])
            print(int(data[2]) == POINT_END_TAME)
            print(int(data[3]) == POINT_END_TAME)
            if int(data[2]) == POINT_END_TAME or int(data[3]) == POINT_END_TAME:
                print("game end!")
                time.sleep(2)
                send_exit_cmd()
                c_sock.close()
                application.quit()
                exit()
            destroy(win_text, delay=1)
            destroy(point_police, delay=1)
            destroy(point_robbers, delay=1)
            i = 0
            player_health = 100
            player_health_text.text = f'Player Health: {player_health}'
            for enemy in dict_enemy.values():
                enemy.health = 100
                enemy_texts[i].text = f'Enemy Health: {enemy.health}'
                i += 1
            data = ",".join(data)

        # elif data[:4] == 'PLYD':

    return data

def send_exit_cmd():
    protocol.send_with_size(c_sock, "EXIT")
    print('send exit data to server!')


def send_bullet_position(bullet_pos, obj_hit):
    protocol.send_with_size(c_sock, f"BLTP,{bullet_pos.x},{bullet_pos.y},{bullet_pos.z},{obj_hit},{name_player}")

def bullet_animation_enemy(bullet_pos, obj_hit, enemy_name):
    global player_health
    enemy = player
    for players in dict_enemy.values():
        if enemy_name == players.name:
            enemy = players

    for players in team_player.values():
        if enemy_name == players.name:
            enemy = players

    bullet_pos = Vec3(*[float(x) for x in bullet_pos])
    bullet = Entity(model='Data/bullet.obj', color=color.red, scale=0.01)
    bullet.position = enemy.world_position + Vec3(0, 1.5, 0)
    bullet.rotation = enemy.world_rotation

    bullet.animate_position(bullet_pos, duration=0.2, curve=curve.linear)  # Animate bullet to the point of collision
    if obj_hit == f'{name_player}':
        player_health -= 10
        player_health_text.text = f'{name_player} Health: {player_health}'
        if player_health <= 0:
            print("you dead!")
            protocol.send_with_size(c_sock, "IMDD")
            player.enabled = False

    elif obj_hit in team_player.values():
        i = 0
        for players in team_player.values():
            if players.name == obj_hit:
                players.health -= 10
                team_texts[i].text = f'{players.name} Health: {players.health}'
            if players.health <= 0:
                print("a player at your team is dead!")
                players.enabled = False
            i += 1

    elif obj_hit in dict_enemy.values():
        i = 0
        for enemy in dict_enemy.values():
            if enemy.name == obj_hit:
                enemy.health -= 10
                enemy_texts[i].text = f'{enemy.name} Health: {enemy.health}'
            if enemy.health <= 0:
                print("an enemy is dead!")
                enemy.enabled = False
            i += 1

    destroy(bullet, delay=0.2)


def fire_bullet():
    bullet = Entity(model='Data/bullet.obj', color=color.red, scale=0.01)
    bullet.position = player.camera_pivot.world_position
    bullet.rotation = player.camera_pivot.world_rotation

    hit_info = raycast(bullet.position, bullet.forward, ignore=[bullet])
    if hit_info.hit:
        if hit_info.entity in dict_enemy.values():
            enemy = dict_enemy[str(hit_info.entity)]
            enemy.health -= 10
            index = list(dict_enemy.values()).index(enemy)
            enemy_texts[index].text = f'{enemy.name} Health: {enemy.health}'
            if enemy.health <= 0:
                enemy.disable()
        elif hit_info.entity in team_player.values():
            print('you cant hit you team player!')
        send_bullet_position(hit_info.world_point, hit_info.entity)  # Send bullet position to other client
        bullet.animate_position(hit_info.world_point, duration=0.2, curve=curve.linear)  # Animate bullet to the point of collision
    destroy(bullet, delay=0.2)


def input(key):
    if held_keys['escape']:
        send_exit_cmd()
        application.quit()

    # Check if the TAB key is held down
    if held_keys['tab']:
        # Enable and show the small screen
        screen.enabled = True
        game_table_text.enabled = True
        title_game_text.enabled = True
        police_player_text.enabled = True
        robber_player_text.enabled = True
        player_health_text.enabled = True
        point_robber_small_screen.enabled = True
        point_police_small_screen.enabled = True
        for texts in num_text:
            texts.enabled = True

        for enemy_health_text in enemy_texts:
            enemy_health_text.enabled = True  # Show the enemy health text

        for team_health_text in team_texts:
            team_health_text.enabled = False  # Hide the enemy health text

    else:
        # Disable and hide the small screen
        screen.enabled = False
        game_table_text.enabled = False
        title_game_text.enabled = False
        police_player_text.enabled = False
        player_health_text.enabled = False
        robber_player_text.enabled = False
        point_police_small_screen.enabled = False
        point_robber_small_screen.enabled = False
        for enemy_health_text in enemy_texts:
            enemy_health_text.enabled = False  # Hide the enemy health text

        for team_health_text in team_texts:
            team_health_text.enabled = False  # Hide the enemy health text

        for texts in num_text:
            texts.enabled = False

    if player.enabled:
        #change height / ctrl
        if held_keys['control']:
            print('ctrl!')
            player.speed = 3
            camera.y = 0.001

        #change speed / shift
        elif held_keys['left shift'] or held_keys['right shift']:
            print('shift!')
            player.speed = 3

        else:
            player.y = 0
            camera.y = 0.25
            player.speed = 5

        if key == 'left mouse down':
            fire_bullet()


def update():
    try:
        handle_request("ENMP")
        handle_server()

    except:
        try:
            send_exit_cmd()
        except:
            print("socket down!")
        print('Closing client...')
        c_sock.close()
        application.quit()
        exit()


def main(game_capacity, name):
    global c_sock, player, enemy, gun_player, gun_enemy, ground, player_team_rtrn, team_player, enemy_texts, player_health, name_enemies, dict_enemy, screen, player_health_text, name_player, team_texts
    global game_table_text, title_game_text, police_player_text, num_text, player_health_text, robber_player_text, point_police_small_screen, point_robber_small_screen
    name_player = name
    # connect and send first msg from and to server
    try:
        c_sock = socket.socket()
        c_sock.connect((IP_SERVER, PORT_SERVER))
        print('connect sucsesfully to the server!')
        handle_request(f"SDGC,{game_capacity},{name_player}")
        print("waiting to players!")
        pos_player = handle_server()
        while pos_player[:4] != "STGM":
            pos_player = handle_server()
        name_enemies = handle_server()
        while not name_enemies:
            name_enemies = handle_server()
        player_team_rtrn = name_enemies[0]
        name_enemies = name_enemies[1:]
        print("game starting!!")

    except:
        try:
            send_exit_cmd()
        except:
            print('socket down!')
        print("server down!")
        application.quit()
        exit()

    # initialize Ursina
    app = Ursina(borderless=False)
    window.size = (800, 600)

    pos = [float(x) for x in pos_player.split(',')[1:]]
    pos = tuple(pos)
    print(pos)
    # players
    player = FirstPersonController(speed=5, position=pos)
    player.y = 0
    player_health = 100

    py = 0.13 * game_capacity
    if game_capacity >= 8:
        py = 0.07 * game_capacity
    screen = WindowPanel(title='', scale=(0.4, py), background_color=color.gray, enabled=False)
    screen.x = -0.4
    screen.y = 0.2

    dic = py / (game_capacity + 4)
    posy = 0.17
    game_table_text = Text(text='Game Table', parent=screen.content, y=posy, x=-0.47, enabled=False)
    posy -= 0.01
    title_game_text = Text(text='_____________', parent=screen.content, y=posy, x=-0.47, enabled=False)
    posy -= 0.04

    num_text = []
    enemy_texts = []
    team_texts = []
    team_player = {}
    dict_enemy = {}
    index_num = 1
    i = 0
    print(name_enemies)

    if player_team_rtrn == 'police':
        police_player_text = Text(text=f'{player_team_rtrn} team', parent=screen.content, y=posy, x=-0.55,
                                  color=color.blue, enabled=False)
        point_police_small_screen = Text(text='0', parent=screen.content, y=posy, x=-0.57, scale=1,
                                         color=color.blue, enabled=False)
        posy -= dic

        num_text.append(Text(text=f'{index_num}', parent=screen.content, y=posy, x=-0.55, enabled=False))
        player_health_text = Text(text=f'{name_player} Health: {player_health}', parent=screen.content, y=posy, x=-0.52, enabled=False)
        posy -= dic
        index_num += 1

        for j in range(game_capacity//2 - 1):
            players = Entity(model='Data/terrorist.obj', collider="box", name=f"{name_enemies[i]}", scale=(0.1, 0.07, 0.1), color=color.blue)
            players.health = 100
            team_player[f'{name_enemies[i]}'] = players
            num_text.append(Text(text=f'{index_num}', parent=screen.content, y=posy, x=-0.55, enabled=False))
            team_texts.append(Text(text=f'{name_enemies[i]} Health: {players.health}', parent=screen.content, y=posy, x=-0.52, enabled=False))
            posy -= dic
            index_num += 1

            # gun enemy
            gun_enemy = Entity(model='Data/ak.obj', color=color.black, scale=0.5)
            gun_parent_enemy = Entity(parent=players, position=(0.7, 20, 2))
            gun_enemy.parent = gun_parent_enemy
            gun_enemy.rotation = (0, 90, 0)
            i += 1


        robber_player_text = Text(text='robber team', parent=screen.content, y=posy, x=-0.55, color=color.brown, enabled=False)
        point_robber_small_screen = Text(text='0', parent=screen.content, y=posy, x=-0.57, scale=1,
                                         color=color.brown, enabled=False)
        posy -= dic
        index_num = 1
        for j in range(game_capacity // 2):
            enemy = Entity(model='Data/terrorist.obj', collider="box", name=f"{name_enemies[i]}",
                           scale=(0.1, 0.07, 0.1), color=color.brown)
            enemy.health = 100
            dict_enemy[f'{name_enemies[i]}'] = enemy
            num_text.append(Text(text=f'{index_num}', parent=screen.content, y=posy, x=-0.55, enabled=False))
            enemy_texts.append(
                Text(text=f'{name_enemies[i]} Health: {enemy.health}', parent=screen.content, y=posy, x=-0.52,
                     enabled=False))
            posy -= dic
            index_num += 1
            i += 1

            # gun enemy
            gun_enemy = Entity(model='Data/ak.obj', color=color.black, scale=0.5)
            gun_parent_enemy = Entity(parent=enemy, position=(0.7, 20, 2))
            gun_enemy.parent = gun_parent_enemy
            gun_enemy.rotation = (0, 90, 0)

    else:
        police_player_text = Text(text=f'{player_team_rtrn} team', parent=screen.content, y=posy, x=-0.55,
                                  color=color.brown, enabled=False)
        point_robber_small_screen = Text(text='0', parent=screen.content, y=posy, x=-0.57, scale=1,
                                         color=color.brown, enabled=False)
        posy -= dic

        num_text.append(Text(text=f'{index_num}', parent=screen.content, y=posy, x=-0.55, enabled=False))
        player_health_text = Text(text=f'{name_player} Health: {player_health}', parent=screen.content, y=posy, x=-0.52,
                                  enabled=False)
        posy -= dic
        index_num += 1

        for j in range(game_capacity // 2 - 1):
            players = Entity(model='Data/terrorist.obj', collider="box", name=f"{name_enemies[i]}",
                             scale=(0.1, 0.07, 0.1), color=color.brown)
            players.health = 100
            team_player[f'{name_enemies[i]}'] = players
            num_text.append(Text(text=f'{index_num}', parent=screen.content, y=posy, x=-0.55, enabled=False))
            team_texts.append(
                Text(text=f'{name_enemies[i]} Health: {players.health}', parent=screen.content, y=posy, x=-0.52,
                     enabled=False))
            posy -= dic
            index_num += 1

            # gun enemy
            gun_enemy = Entity(model='Data/ak.obj', color=color.black, scale=0.5)
            gun_parent_enemy = Entity(parent=players, position=(0.7, 20, 2))
            gun_enemy.parent = gun_parent_enemy
            gun_enemy.rotation = (0, 90, 0)
            i += 1

        robber_player_text = Text(text='police team', parent=screen.content, y=posy, x=-0.55, color=color.blue,
                                  enabled=False)
        point_police_small_screen = Text(text='0', parent=screen.content, y=posy, x=-0.57, scale=1,
                                         color=color.blue, enabled=False)
        posy -= dic

        index_num = 1
        for j in range(game_capacity // 2):
            enemy = Entity(model='Data/terrorist.obj', collider="box", name=f"{name_enemies[i]}",
                           scale=(0.1, 0.07, 0.1), color=color.blue)
            enemy.health = 100
            dict_enemy[f'{name_enemies[i]}'] = enemy
            num_text.append(Text(text=f'{index_num}', parent=screen.content, y=posy, x=-0.55, enabled=False))
            enemy_texts.append(
                Text(text=f'{name_enemies[i]} Health: {enemy.health}', parent=screen.content, y=posy, x=-0.52,
                     enabled=False))
            posy -= dic
            index_num += 1
            i += 1

            # gun enemy
            gun_enemy = Entity(model='Data/ak.obj', color=color.black, scale=0.5)
            gun_parent_enemy = Entity(parent=enemy, position=(0.7, 20, 2))
            gun_enemy.parent = gun_parent_enemy
            gun_enemy.rotation = (0, 90, 0)

    print(team_player)
    print(dict_enemy)
    # floor
    ground = Entity(model='plane', scale=(GROUND_SIZE, 1, GROUND_SIZE), color=color.lime, texture="grass",
                    texture_scale=(100, 100),
                    collider='mesh',name ="ground")

    # sky
    sky = Sky(collider="box", name='sky')

    # gun player
    gun_player = Entity(model='Data/ak.obj', color=color.black, scale=0.1)
    gun_parent_player  = Entity(parent=player, position=(0.7, 1, 1))
    gun_player.parent = gun_parent_player
    gun_player.rotation = (0, 90, 0)

    # create limits walls
    wall_forward = Entity(model='quad', collider="box", name='limit1', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_FORWARD_POS,
                          rotation=(0, 0, 0))
    wall_back = Entity(model='quad', collider="box", name='limit2', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_BACK_POS,
                       rotation=(180, 0, 0))
    wall_right = Entity(model='quad', collider="box", name='limit3', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_RIGHT_POS,
                        rotation=(0, 90, 0))
    wall_left = Entity(model='quad', collider="box", name='limit4', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_LEFT_POS,
                       rotation=(0, -90, 0))

    app.run()

if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
