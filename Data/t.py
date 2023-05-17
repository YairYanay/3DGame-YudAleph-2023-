from ursina.prefabs.first_person_controller import FirstPersonController

from ursina import *
from ursina import *
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from ursina.physics import *

app = Ursina()

# Set up camera
camera.position = (0, 2, -10)
camera.rotation_x = 10

#floor
ground = Entity(model='plane', scale=(50, 0, 50), color=color.lime, texture="grass", texture_scale=(100, 100),
                collider='mesh')

player = FirstPersonController()

# Create an enemy entity
enemy = Entity(model='cube', color=color.red, scale=2, position=(5, 0, 0))


# Create a wall entity
wall_1 = Entity(model='cube', collider='box', position=(0, 0, 10), scale=(8, 5, 1), rotation=(0, 0, 0), texture='brick', texture_scale=(5, 5), color=color.rgb(255, 128, 0))

# Set up gun entity
gun = Entity(model='cube', scale=(0.5, 0.5, 2), position=camera.position + (0, -0.5, 0.5), rotation=camera.rotation)

def input(key):
    if key == 'left mouse down':
        shoot_bullet()

def shoot_bullet():
    # Set up bullet entity
    bullet = Entity(model='cube', color=color.red, scale=0.2)
    bullet.position = gun.world_position

    # Calculate direction
    direction = camera.forward

    # Calculate max distance to travel before hitting the ground
    max_distance = -bullet.y / direction.y

    if max_distance > 0:
        # Calculate the point where the bullet will hit the ground
        ground_hit = bullet.position + max_distance * direction
        bullet.animate_position(ground_hit, duration=max_distance / 20.0, curve=curve.out_expo)

    else:
        # Shoot upwards
        shoot_upwards(bullet)

def shoot_upwards(bullet):
    # Calculate max height to reach
    max_height = 5

    # Calculate time to reach max height
    time_to_max_height = math.sqrt((2 * max_height) / abs(Physics.gravity.y))

    # Calculate vertical speed to reach max height
    speed = abs(Physics.gravity.y) * time_to_max_height

    # Calculate time to reach ground again
    time_to_ground = math.sqrt((2 * max_height) / abs(Physics.gravity.y))

    # Calculate the point where the bullet will hit the ground
    ground_hit = bullet.position + camera.forward * 10

    # Shoot bullet upwards and then downwards
    bullet.animate_position(bullet.position + (0, max_height, 0), duration=time_to_max_height / 2, curve=curve.out_expo, interrupt='kill')
    bullet.animate_position(ground_hit, duration=time_to_ground / 2, delay=time_to_max_height / 2, curve=curve.out_expo, interrupt='kill')

app.run()