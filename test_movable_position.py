from pygame import Vector2

from movable_location import MovableLocation


class TestMovablePosition:
    def test_creation(self):
        position = Vector2(0, 0)
        velocity = Vector2(100, 200)
        mp = MovableLocation(position, velocity)

    def test_motion(self):
        position = Vector2(0, 0)
        velocity = Vector2(100, 200)
        mp = MovableLocation(position, velocity)
        mp.move(0.25)
        assert mp.position == Vector2(25, 50)

    def test_motion_wraps(self):
        position = Vector2(990, 990)
        velocity = Vector2(100, 200)
        mp = MovableLocation(position, velocity, 1000)
        mp.move(0.25)
        assert mp.position == Vector2(15, 40)