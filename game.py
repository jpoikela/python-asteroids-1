# Game

from pygame import Vector2

from asteroid import Asteroid
import pygame

from collider import Collider
from saucer import Saucer
from ship import Ship
import u


class Game:
    def __init__(self, testing=False):
        self.init_general_game_values()
        self.init_asteroids_game_values()
        self.init_space_objects()
        self.init_pygame_and_display(testing)

    # noinspection PyAttributeOutsideInit
    def init_general_game_values(self):
        self.delta_time = 0
        self.elapsed_time = 0
        self.game_over = False
        self.running = False
        self.score = 0

    # noinspection PyAttributeOutsideInit
    def init_asteroids_game_values(self):
        self.asteroids_in_this_wave: int
        self.saucer_timer = 0
        self.saucer_zigzag_timer = 0
        self.ship_timer = 0
        self.ships_remaining = 0
        self.wave_timer = u.ASTEROID_TIMER_STOPPED

    # noinspection PyAttributeOutsideInit
    def init_space_objects(self):
        self.asteroids = []
        self.missiles = []
        self.saucer = Saucer(Vector2(u.SCREEN_SIZE / 4, u.SCREEN_SIZE / 4))
        self.saucers = []
        self.saucer_missiles = []
        self.ship = Ship(pygame.Vector2(u.SCREEN_SIZE / 2, u.SCREEN_SIZE / 2))
        self.ships = []

    # noinspection PyAttributeOutsideInit
    def init_pygame_and_display(self, testing):
        if testing: return
        pygame.init()
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.game_over_pos = None
        self.game_over_surface = None
        self.help_lines = None
        self.screen = pygame.display.set_mode((u.SCREEN_SIZE, u.SCREEN_SIZE))
        self.score_font = None
        self.define_game_over()
        self.define_score()

    def process_collisions(self):
        collider = Collider(asteroids=self.asteroids, missiles=self.missiles, saucers=self.saucers, saucer_missiles=self.saucer_missiles,
                            ships=self.ships)
        self.score += collider.check_collisions()
        if not self.ships:
            self.set_ship_timer(u.SHIP_EMERGENCE_TIME)

    def check_next_wave(self, delta_time):
        if not self.asteroids:
            if self.wave_timer == u.ASTEROID_TIMER_STOPPED:
                self.wave_timer = u.ASTEROID_DELAY
            else:
                self.create_wave_in_due_time(self.asteroids, delta_time)

    def check_saucer_spawn(self, saucer, saucers, delta_time):
        if saucers: return
        self.saucer_timer -= delta_time
        self.elapsed_time += delta_time
        if self.saucer_timer <= 0:
            saucer.ready()
            saucers.append(saucer)
            self.saucer_timer = u.SAUCER_EMERGENCE_TIME

    def check_ship_spawn(self, ship, ships, delta_time):
        if ships: return
        if self.ships_remaining <= 0:
            self.game_over = True
            return
        self.ship_timer -= delta_time
        if self.ship_timer <= 0 and self.safe_to_emerge(self.missiles, self.asteroids):
            ship.reset()
            ships.append(ship)
            self.ships_remaining -= 1

    def control_ship(self, ship, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.insert_quarter(u.SHIPS_PER_QUARTER)
        if keys[pygame.K_f]:
            ship.turn_left(dt)
        if keys[pygame.K_d]:
            ship.turn_right(dt)
        if keys[pygame.K_j]:
            ship.power_on(dt)
        else:
            ship.power_off()
        if keys[pygame.K_k]:
            ship.fire_if_possible(self.missiles)
        else:
            ship.not_firing()

    def create_wave_in_due_time(self, asteroids, dt):
        self.wave_timer -= dt
        if self.wave_timer <= 0:
            asteroids.extend([Asteroid() for _ in range(0, self.next_wave_size())])
            self.wave_timer = u.ASTEROID_TIMER_STOPPED

    def define_game_over(self):
        big_font = pygame.font.SysFont("arial", 64)
        small_font = pygame.font.SysFont("arial", 48)
        self.game_over_surface = big_font.render("GAME OVER", True, "white")
        self.game_over_pos = self.game_over_surface.get_rect(centerx=u.CENTER.x, centery=u.CENTER.y / 2)
        pos_left = u.CENTER.x - 150
        pos_top = self.game_over_pos.centery
        self.help_lines = []
        messages = ["d - turn left", "f - turn right", "j - accelerate", "k - fire missile", "q - insert quarter", ]
        for message in messages:
            pos_top += 60
            text = small_font.render(message, True, "white")
            text_rect = text.get_rect(topleft=(pos_left, pos_top))
            pair = (text, text_rect)
            self.help_lines.append(pair)

    def define_score(self):
        self.score = 0
        self.score_font = pygame.font.SysFont("arial", 48)

    def draw_everything(self):
        screen = self.screen
        screen.fill("midnightblue")
        for saucer in self.saucers:
            saucer.draw(screen)
        for missile in self.saucer_missiles:
            missile.draw(screen)
        for ship in self.ships:
            ship.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        for missile in self.missiles:
            missile.draw(screen)
        self.draw_score()
        self.draw_available_ships()

    def draw_available_ships(self):
        ship = Ship(Vector2(20, 100))
        ship.angle = 90
        for i in range(0, self.ships_remaining):
            self.draw_available_ship(ship)

    def draw_available_ship(self, ship):
        ship.position += Vector2(35, 0)
        ship.draw(self.screen)

    def draw_game_over(self):
        screen = self.screen
        screen.blit(self.game_over_surface, self.game_over_pos)
        for text, pos in self.help_lines:
            screen.blit(text, pos)

    def draw_score(self):
        score_surface, score_rect = self.render_score()
        self.screen.blit(score_surface, score_rect)

    def render_score(self):
        score_text = f"0000{self.score}"[-5:]
        score_surface = self.score_font.render(score_text, True, "green")
        score_rect = score_surface.get_rect(topleft=(10, 10))
        return score_surface, score_rect

    def game_init(self):
        self.running = True
        self.saucer.init_for_new_game()
        self.insert_quarter(0)

    def insert_quarter(self, number_of_ships):
        self.asteroids = []
        self.missiles = []
        self.ships = []
        self.asteroids_in_this_wave = 2
        self.game_over = False
        self.saucer_timer = u.SAUCER_EMERGENCE_TIME
        self.score = 0
        self.ships_remaining = number_of_ships
        self.set_ship_timer(u.SHIP_EMERGENCE_TIME)
        self.wave_timer = u.ASTEROID_TIMER_STOPPED
        self.delta_time = 0

    def main_loop(self):
        self.game_init()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.check_saucer_spawn(self.saucer, self.saucers, self.delta_time)
            self.check_ship_spawn(self.ship, self.ships, self.delta_time)
            self.check_next_wave(self.delta_time)
            self.check_missile_timeout()

            self.control_ship(self.ship, self.delta_time)

            self.move_everything(self.delta_time)
            self.process_collisions()
            self.draw_everything()
            if self.game_over: self.draw_game_over()
            pygame.display.flip()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()

    def check_missile_timeout(self):
        for missile in self.missiles.copy():
            missile.update(self.missiles, self.delta_time)
        for missile in self.saucer_missiles.copy():
            missile.update(self.saucer_missiles, self.delta_time)

    def move_everything(self,dt):
        for the_saucer in self.saucers.copy():
            the_saucer.move(dt, self.saucers, self.saucer_missiles, self.ships)
        for missile in self.saucer_missiles:
            missile.move(dt)
        for the_ship in self.ships:
            the_ship.move(dt)
        for asteroid in self.asteroids:
            asteroid.move(dt)
        for missile in self.missiles:
            missile.move(dt)

    def next_wave_size(self):
        self.asteroids_in_this_wave += 2
        if self.asteroids_in_this_wave > 10:
            self.asteroids_in_this_wave = 11
        return self.asteroids_in_this_wave

    def safe_to_emerge(self, missiles, asteroids):
        if missiles: return False
        for asteroid in asteroids:
            if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
                return False
        return True

    def set_ship_timer(self, seconds):
        if self.ship_timer <= 0:
            self.ship_timer = seconds
