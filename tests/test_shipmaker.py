from pygame import Vector2

import u
from asteroid import Asteroid
from fleets import Fleets
from interactor import Interactor
from missile import Missile
from saucer import Saucer
from shipmaker import ShipMaker
from test_interactions import FI


class TestShipMaker:
    def test_exists(self):
        ShipMaker()

    def test_creates_ship(self):
        fleets = Fleets()
        fi = FI(fleets)
        fleets.add_flyer(ShipMaker())
        interactor = Interactor(fleets)
        interactor.perform_interactions()
        assert not fi.ships
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert fi.ships

    def test_unsafe_because_missile(self):
        missile = Missile(u.CENTER, Vector2(0, 0), [0, 0, 0], [0, 0, 0])
        fleets = Fleets()
        fleets.add_flyer(ShipMaker())
        interactor = Interactor(fleets)
        fi = FI(fleets)
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME - 1)
        assert not fi.ships
        fleets.add_flyer(missile)
        interactor.perform_interactions()
        fleets.tick(1)
        assert not fi.ships
        for missile in fi.missiles:
            fleets.remove_flyer(missile)
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert fi.ships

    def test_unsafe_because_saucer(self):
        fleets = Fleets()
        fleets.add_flyer(ShipMaker())
        interactor = Interactor(fleets)
        fi = FI(fleets)
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME - 1)
        assert not fi.ships
        fleets.add_flyer(Saucer())
        interactor.perform_interactions()
        fleets.tick(1)
        assert not fi.ships
        for missile in fi.missiles:
            fleets.remove_flyer(missile)
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert not fi.ships
        for saucer in fi.saucers:
            fleets.remove_flyer(saucer)
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert fi.ships

    def test_unsafe_because_asteroid(self):
        fleets = Fleets()
        fleets.add_flyer(ShipMaker())
        interactor = Interactor(fleets)
        fi = FI(fleets)
        asteroid = Asteroid()
        asteroid.move_to(u.CENTER + Vector2(u.SAFE_EMERGENCE_DISTANCE - 0.1, 0))
        asteroid._location.velocity = Vector2(0, 0)
        fleets.add_flyer(asteroid)
        assert not fi.ships
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert not fi.ships
        asteroid.move_to(u.CENTER + Vector2(u.SAFE_EMERGENCE_DISTANCE + 0.1, 0))
        interactor.perform_interactions()
        fleets.tick(0.001)
        assert fi.ships

    def test_can_run_out_of_ships(self):
        fleets = Fleets()
        fleets.add_flyer(ShipMaker())
        interactor = Interactor(fleets)
        fi = FI(fleets)
        for _ in range(4):
            interactor.perform_interactions()
            fleets.tick(u.SHIP_EMERGENCE_TIME)
            assert fi.ships
            assert not fi.game_over
            for ship in fi.ships:
                fleets.remove_flyer(ship)
        interactor.perform_interactions()
        fleets.tick(u.SHIP_EMERGENCE_TIME)
        assert not fi.ships
        assert fi.game_over
