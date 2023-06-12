from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socket, protocol

# DATA
#map pos
GROUND_SIZE = 50

#wall pos = MIDDLE OF THE WALL adn size
WALL_FORWARD_POS = (0, 0, 25)
WALL_BACK_POS = (0, 0, -25)
WALL_RIGHT_POS = (25, 0, 0)
WALL_LEFT_POS = (-25, 0, 0)

WALL_SIZE = 3

#Data server/client
IP_SERVER = '127.0.0.1'
PORT_SERVER = 8200

def handle_request(data):
    #SDGC = send game capacity
    if data[:4] == "SDGC":
        protocol.send_with_size(c_sock, data)

    #PLYP = player position
    elif data[:4] == "ENMP":
        protocol.send_with_size(c_sock, f"ENMP,{number_player},{player.x},{player.y},{player.z}")

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
            # print(dict_enemy[f'enemy{data[1]}'])
            # print(int(number_player) != int(data[1]))
            if int(number_player) != int(data[1]):
                enemy_entity = dict_enemy['enemy' + data[1]]
                enemy_entity.x, enemy_entity.y, enemy_entity.z = float(data[2]), float(data[3]), float(data[4])
                data = ",".join(data)

            else:
                player.x, player.y, player.z = float(data[2]), float(data[3]), float(data[4])
                # wait_text = Text(text='wait to the next round!', position=(0.2,0), scale=2, color=color.blue)
                # destroy(wait_text, delay=0.5)
                player.enabled = True
                for enemy in dict_enemy.values():
                    enemy.health = 100
                    player_health = 100
                    if not enemy.enabled:
                        enemy.enable()
                        print("Enabled enemy:", enemy.name)


        elif data[:4] == 'BLTP':
            data = data.split(',')
            bullet_animation_enemy(data[1:-1], data[-1])

        elif data[:4] == 'EXIT':
            print("exit!!!")
            c_sock.close()
            application.quit()

        elif data[:4] == 'NMPL':
            data = data.split(',')[1]

        elif data[:4] == 'TMWN':
            data = data.split(',')
            print(data[1] + " win!")
            if data[1] == "police":
                win_text = Text(text=f'{data[1]} win!', position=(0, 0.2),scale=2, color=color.blue)
            else:
                win_text = Text(text=f'{data[1]} win!', position=(0, 0.2),scale=2, color=color.brown)
            destroy(win_text, delay=1)
            data = ",".join(data)

        # elif data[:4] == 'PLYD':

    return data

def send_exit_cmd():
    protocol.send_with_size(c_sock, "EXIT")
    print('send exit data to server!')


def send_bullet_position(bullet_pos, obj_hit):
    protocol.send_with_size(c_sock, f"BLTP,{bullet_pos.x},{bullet_pos.y},{bullet_pos.z},{obj_hit}")

def bullet_animation_enemy(bullet_pos, obj_hit):
    global player_health
    bullet_pos = Vec3(*[float(x) for x in bullet_pos])
    bullet = Entity(model='Data/bullet.obj', color=color.red, scale=1)
    bullet.position = enemy.world_position + Vec3(0,0,-5)
    bullet.rotation = enemy.world_rotation

    bullet.animate_position(bullet_pos, duration=0.2, curve=curve.linear)  # Animate bullet to the point of collision
    if obj_hit == f'enemy{number_player}':
        player_health -= 10
        player_health_text.text = f'Player Health: {player_health}'
        if player_health <= 0:
            print("player dead!")
            protocol.send_with_size(c_sock, "IMDD")
            player.enabled = False

    destroy(bullet, delay=0.2)

def fire_bullet():
    bullet = Entity(model='Data/bullet.obj', color=color.red, scale=0.01)
    bullet.position = player.camera_pivot.world_position
    bullet.rotation = player.camera_pivot.world_rotation

    hit_info = raycast(bullet.position, bullet.forward, ignore=[bullet])
    if hit_info.hit:
        if 'enemy' in str(hit_info.entity):
            enemy = dict_enemy[str(hit_info.entity)]
            enemy.health -= 10
            enemy.text = f'Enemy Health: {enemy.health}'
            if enemy.health <= 0:
                enemy.disable()
                # protocol.send_with_size(c_sock, "PLYD")
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
        screen.visible = True
    else:
        # Disable and hide the small screen
        screen.enabled = False
        screen.visible = False

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


def main(game_capacity):
    global c_sock, player, enemy, gun_player, gun_enemy, ground, enemy_texts, player_health, number_player, dict_enemy, screen, player_health_text
    # connect and send first msg from and to server
    try:
        c_sock = socket.socket()
        c_sock.connect((IP_SERVER, PORT_SERVER))
        print('connect sucsesfully to the server!')
        handle_request(f"SDGC,{game_capacity}")
        print("waiting to players!")
        pos_player = handle_server()
        while pos_player[:4] != "STGM":
            pos_player = handle_server()
        number_player = handle_server()
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

    pos = [int(x) for x in pos_player.split(',')[1:]]

    # players
    player = FirstPersonController(speed=5, position=tuple(pos))
    player_health = 100
    # player.y = 0


    # Create the small screen
    screen = WindowPanel(title='Game Table', width=0.3*game_capacity, height=0.2*game_capacity, background_color=color.gray, enabled=False)
    screen.x = -0.4
    screen.y = 0.2
    # Player and enemy health text
    player_health_text = Text(text=f'Player Health: {player_health}', parent=screen.content, y=0.05)


    enemy_texts = []
    dict_enemy = {}
    i = 1
    print(number_player)
    while len(dict_enemy) != game_capacity - 1:
        if int(number_player) != i:
            enemy = Entity(model='Data/terrorist.obj', collider="box", name=f"enemy{i}", scale=(0.1, 0.07, 0.1))
            enemy.health = 100
            dict_enemy[f'enemy{i}'] = enemy
            enemy_texts.append(Text(text=f'Enemy Health: {enemy.health}', parent=screen.content, y=-0.05))
        i += 1
        # enemy_text = Text(text=f"Health: {enemy.health}", origin=(0, 0), y=-0.4)  # Create the enemy_text entity
        # enemy_text.position = enemy.world_position + (0, 1, 0)

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

    # gun enemy
    gun_enemy = Entity(model='Data/ak.obj', color=color.black, scale=0.5)
    gun_parent_enemy = Entity(parent=enemy, position=(0.7, 20, 2))
    gun_enemy.parent = gun_parent_enemy
    gun_enemy.rotation = (0, 90, 0)

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
    game_capacity = int(sys.argv[1])
    main(game_capacity)
