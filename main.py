# Copyright (C) 2019 Aydan Gooneratne

from t_opers import scale, add, subtract, dist_squared, dist
from planet import Planet
import math
import pygame
from pygame import Vector2
import sys
import random

pygame.init()
screen_width = 1400
screen_height = 800

screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
pygame.display.set_caption("gravity sim")
image = pygame.image.load('planet.png')
pygame.display.set_icon(image)

ARROW_FACTOR = 0.25
MIN_ACCEL = 0
MAX_ACCEL = 2
FRICTION_COEFFICIENT = 1
BOUNCE_COEFFICIENT = 1.0
GRAVITY_COEFFICIENT = 1

stars = [pygame.Rect(random.randint(0, screen_width), random.randint(0, screen_height), 2, 2) for _ in range(100)]
planets = []
dots = []  # array of triple tuples where the first 2 values are the x,y and the last is time
curr_planet = None


def draw_background():
    screen.fill(pygame.Color("black"))


def draw_stars():
    for star in stars:
        pygame.draw.rect(screen, pygame.Color("white"), star)


def draw_string(str, pos):
    basic_font = pygame.font.SysFont("Times New Roman", 14)
    text = basic_font.render(str, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = pos[0] - (text_rect.width / 2)
    text_rect.centery = pos[1] - (text_rect.height / 2)
    screen.blit(text, text_rect)


def draw_dot(d):
    pygame.draw.rect(screen, pygame.Color("white"), pygame.Rect(d[0], d[1], 1, 1))
    d[2] = d[2] - 1


def draw_planet(p: Planet):
    if p.get_pos()[0] - p.get_radius() > screen_width:
        p.set_pos((0 - p.get_radius(), p.get_pos()[1]))
    elif p.get_pos()[0] + p.get_radius() < 0:
        p.set_pos((screen_width + p.get_radius(), p.get_pos()[1]))

    if p.get_pos()[1] - p.get_radius() > screen_height:
        p.set_pos((p.get_pos()[0], 0 - p.get_radius()))
    elif p.get_pos()[1] + p.get_radius() < 0:
        p.set_pos((p.get_pos()[0], screen_height + p.get_radius()))

    pygame.draw.circle(screen, p.get_color(), p.get_pos(), p.get_radius())

    velocity = Vector2(p.get_vel())
    if velocity.magnitude() > 0:
        try:
            velocity.scale_to_length(p.get_radius())
        except ValueError:
            print("faulty scale_to_length")


def gravity(p, other):
    dist = dist_squared(p.get_pos(), other.get_pos())
    if dist != 0:
        a = other.get_mass() / dist
    else:
        a = MAX_ACCEL

    x_component = p.get_pos()[0] - other.get_pos()[0]
    y_component = p.get_pos()[1] - other.get_pos()[1]
    force = Vector2(x_component, y_component)
    if force.magnitude() != 0:
        force.normalize()
        force.scale_to_length(-1 * a * GRAVITY_COEFFICIENT)
    p.shift_vel(force)


def find_vel(p_m, p_pos, p_vel, o_m, o_pos, o_vel):
    m1 = p_m
    m2 = o_m
    c_axis = Vector2(subtract(o_pos, p_pos))
    o_axis = Vector2(1, 0)
    forward_ang = c_axis.angle_to(o_axis)
    p_new_vel = Vector2(p_vel).rotate(forward_ang)
    o_new_vel = Vector2(o_vel).rotate(forward_ang)
    new_x = BOUNCE_COEFFICIENT * FRICTION_COEFFICIENT * (((m1 - m2) * p_new_vel.x) + (2 * m2 * o_new_vel.x)) / (m1 + m2)
    new_y = p_new_vel.y
    return Vector2(new_x, new_y).rotate(-1 * forward_ang)


def collision(p, other):
    d = dist(p.get_pos(), other.get_pos())
    if d - p.get_radius() - other.get_radius() < 0:

        overlap = math.fabs(d - p.get_radius() - other.get_radius())
        d2 = Vector2(subtract(other.get_pos(), p.get_pos()))
        if d2.magnitude() != 0:
            d2.scale_to_length(-1 * overlap)

        if p.get_mass() < other.get_mass() or other.UNMOVABLE:
            p.shift_pos(d2)
        else:
            other.shift_pos(d2.rotate(180))

        p_m = p.get_mass()
        o_m = other.get_mass()
        p_pos = p.get_pos()
        o_pos = other.get_pos()
        p_vel = p.get_vel()
        o_vel = other.get_vel()
        if not p.UNMOVABLE:
            p.set_vel(find_vel(p_m, p_pos, p_vel, o_m, o_pos, o_vel))
            new_acc = Vector2(p.get_vel())
            if new_acc.magnitude() > 0:
                try:
                    new_acc.scale_to_length(new_acc.magnitude() * -0.1)
                except ValueError:
                    print("faulty scale_to_length")
            p.shift_vel(new_acc)
        if not other.UNMOVABLE:
            other.set_vel(find_vel(o_m, o_pos, o_vel, p_m, p_pos, p_vel))
            new_acc = Vector2(other.get_vel())
            if new_acc.magnitude() > 0:
                try:
                    new_acc.scale_to_length(new_acc.magnitude() * -0.1)
                except ValueError:
                    print("faulty scale_to_length")
            other.shift_vel(new_acc)


def apply_forces(p: Planet):
    for other in planets:
        if p is not other and not p.UNMOVABLE:
            collision(p, other)
            gravity(p, other)


# Loop
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if curr_planet is None:
                pos = pygame.mouse.get_pos()
                curr_planet = Planet(Vector2(pos), Vector2(0, 0), 0.1)
                if pygame.mouse.get_pressed()[2]:
                    curr_planet.UNMOVABLE = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if curr_planet is not None:
                planets.append(curr_planet)
                curr_planet = None
        elif event.type == pygame.MOUSEMOTION:
            if curr_planet is not None:
                m_pos = pygame.mouse.get_pos()
                p_pos = curr_planet.get_pos()
                curr_planet.set_vel(scale(subtract(m_pos, p_pos), ARROW_FACTOR))
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                GRAVITY_COEFFICIENT = GRAVITY_COEFFICIENT + 0.1 if GRAVITY_COEFFICIENT + 0.1 < 3 else 3
            elif event.key == pygame.K_DOWN:
                GRAVITY_COEFFICIENT = GRAVITY_COEFFICIENT - 0.1 if GRAVITY_COEFFICIENT - 0.1 >= 0 else 0
            elif event.key == pygame.K_BACKSPACE:
                if len(planets) > 0:
                    planets.pop(len(planets) - 1)
            elif event.key == pygame.K_ESCAPE:
                planets.clear()

    draw_background()
    draw_stars()
    draw_string("gravity:" + str("{:.1f}".format(GRAVITY_COEFFICIENT)), (60, 20))
    for dot in dots:
        draw_dot(dot)
        if dot[2] == 0:
            dots.remove(dot)

    if curr_planet is not None:
        curr_planet.shift_radius(0.2)
        pygame.draw.line(screen, pygame.Color("white"), curr_planet.get_pos(), pygame.mouse.get_pos(), 1)
        draw_planet(curr_planet)

    for planet in planets:
        apply_forces(planet)
        planet.move()
        draw_planet(planet)
        dots.append([planet.get_pos()[0], planet.get_pos()[1], 120])

    pygame.display.update()

pygame.quit()
sys.exit()
