import u
from asteroid import Asteroid
from flyer import Flyer
from timer import Timer


class WaveMaker(Flyer):
    def __init__(self):
        self._need_asteroids = None
        self._timer = Timer(u.ASTEROID_DELAY, self.create_asteroids)
        self._number_to_create = 2

    def create_asteroids(self, fleets):
        self._number_to_create += 2
        if self._number_to_create > 11:
            self._number_to_create = 11
        for i in range(self._number_to_create):
            fleets.add_asteroid(Asteroid())

    def begin_interactions(self, fleets):
        self._need_asteroids = True

    def interact_with_asteroid(self, asteroid, fleets):
        self._need_asteroids = False

    def tick(self, delta_time, fleet, fleets):
        if self._need_asteroids:
            self._timer.tick(delta_time, fleets)

    def interact_with(self, other, fleets):
        other.interact_with_wavemaker(self, fleets)

    def draw(self, screen):
        pass
