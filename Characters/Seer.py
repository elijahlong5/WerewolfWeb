class Seer:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Seer."
        self.description = "Look at 2 middle roles or 1 players role."
        self.stage = None
        self.alters_roles = False

    def __str__(self):
        return "Seer"

    def jsonify_request(self, player_id):
        names_copy = self.game.jsonify_players_names().copy()
        d = {'names': {}}
        for key in names_copy.keys():
            d['names'][str(key)] = names_copy[key]

        d['names'].pop(str(player_id))
        return d