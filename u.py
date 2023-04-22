# U - Universal Constants
import pygame

SCREEN_SIZE = 768
SPEED_OF_LIGHT = 500

ASTEROID_DELAY = 4
ASTEROID_SPEED = pygame.Vector2(100,0)
ASTEROID_TIMER_STOPPED = -9999
CENTER = pygame.Vector2(SCREEN_SIZE/2, SCREEN_SIZE/2)
MISSILE_LIFETIME = 3
MISSILE_LIMIT = 4
MISSILE_SPEED = SPEED_OF_LIGHT/3
SAFE_EMERGENCE_DISTANCE = 100
SAUCER_EMERGENCE_TIME = 7
SAUCER_MISSILE_DELAY = 0.5
SAUCER_MISSILE_LIMIT = 2
SAUCER_VELOCITY = pygame.Vector2(150, 0)
SAUCER_ZIG_TIME = 1
SHIPS_PER_QUARTER = 4
SHIP_ACCELERATION = pygame.Vector2(120, 0)
SHIP_EMERGENCE_TIME = 3
SHIP_ROTATION_STEP = 120
