class Spectator:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Spectating the game."
        self.description = "View the madness"
        self.team = "Villagers"

    def __str__(self):
        return "Spectator"

    def jsonify_request(self, player_id=None):
        return

