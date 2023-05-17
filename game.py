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

# c_sock = socket.socket()
# c_sock.connect((IP_SERVER,PORT_SERVER))
# print('connect sucsesfully!')

def start_connect_server():
    pass
    # check_first_msg = False
    #
    # while not check_first_msg:
    #     try:
    #         # data = c_sock.recv(1024).decode()
    #         data = protocol.recv_by_size(c_sock)
    #         print(data)
    #         if ('OK' in data):
    #             check_first_msg = True
    #             break
    #     except:
    #         pass
    # print('Connected To Server!')

# def send_msg():
#     time.sleep(3)
#     num = str(random.randint(1,10))
#     print(num)
#     return protocol.send_with_size(c_sock, num)
#
# def recv_msg(c_sock):
#     # time.sleep(3)
#     print(f"msg recieve {protocol.recv_by_size(c_sock)}")

# initialize Ursina
app = Ursina(borderless=False)
window.size = (800,600)

#players
player = FirstPersonController(speed=5, position=(random.randint(1, 10), PLAYER_Y_POS, PLAYER_Z_POS))
anemy = Entity(model='Data/img/terrorist.obj', scale=(0.1,0.07,0.1))

#floor
ground = Entity(model='plane', scale=(MAP_X_POS, MAP_Y_POS, MAP_Z_POS), color=color.lime, texture="grass", texture_scale=(100, 100),
                collider='mesh')

#sky
sky = Sky()

#gun
gun = Entity(model='Data/img/ak.obj', scale=0.1)
gun_parent = Entity(parent=player, position=(0.7, 1, 1))
gun.parent = gun_parent
gun.rotation = (0, 90, 0)

#bullet
# blt = Entity(model='sphere', color=color.red, scale=0.1)
# blt.parent = gun
bullet = Entity(model='Data/img/bullet.obj', color=color.black, scale=0.01)

wall_1=Entity(model="cube", collider="box", position=(-8, 0, 0), scale=(8, 5, 1), rotation=(0,0,0),
	texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))
# wall_2 = duplicate(wall_1, z=5)
# wall_3=duplicate(wall_1, z=10)
# wall_4=Entity(model="cube", collider="box", position=(-15, 0, 10), scale=(1,5,20), rotation=(0,0,0),
# 	texture="brick", texture_scale=(5,5), color=color.rgb(255, 128, 0))

# create limits walls
wall_forward = Entity(model='quad', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_FORWARD_POS, rotation=(0,0,0))
wall_back = Entity(model='quad', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_BACK_POS, rotation=(180,0,0))
wall_right = Entity(model='quad', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_RIGHT_POS, rotation=(0,90,0))
wall_left = Entity(model='quad', color=color.rgb(255, 128, 0), scale=(50, 5), position=WALL_LEFT_POS, rotation=(0,-90,0))


def check_limits():
    if(player.x > MAP_X_POS/2 or player.x < -MAP_X_POS/2):
        player.x = 0
    if (player.y < -5):
        player.x, player.y, player.z = 0,0,0
    if (player.z > MAP_Z_POS/2 or player.z < -MAP_Z_POS/2):
        player.z = 0

def wall_move_zone():
    pass


def send_and_recv():
    pass
    # protocol.send_with_size(c_sock, f"ENMP,{player.x},{player.Y},{player.Z}")
    # try:
    #     data = protocol.recv_by_size(c_sock)
    # except:
    #     pass
    # if data:
    #     data = data.split(',')
    #     if(data[0] == 'ENMP'):
    #         print(data[1:])
    #         anemy.x, anemy.y, anemy.z = float(data[1]), float(data[2]), float(data[3])
    #         print(anemy.x, anemy.y, anemy.z)

def check_keys():
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


def on_bullet_hit(hit):
    pass
    # print("Bullet hit at:", hit.world_point)

