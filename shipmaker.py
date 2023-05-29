import u
from flyer import Flyer
from ship import Ship
from timer import Timer


class ShipMaker(Flyer):
    def __init__(self):
        self._timer = Timer(u.SHIP_EMERGENCE_TIME, self.create_ship)
        self._need_ship = True
        self._safe_to_emerge = False

    def begin_interactions(self, fleets):
        self._need_ship = True
        self._safe_to_emerge = True

    def interact_with_saucer(self, saucer, fleets):
        self._safe_to_emerge = False

    def interact_with_ship(self, ship, fleets):
        self._need_ship = False

    def interact_with_missile(self, missile, fleets):
        self._safe_to_emerge = False

    def interact_with_asteroid(self, asteroid, fleets):
        if asteroid.position.distance_to(u.CENTER) < u.SAFE_EMERGENCE_DISTANCE:
            self._safe_to_emerge = False

    def tick(self, delta_time, fleet, fleets):
        if self._need_ship:
            self._timer.tick(delta_time, fleets)

    def create_ship(self, fleets):
        if not self._safe_to_emerge:
            return False
        if fleets.ships_remaining > 0:
            fleets.ships_remaining -= 1
            fleets.add_ship(Ship(u.CENTER))
        else:
            fleets.game_over = True
        return True

    def interact_with(self, other, fleets):
        pass

    def draw(self, screen):
        pass