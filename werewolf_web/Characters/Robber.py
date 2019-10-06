class Robber:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Robber."
        self.description = "Choose someone to rob. Their identity is switched with yours. " \
                           " Now you are the role of this new card."
        self.stage = None
        self.alters_roles = True

    def __str__(self):
        return "Robber"

    def jsonify_request(self, player_id):
        names_copy = self.game.jsonify_players_names().copy()
        d = {'names': {}}
        for key in names_copy.keys():
            d['names'][str(key)] = names_copy[key]

        d['names'].pop(str(player_id))
        return d