def check_fire_derection():
    if held_keys['left mouse']:

        # ...

        # Set up bullet entity
        bullet = Entity(model='cube', color=color.red, scale=0.2)
        # bullet.position = camera.position + camera.forward * 2
        bullet.position = gun.world_position
        # bullet.position = Vec3(camera.x, camera.y, camera.z)

        # Calculate direction
        direction = camera.forward
        print(direction)

        # Calculate max distance to travel before hitting the ground
        max_distance = -bullet.y / direction.y

        # Calculate the point where the bullet will hit the ground
        ground_hit = bullet.position + max_distance * direction

        bullet.animate_position(ground_hit, duration=1, curve=curve.out_circ)
        # print(bullet.world_position)
        # # Calculate the closest object the bullet will hit (if any)
        # object_hit = raycast(bullet.position, direction, ignore=[bullet])
        #
        # # Calculate the distance to the object hit
        # if object_hit.entity:
        #     object_distance = (object_hit.entity.world_position - bullet.world_position).length()
        # else:
        #     object_distance = math.inf
        # print(object_distance, max_distance)
        # # Determine the duration and curve of the animation
        # if object_distance < max_distance:
        #     # Bullet will hit an object
        #     bullet.animate_position(ground_hit, duration=object_distance / 20.0, curve=curve.out_circ)
        #
        # else:
        #     # Bullet will hit the ground
        #     bullet.animate_position(ground_hit, duration=max_distance / 20.0, curve=curve.out_expo)
        #
        # sky_hit = raycast(camera.position, camera.forward, distance=100, ignore=[gun])
        # print(sky_hit.entity)
        # if not sky_hit.hit:
        #     bullet.animate_position(ground_hit, duration=max_distance / 20.0, curve=curve.out_expo)
        #     print("Shoot bullet!")

        # Fire the bullet

        # # print(camera.forward)
        # bullet.position = gun.world_position
        # #I take curve.out_expo for more speed but curve.linear is good but less speed
        # bullet.animate_position(bullet.world_position + player.forward * 5, duration=1, curve=curve.out_expo)
        # print(bullet.position)
        # print(player.position)
        # print(bullet.world_position)

        # # bullet = Entity(model='Data/img/bullet.obj', color=color.black, position=(-3, 8, -5), scale=0.1, rotation=(0, -90, 0))
        # # bullet.parent = gun
        # # # bullet.position = gsdun.position
        # # direction = (bullet.position - target.position).normalized()
        # # print(direction)
        # # bullet.animate_position(bullet.position + direction * 10, duration=1)
        # # print('Bullet position:', bullet.position)
        # bullet = Entity(model='Data/img/bullet.obj', color=color.black, position=(-6, 8, -4), scale=(0.05, 0.2, 0.05))
        # bullet.parent = Entity(parent=gun, position=(-6, 8, -4))
        # # bullet.position = gun.position + (0, 1, 0)
        # # print(bullet.position)
        # target_position = mouse.world_point
        # # print(target_position)
        # if target_position is None:
        #     return  # Ignore if target position is None
        # # target_position = (target_position.x, 1, target_position.z)
        # direction = (target_position - gun.position).normalized()
        # # if direction is not None:
        # direction.y = 1
        # print(direction.x, direction.x, direction.z)
        # print(direction)
        # bullet.look_at(bullet.position + direction)
        # bullet_ray = raycast(origin=bullet.position, direction=direction)
        #
        # if bullet_ray.hit:
        #     on_bullet_hit(bullet_ray)
        #
        # bullet_distance = bullet_ray.distance if bullet_ray.hit else 100
        # hit_point = bullet.position + direction * bullet_distance
        #
        # bullet.animate_position(hit_point, duration=bullet_distance / 10, curve=curve.linear)


        # hit_info = raycast(camera.position, camera.forward, distance=10, ignore=[camera], debug=True)
        # print(hit_info)


def fire_bullet():
    # Set up bullet entity
    bullet = Entity(model='cube', color=color.red, scale=0.2)
    # bullet.position = camera.position + camera.forward * 2
    bullet.position = gun.world_position
    # bullet.position = Vec3(camera.x, camera.y, camera.z)

    # Calculate direction
    direction = camera.forward

    # Calculate max distance to travel before hitting the ground
    max_distance = -bullet.y / direction.y

    # Calculate the point where the bullet will hit the ground
    ground_hit = bullet.position + max_distance * direction
    bullet.animate_position(ground_hit, duration=1, curve=curve.out_circ)
    

def input(key):
    if held_keys['escape']:
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
    # check_fire_derection()
    send_and_recv()
    # check_keys()
    check_limits()
    wall_move_zone()
    # print(gun_parent.world_position)
    # print(player.speed, camera.y)
    # print(player.x, player.y, player.z)
    if held_keys['escape']:
        application.quit()

# start_connect_server()
app.run()
# c_sock.close()