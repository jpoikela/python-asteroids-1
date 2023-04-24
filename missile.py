# Missile

import pygame
import u


class Missile:
    def __init__(self, position, velocity, score_list):
        self.score_list = score_list
        self.saucer_score_list = [1000, 200]
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.radius = 2
        self.time = 0

    @classmethod
    def from_ship(cls, position, velocity):
        return cls(position, velocity, u.MISSILE_SCORE_LIST)

    @classmethod
    def from_saucer(cls, position, velocity):
        return cls(position, velocity, [0, 0, 0])

    def destroyed_by(self, attacker, missiles):
        if self in missiles: missiles.remove(self)

    def score_against(self, _):
        return 0

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, 4)

    def move(self, deltaTime):
        position = self.position + self.velocity * deltaTime
        position.x = position.x % u.SCREEN_SIZE
        position.y = position.y % u.SCREEN_SIZE
        self.position = position

    def update(self, missiles, delta_time):
        self.time += delta_time
        if self.time > u.MISSILE_LIFETIME:
            missiles.remove(self)

