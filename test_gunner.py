from pygame import Vector2

import u
from fleets import Fleets
from gunner import Gunner
from test_interactions import FI


class TestGunner:
    def test_exists(self):
        assert Gunner()

    def test_no_fire(self):
        delta_time = 0.1
        saucer_position = Vector2(0, 0 )
        ship_position = Vector2(1, 1)
        fleets = Fleets()
        Gunner().fire(delta_time, saucer_position, Vector2(0, 0), ship_position, fleets)
        assert not FI(fleets).saucer_missiles

    def test_fire(self):
        delta_time = u.SAUCER_MISSILE_DELAY
        saucer_position = Vector2(0, 0 )
        ship_position = Vector2(1, 1)
        fleets = Fleets()
        Gunner().fire(delta_time, saucer_position, Vector2(0, 0), ship_position, fleets)
        assert FI(fleets).saucer_missiles

    def test_random_missile(self):
        no_target = 0.5
        angle = 0.0
        fleets = Fleets()
        fi = FI(fleets)
        position = Vector2(500, 500)
        Gunner().create_missile(no_target, angle, position, Vector2(12, 34), None, fleets)
        assert fi.saucer_missiles
        missile = fi.saucer_missiles[0]
        assert missile.position == position + Vector2(40, 0)
        assert missile.velocity_testing_only == Vector2(u.MISSILE_SPEED + 12, 34)
