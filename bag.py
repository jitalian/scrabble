import random


class TilesBag:
    def __init__(self):
        self.tiles = ["A"] * 9 + ["B"] * 2 + ["C"] * 2 + ["D"] * 4 + ["E"] * 12 + ["F"] * 2 + ["G"] * 3 + \
                     ["H"] * 2 + ["I"] * 9 + ["J"] * 1 + ["K"] * 1 + ["L"] * 4 + ["M"] * 2 + ["N"] * 6 + \
                     ["O"] * 8 + ["P"] * 2 + ["Q"] * 1 + ["R"] * 6 + ["S"] * 4 + ["T"] * 6 + ["U"] * 4 + \
                     ["V"] * 2 + ["W"] * 2 + ["X"] * 1 + ["Y"] * 2 + ["Z"] * 1 + ["*"] * 2
        # Lower case = letter from blank tile
        self.points = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2,
                       "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1,
                       "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1,
                       "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "*": 0,
                       "a": 0, "b": 0, "c": 0, "d": 0, "e": 0, "f": 0, "g": 0, "h": 0, "i": 0, "j": 0, "k": 0,
                       "l": 0, "m": 0, "n": 0, "o": 0, "p": 0, "q": 0, "r": 0, "s": 0, "t": 0, "u": 0,
                       "v": 0, "w": 0, "x": 0, "y": 0, "z": 0}

        # Short game for testing
        # self.tiles = ["A"] * 2 + ["B"] * 2 + ["D"] * 2 + ["L"] * 2 + ["N"] * 2 + ["S"] * 2 + ["*"] * 2

    def get_random_tile(self):
        if len(self.tiles) == 0:
            return None

        random_tile = random.choice(self.tiles)
        self.tiles.remove(random_tile)

        return random_tile

    def get_tile_points(self, tile):
        return self.points[tile]

    def get_tiles_remaining(self):
        return len(self.tiles)
