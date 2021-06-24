import pygame
import os
import ctypes

cwd = os.getcwd()
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
game_display = pygame.display.set_mode((0, 0))

print(screen_size)

def draw_background(screen_size, game_display):
    background = pygame.image.load("C:\\Users\\Elijah McLaughlin\\Desktop\\Python Projects\\Blob Ball\\blob_ball\\resources\\images\\triforce.jpg")
    background = pygame.transform.scale(background, screen_size)
    game_display.blit(background, (0, 0))

def handle_graphics():
    global screen_size
    global game_display
    draw_background(screen_size, game_display)
    pygame.display.flip()
    