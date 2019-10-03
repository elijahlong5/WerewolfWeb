class Villager:

    def __init__(self, game):
        self.game = game
        self.identity = "You are a villager."
        self.description = "lol"
        self.stage = None

    def __str__(self):
        return "Villager"