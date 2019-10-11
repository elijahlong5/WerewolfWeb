class Villager:

    def __init__(self, game):
        self.game = game
        self.identity = "You are a villager."
        self.description = "lol"
        self.stage = None

    def __str__(self):
        return "Villager"

    def jsonify_request(self, player_id):
        # TODO: The villager acknowledged their villagerness
        return {"villager": "no info to show"}
