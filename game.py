from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import socket, protocol
import random

# DATA
#map pos
MAP_X_POS = 50
MAP_Y_POS = 0
MAP_Z_POS = 50

#player pos
# PLAYER_X_POS = 1
PLAYER_Y_POS = 1
PLAYER_Z_POS = 0

#wall pos = MIDDLE OF THE WALL
WALL_FORWARD_POS = (0, 0, 25)
WALL_BACK_POS = (0, 0, -25)
WALL_RIGHT_POS = (25, 0, 0)
WALL_LEFT_POS = (-25, 0, 0)

#Data server/client
IP_SERVER = '127.0.0.1'
PORT_SERVER = 8201


def send_and_recv():
    protocol.send_with_size(c_sock, f"ENMP,{player.x},{player.Y},{player.Z}")
    data = ""
    try:
        data = protocol.recv_by_size(c_sock)
    except:
        pass

    if data:
        if(data[:4] == 'ENMP'):
            data = data.split(',')
            # print(data[1:])
            enemy.x, enemy.y, enemy.z = float(data[1]), float(data[2]), float(data[3])
            # print(anemy.x, anemy.y, anemy.z)

        if(data[:4] == 'EXIT'):
            c_sock.close()
            application.quit()


def send_exit_cmd():
    protocol.send_with_size(c_sock, f"EXIT")
    print('send exit data to server!')


def on_bullet_hit(hit):
    pass
    # print("Bullet hit at:", hit.world_point)

def fire_bullet():
    bullet = Entity(model='Data/img/bullet.obj', color=color.red, scale=0.01)
    bullet.position = player.camera_pivot.world_position
    bullet.rotation = player.camera_pivot.world_rotation

    hit_info = raycast(bullet.position, bullet.forward, ignore=[bullet])
    if hit_info.hit:
        if hit_info.entity == enemy:
            print("Enemy Hit!")
        bullet.animate_position(hit_info.world_point, duration=0.2, curve=curve.linear)  # Animate bullet to the point of collision
        destroy(bullet, delay=0.2)




def input(key):
    if held_keys['escape']:
        send_exit_cmd()
        application.quit()

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
        camera.y = 0.25
        player.speed = 5

    if key == 'left mouse down':
        fire_bullet()


def update():
    send_and_recv()

    if held_keys['escape']:
        application.quit()

def start_connect_server():
    check_first_msg = False

    while not check_first_msg:
        try:
            # data = c_sock.recv(1024).decode()
            data = protocol.recv_by_size(c_sock)
            print(data)
            if ('OK' in data):
                check_first_msg = True
                break
        except:
            pass
    print('Connected To Server!')

def main():
    global c_sock, player, enemy, gun, ground
    # connect and send first msg from and to server
    c_sock = socket.socket()
    c_sock.connect((IP_SERVER, PORT_SERVER))
    print('connect sucsesfully!')
    start_connect_server()

    # initialize Ursina
    app = Ursina(borderless=False)
    window.size = (800, 600)

    # players
    player = FirstPersonController(speed=5, position=(random.randint(1, 10), PLAYER_Y_POS, PLAYER_Z_POS))
    enemy = Entity(model='Data/img/terrorist.obj',collider="box", name="enemy", scale=(0.1, 0.07, 0.1))

    # floor
    ground = Entity(model='plane', scale=(MAP_X_POS, MAP_Y_POS, MAP_Z_POS), color=color.lime, texture="grass",
                    texture_scale=(100, 100),
                    collider='mesh',name ="ground")

    # sky
    sky = Sky(collider="box", name='sky')

    # gun
    gun = Entity(model='Data/img/ak.obj', scale=0.1)
    gun_parent = Entity(parent=player, position=(0.7, 1, 1))
    gun.parent = gun_parent
    gun.rotation = (0, 90, 0)

    wall_1 = Entity(name ="wall",model="cube", collider="box", position=(-8, 0, 0), scale=(8, 5, 1), rotation=(0, 0, 0),
                    texture="brick", texture_scale=(5, 5), color=color.rgb(255, 128, 0))

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

main()