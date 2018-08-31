import pygame
import pymunk
import ast
import math
import random

pygame.init()
clock = pygame.time.Clock()
width, height = 1280, 720
screen = pygame.display.set_mode((width, height))
icon = pygame.image.load("favicon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Pyvlov's Dog - Simulation")
screen.fill([51, 153, 51])
paint_brush = None
aa = False

space = pymunk.Space()

###boundaries###

top_bb = pymunk.Body(1, 0, pymunk.Body.STATIC)
top_bs = pymunk.Segment(top_bb, (0, 0), (1280, 0), 2)
top_bb.position = 0, 0

left_bb = pymunk.Body(1, 0, pymunk.Body.STATIC)
left_bs = pymunk.Segment(left_bb, (0, 0), (0, 720), 2)
left_bb.position = 0, 0

right_bb = pymunk.Body(1, 0, pymunk.Body.STATIC)
right_bs = pymunk.Segment(right_bb, (0, 0), (0, 720), 2)
right_bb.position = 1280, 0

bottom_bb = pymunk.Body(1, 0, pymunk.Body.STATIC)
bottom_bs = pymunk.Segment(bottom_bb, (0, 0), (1280, 0), 2)
bottom_bb.position = 0, 720

space.add(top_bb, top_bs, left_bb, left_bs, right_bb, right_bs, bottom_bb, bottom_bs)


def space_step(dt, wheel_vols, dog):
    dog.body.apply_impulse_at_local_point((0.00, wheel_vols[0] * dog.parts[1].circ), dog.parts[1].loc)
    dog.body.apply_impulse_at_local_point((0.00, wheel_vols[1] * dog.parts[2].circ), dog.parts[2].loc)
    space.step(dt)
    dog.body.angular_velocity = 0
    dog.body.velocity = (0, 0)
    space.step(dt)


def zero(p_tuple, bbox_tuple):
    x = bbox_tuple[0]
    y = bbox_tuple[1]
    return (p_tuple[0] - x, p_tuple[1] - y)


class Part:
    def __init__(self, name, colour, vertices, input_link, settings, collide, wheel, file):
        self.name = name
        self.colour = colour
        self.vertices = ast.literal_eval(vertices)
        self.input_link = input_link
        self.settings = settings
        self.collide = collide
        self.wheel = wheel
        self.z_verts = []
        self.bbox = ast.literal_eval(file[0])
        self.circ = None

        for tple in self.vertices:
            self.z_verts.append(zero(tple, self.bbox))

        x = 0
        y = 0
        for vert in self.z_verts:
            x += vert[0]
            y += vert[1]
        x = x / len(self.z_verts)
        y = y / len(self.z_verts)

        self.middle = (x, y)
        # print(self.middle)

        if self.wheel == "1":
            self.circ = (self.z_verts[1][1] - self.z_verts[2][1]) * math.pi

        ###pymunk###
        self.shape = pymunk.Poly(None, self.z_verts, radius=0.5)
        self.shape.friction = 0
        self.moment = pymunk.moment_for_poly(1, self.shape.get_vertices())

        if self.name in collision_types:
            self.shape.collision_type = collision_types[self.name]
            self.handler = Coll_Handler(self.shape.collision_type, collision_types[self.input_link])


    def draw(self, body):
        c_g = self.colour
        try:
            if len(c_g) != 9:
                raise Exception
            colour = [int(c_g[0:3]), int(c_g[3:6]), int(c_g[6:9])]
            if any(x not in range(0, 256) for x in colour):
                raise Exception
        except Exception:
            colour = [0, 0, 0]

        verts = []
        for v in self.shape.get_vertices():
            x = v.rotated(body.angle)[0] + body.position[0]
            y = v.rotated(body.angle)[1] + body.position[1]
            verts.append((x, y))
        pygame.draw.polygon(screen, colour, verts)


class Coll_Handler:
    def __init__(self, dog_part, object_part):
        print(dog_part, object_part)
        self.dog_part = dog_part
        self.object_part = object_part
        self.handler = space.add_collision_handler(dog_part, object_part)
        self.handler.begin = self.collision
        self.handler.separate = self.detatch

    def collision(self, arbiter, space, data):
        global var
        var[self.dog_part] = 1
        return True

    def detatch(self, arbiter, space, data):
        global var
        var[self.dog_part] = 0
        return False


