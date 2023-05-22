from flyer import Flyer


class ScoreKeeper(Flyer):
    def __init__(self):
        self.score = 0

    def are_we_colliding(self, position, radius):
        return False

    def draw(self, screen):
        pass

    def interact_with(self, other, fleets):
        other.interact_with_scorekeeper(self, fleets)

    def interact_with_score(self, score, fleets):
        self.score += score.score

    def tick(self, delta_time, _fleet, _fleets):
        pass
