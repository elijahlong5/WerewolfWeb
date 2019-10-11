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
        d = self.game.jsonify_players_names().copy()
        d['names'].pop(str(player_id))
        return d

    def process_player_response(self, player_id, player_response):
        p1_id = player_id
        p2_id = int(player_response['robThisId'])
        p2_role = self.game.players[p2_id].original_role
        response_text = f"You are now the {p2_role}"
        self.game.update_move("Robber", self.game.swap_roles, p1_id, p2_id)
        return {'response': response_text}