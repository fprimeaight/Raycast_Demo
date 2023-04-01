import pygame
from math import pi, sin, cos, sqrt
from random import randint
from sys import exit

pygame.init()
scr_x = 800
scr_y = 400
scr = pygame.display.set_mode((scr_x,scr_y))
pygame.display.set_caption('3D Raycast')
clock = pygame.time.Clock()

def clamp(num, min_val, max_val):
   return max(min(num, max_val), min_val)

def generate_map(size):
    # Generates a random map with walls
    map = [[1 for i in range(size)] for j in range(size)]
    for i in range(1, size-1):
        for j in range(1, size-1):
            map[i][j] = randint(0,1)
    map[1][1] = 0
    return map

def main():
    tilemap = generate_map(11)

    pos_x, pos_y = (1,1)
    rotation = pi/4
    fov = 60
    wall_col_r, wall_col_g, wall_col_b = (21, 27, 109)
    shade_factor = 0.75

    while True:
        # Fill in background
        scr.fill((255, 255, 255))
        pygame.draw.rect(scr, (55,55,55), pygame.Rect((0, scr_y//2, scr_x, scr_y)))
        pygame.draw.rect(scr, (30,30,30), pygame.Rect((0, 0, scr_x, scr_y//2)))

        # Raycast logic
        for i in range(fov):
                rotated_i = rotation + (i - fov/2) * pi/180
                x, y = pos_x, pos_y
                n = 0
                while True:
                    x, y = (x + 0.01 * cos(rotated_i), y + 0.01 * sin(rotated_i))
                    n += 1
                    if tilemap[int(x)][int(y)] != 0:
                        h = 1/(0.0001 * n)

                        # Colour shading
                        dist = sqrt((pos_x - x) ** 2 + (pos_y - y) ** 2)
                        col = (clamp(wall_col_r * shade_factor / dist, 0, wall_col_r),
                               clamp(wall_col_g * shade_factor / dist, 0, wall_col_g),
                               clamp(wall_col_b * shade_factor / dist, 0, wall_col_b))
                        
                        pygame.draw.line(scr,
                                        col, 
                                        (i * scr_x/fov, scr_y/2 + h), 
                                        (i * scr_x/fov, scr_y/2 - h),
                                        width = scr_x//fov + 1)
                        break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            # Handling keyboard movement
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                rotation -= 0.1
            if keys[pygame.K_d]:
                rotation += 0.1
            if keys[pygame.K_w]:
                if tilemap[int(pos_x + 0.03 * cos(rotation))][int(pos_y + 0.03 * sin(rotation))] == 0:
                    pos_x += 0.03 * cos(rotation)
                    pos_y += 0.03 * sin(rotation)
            if keys[pygame.K_s]:
                if tilemap[int(pos_x - 0.03 * cos(rotation))][int(pos_y - 0.03 * sin(rotation))] == 0:
                    pos_x -= 0.03 * cos(rotation)
                    pos_y -= 0.03 * sin(rotation)
                
        pygame.display.update()
        clock.tick(60)

main()
