# Asteroids Main program

from game import Game

asteroids_game: Game

if __name__ == "__main__":
    keep_going = True
    while keep_going:
        asteroids_game = Game()
        keep_going = asteroids_game.main_loop()
