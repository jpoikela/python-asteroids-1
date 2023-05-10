from pygame import Vector2

import u
from asteroid import Asteroid
from fleets import Fleets
from fleet import Fleet, AsteroidFleet, ShipFleet, MissileFleet, ExplosionFleet
from missile import Missile


class FakeFlyer:
    def __init__(self):
        pass

    def control_motion(self, delta_time):
        pass

    def fire_if_possible(self, _delta_time, _saucer_missiles, _ships):
        pass

    def move(self, delta_time, fleet):
        pass

    @staticmethod
    def tick(_delta_time, _fleet, _fleets):
        return True


class TestFleets:
    def test_creation(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        assert fleets

    def test_access(self):
        asteroids = ["asteroid"]
        missiles = ["missile"]
        saucers = ["saucer"]
        saucer_missiles = ["saucer_missile"]
        ships = ["ship"]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        assert fleets.asteroids.flyers == asteroids
        assert fleets.missiles.flyers == missiles
        assert fleets.saucers.flyers == saucers
        assert fleets.saucer_missiles.flyers == saucer_missiles
        assert fleets.ships.flyers == ships

    def test_fleet_creation(self):
        asteroids = ["asteroid"]
        fleet = Fleet(asteroids)
        assert fleet

    def test_fleets_tick(self):
        asteroids = [FakeFlyer()]
        missiles = [FakeFlyer()]
        saucers = [FakeFlyer()]
        saucer_missiles = [FakeFlyer()]
        ships = [FakeFlyer()]
        fleets = Fleets(asteroids, missiles, saucers, saucer_missiles, ships)
        result = fleets.tick(0.1)
        assert result

    def test_saucer_spawn(self):
        saucers = []
        fleets = Fleets([], [], saucers, [], [])
        saucer_fleet = fleets.saucers
        saucer_fleet.tick(0.1, fleets)
        assert not saucers
        saucer_fleet.tick(u.SAUCER_EMERGENCE_TIME, fleets)
        assert saucers

    def test_len_etc(self):
        saucer_missiles = []
        fleets = Fleets([], [], [], saucer_missiles, [])
        s_m_fleet = fleets.saucer_missiles
        assert len(s_m_fleet) == 0
        s_m_fleet.extend([1, 20, 300])
        assert len(s_m_fleet) == 3
        assert s_m_fleet[1] == 20

    def test_asteroid_fleet_exists(self):
        asteroids = []
        _fleet = AsteroidFleet(asteroids)

    def test_asteroid_wave(self):
        asteroids = []
        fleets = Fleets(asteroids, [], [], [], [])
        asteroid_fleet = fleets.asteroids
        assert isinstance(asteroid_fleet, AsteroidFleet)
        asteroid_fleet.tick(0.1, fleets)
        assert not asteroids
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 4
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 6
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 8
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 10
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 11
        asteroid_fleet.clear()
        asteroid_fleet.tick(u.ASTEROID_DELAY, fleets)
        assert len(asteroids) == 11

    def test_ship_rez(self):
        ShipFleet.rez_from_fleet = True
        ships = []
        fleets = Fleets([], [], [], [], ships)
        ship_fleet = fleets.ships
        assert not ships
        ship_fleet.tick(0.1, fleets)
        assert not ships
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert ships

    def test_unsafe_because_missile(self):
        ShipFleet.rez_from_fleet = True
        ships = []
        missile = Missile(u.CENTER, Vector2(0,0), [0,0,0], [0,0,0])
        missiles = [missile]
        fleets = Fleets([], missiles, [], [], ships)
        ship_fleet = fleets.ships
        assert not ships
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert not ships
        missiles.clear()
        ship_fleet.tick(0.001, fleets)
        assert ships

    def test_unsafe_because_saucer_missile(self):
        ships = []
        missile = Missile(u.CENTER, Vector2(0,0), [0,0,0], [0,0,0])
        saucer_missiles = [missile]
        fleets = Fleets([], [], [], saucer_missiles, ships)
        ship_fleet = fleets.ships
        assert not ships
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert not ships
        saucer_missiles.clear()
        ship_fleet.tick(0.001, fleets)
        assert ships

    def test_unsafe_because_asteroid(self):
        ShipFleet.rez_from_fleet = True
        ships = []
        asteroid = Asteroid()
        asteroid.position = u.CENTER + Vector2(u.SAFE_EMERGENCE_DISTANCE - 0.1, 0)
        asteroids = [asteroid]
        fleets = Fleets(asteroids, [], [], [], ships)
        ship_fleet = fleets.ships
        assert not ships
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert not ships
        asteroids.clear()
        ship_fleet.tick(0.001, fleets)
        assert ships

    def test_can_run_out_of_ships(self):
        ShipFleet.rez_from_fleet = True
        ships = []
        fleets = Fleets([], [], [], [], ships)
        ship_fleet = fleets.ships
        ShipFleet.ships_remaining = 2
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert ships
        assert ship_fleet.ships_remaining == 1
        ships.clear()
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert ships
        assert ship_fleet.ships_remaining == 0
        assert not ship_fleet.game_over
        ships.clear()
        ship_fleet.tick(u.SHIP_EMERGENCE_TIME, fleets)
        assert not ships
        assert ship_fleet.game_over

    def test_missile_fleet(self):
        missiles = []
        fleet = MissileFleet(missiles, 3)
        fired = fleet.fire(lambda:  666 )
        assert fired
        assert len(missiles) == 1
        assert missiles[-1] == 666

        fired = fleet.fire(lambda:  777 )
        assert fired
        assert len(missiles) == 2
        assert missiles[-1] == 777

        fired = fleet.fire(lambda:  888 )
        assert fired
        assert len(missiles) == 3
        assert missiles[-1] == 888

        fired = fleet.fire(lambda:  999 )
        assert not fired
        assert len(missiles) == 3

    def test_missile_fleet_parameter(self):
        missiles = []
        fleet = MissileFleet(missiles, 2)
        fired = fleet.fire(lambda m: m*2, 333)
        assert fired
        assert len(missiles) == 1
        assert missiles[-1] == 666

    def test_explosion_fleet(self):
        fleet = ExplosionFleet()
        explosion = fleet.flyers
        fleet.explosion_at(u.CENTER)
        assert explosion





