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
        d = self.game.jsonify_players_names().copy()
        d['names'].pop(str(player_id))
        return d

    def process_player_response(self, player_id, player_response):
        p1_id = int(player_response['playerId_1'])
        p2_id = int(player_response['playerId_2'])
        p1_name = self.game.players[p1_id].name
        p2_name = self.game.players[p2_id].name
        response_text = f"The troublemaker is switching {p1_name} and {p2_name}'s cards."

        self.game.update_move("Troublemaker", self.game.swap_roles, p1_id, p2_id)
        self.game.update_game("Troublemaker", response_text)
        return {'response': response_text}