class Dog:
    def __init__(self, location):
        self.location = location
        self.datafile = open(location + "\\data.txt", "r").read()
        self.datafile = self.datafile.split("\n")
        self.parts = []
        self.wheels = []
        self.chassis = None
        self.mass = 1
        self.moment = 0
        self.body = pymunk.Body(self.mass, self.moment)
        self.body.position = 640, 360
        space.add(self.body)
        # TODO real centre value
        part_number = 0
        for line in range(len(self.datafile)):
            if self.datafile[line] == "#start#":
                self.parts.append(Part(self.datafile[line + 1], self.datafile[line + 2], self.datafile[line + 3],
                                       self.datafile[line + 4], self.datafile[line + 5], self.datafile[line + 6],
                                       self.datafile[line + 7], self.datafile))
                if self.parts[-1].settings == "chassis":
                    self.chassis = self.parts[-1]
                self.moment += self.parts[-1].moment
                self.body.moment = self.moment
                self.parts[-1].shape.body = self.body
                part_number += 1
        for part in self.parts:
            x = part.middle[0] - (part.bbox[2] - part.bbox[0]) / 2
            y = part.middle[1] - (part.bbox[3] - part.bbox[1]) / 2
            part.loc = (x, y)
            space.add(part.shape)

    def draw(self):
        for part in self.parts:
            part.draw(self.body)


class Object:
    def __init__(self, name, colour, collide, size, alpha):
        self.name = name
        self.colour = colour
        self.collide = collide
        self.size = size
        self.alpha = alpha
        self.copies = []
        self.locs = []
        self.surfaces = []

        # for input in inputs:
        #     if self.name == inputs[input].collides_with:
        #         self.create_collision(input)
        #         break
        #     # inputs[self.name].handler = space.add_collision_handler(inputs[self.name].)

    def generate(self, xy):
        # for input in inputs:
        #     if self.name == inputs[input].collides_with:
        #         self.create_collision(input)
        #         break
        self.collision_type = collision_types[self.name]
        self.body = pymunk.Body(mass=0, moment=0, body_type=pymunk.Body.STATIC)
        self.body.position = xy
        self.copies.append(pymunk.Poly.create_box(self.body, (self.size, self.size), radius=1))
        self.copies[-1].collision_type = self.collision_type
        space.add(self.body, self.copies[-1])

    def drawall(self):
        c_g = self.colour
        try:
            if len(c_g) != 9:
                raise Exception
            colour = [int(c_g[0:3]), int(c_g[3:6]), int(c_g[6:9]), int(self.alpha)]
            if any(x not in range(0, 256) for x in colour):
                raise Exception
        except Exception:
            c_g = "000000000"
        if self.copies != []:
            colour = pygame.Color(int(c_g[0:3]), int(c_g[3:6]), int(c_g[6:9]), int(self.alpha))
        for obj in self.copies:
            verts = []
            for v in obj.get_vertices():
                x = v[0] + obj.body.position[0]
                y = v[1] + obj.body.position[1]
                verts.append((x, y))
            pygame.draw.polygon(screen, colour, verts)
            # print(inputs["LDR"].handler.post_solve)


def draw_obj(md, ml):
    if paint_brush != None and md == 1 and not any(x == ml for x in obj_list[paint_brush].locs):
        obj_list[paint_brush].generate(ml)


def simon():
    global sim
    sim = 1


def simoff():
    global sim
    sim = 0


obj_list = []
collision_types = {
    "Brick": 1,
    "Light": 2,
    "LDR": 3,
    "L Bump": 4,
    "R Bump": 5
}
sim = 0
rot = 0
global len_obj
len_obj = 0

var = [0, 0, 0, 0, 0, 0]




def update_sim(dog):
    screen.fill([51, 153, 51])
    draw_obj(pygame.mouse.get_pressed()[0], pygame.mouse.get_pos())
    dog.draw()
    for obj in obj_list:
        obj.drawall()

    pygame.display.update()
