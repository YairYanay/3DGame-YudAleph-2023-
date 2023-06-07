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
PORT_SERVER = 8201

def handle_request(data):
    #SDGC = send game capacity
    if data[:4] == "SDGC":
        protocol.send_with_size(c_sock, data)
    #PLYP = player position
    elif data[:4] == "ENMP":
        # print(f"ENMP,{player.x},{player.Y},{player.Z}")
        protocol.send_with_size(c_sock, f"ENMP,{player.x},{player.Y},{player.Z}")


def handle_server():
    data = ""
    try:
        data = protocol.recv_by_size(c_sock)
    except:
        pass

    if data:
        #STGM = start game
        if data[:4] == "STGM":
            print('Connected To Server!')

        #RCGC = recv game capacity
        elif data[:4] == "RCGC":
            print("asdknasjkda")
            exit()

        #ENMP = enemy position
        elif(data[:4] == 'ENMP'):
            data = data.split(',')
            enemy.x, enemy.y, enemy.z = float(data[1]), float(data[2]), float(data[3])
            data = ",".join(data)

        elif(data[:4] == 'EXIT'):
            print("exit!!!")
            c_sock.close()
            application.quit()

    return data

def send_exit_cmd():
    protocol.send_with_size(c_sock, "EXIT")
    print('send exit data to server!')


def on_bullet_hit(hit):
    pass
    # print("Bullet hit at:", hit.world_point)

def fire_bullet():
    bullet = Entity(model='Data/bullet.obj', color=color.red, scale=0.01)
    bullet.position = player.camera_pivot.world_position
    bullet.rotation = player.camera_pivot.world_rotation

    hit_info = raycast(bullet.position, bullet.forward, ignore=[bullet])
    if hit_info.hit:
        print(hit_info.entity)
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
    try:
        handle_request("ENMP")
        handle_server()

    except:
        print('Closing client...')
        c_sock.close()
        exit()


def main(game_capacity):
    global c_sock, player, enemy, gun, ground
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
        print("game starting!!")

    except:
        print("server down!")
        exit()

    # initialize Ursina
    app = Ursina(borderless=False)
    window.size = (800, 600)

    pos = [int(x) for x in pos_player.split(',')[1:]]
    # players
    player = FirstPersonController(speed=5, position=tuple(pos))
    enemy = Entity(model='Data/terrorist.obj',collider="box", name="enemy", scale=(0.1, 0.07, 0.1))

    # floor
    ground = Entity(model='plane', scale=(GROUND_SIZE, 1, GROUND_SIZE), color=color.lime, texture="grass",
                    texture_scale=(100, 100),
                    collider='mesh',name ="ground")

    # sky
    sky = Sky(collider="box", name='sky')

    # gun
    gun = Entity(model='Data/ak.obj', scale=0.1)
    gun_parent = Entity(parent=player, position=(0.7, 1, 1))
    gun.parent = gun_parent
    gun.rotation = (0, 90, 0)

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