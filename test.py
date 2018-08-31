import pymunk
import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))

space = pymunk.Space()
space.gravity = (0, 0)

mass = 1

chassis_shape = pymunk.Poly.create_box(None, size=(100, 100), radius=0.05)
chassis_shape.friction = 0
chassis_moment = pymunk.moment_for_poly(mass, chassis_shape.get_vertices())
chassis = pymunk.Body(mass, chassis_moment)
chassis_shape.body = chassis
chassis.position = 640, 360

wheel1_shape = pymunk.Poly.create_box(None, size=(50, 50), radius=0.05)
wheel1_shape.friction = 0
wheel1_moment = pymunk.moment_for_poly(mass, wheel1_shape.get_vertices())
wheel1 = pymunk.Body(mass, wheel1_moment)
wheel1_shape.body = wheel1
wheel1.position = 565, 360

wheel2_shape = pymunk.Poly.create_box(None, size=(50, 50), radius=0.05)
wheel2_shape.friction = 0
wheel2_moment = pymunk.moment_for_poly(mass, wheel2_shape.get_vertices())
wheel2 = pymunk.Body(mass, wheel2_moment)
wheel2_shape.body = wheel2
wheel2.position = 715, 360

axel1 = pymunk.SlideJoint(chassis, wheel1, chassis.center_of_gravity, wheel1.center_of_gravity, 74, 76)
# axel1.collide_bodies = 0
axel2 = pymunk.SlideJoint(chassis, wheel2, chassis.center_of_gravity, wheel2.center_of_gravity, 74, 76)
# axel2.collide_bodies = 0


space.add(chassis, chassis_shape, wheel1, wheel1_shape, wheel2, wheel2_shape, axel1, axel2)


def draw_poly(shape):
    verts = []
    for v in shape.get_vertices():
        x = v.rotated(shape.body.angle)[0] + shape.body.position[0]
        y = v.rotated(shape.body.angle)[1] + shape.body.position[1]
        verts.append((x, y))
    pygame.draw.polygon(screen, [255, 255, 255], verts)


while True:
    screen.fill([0, 0, 0])
    wheel2.apply_impulse_at_local_point((0, -9), wheel2.center_of_gravity)
    wheel1.apply_impulse_at_local_point((0, 9), wheel1.center_of_gravity)
    draw_poly(chassis_shape)
    draw_poly(wheel1_shape)
    draw_poly(wheel2_shape)

    space.step(0.02)
    pygame.display.update()

    wheel1.velocity = (0, 0)
    wheel2.velocity = (0, 0)
