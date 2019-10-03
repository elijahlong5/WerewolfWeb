class Troublemaker:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Troublemaker."
        self.definition = "You switch 2 players cards."
        self.stage = None
        self.alters_roles = True

    def __str__(self):
        return "Troublemaker"

    def jsonify_request(self, player_id):
        # TODO: is this helpful.  can i have integers as keys?
        names_copy = self.game.jsonify_players_names().copy()
        d = {'names': {}}
        for key in names_copy.keys():
            d['names'][str(key)] = names_copy[key]

        d['names'].pop(str(player_id))
        # TODO: delete or reformat:
        # d = {
        #     'names': self.game.jsonify_players_names().copy()
        # }
        # remove this players name from the dict.
        # d['names'].pop(player_id)
        return d
