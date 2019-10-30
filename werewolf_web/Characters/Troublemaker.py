class Troublemaker:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Troublemaker."
        self.description = "You switch 2 players cards. You do not get to see these cards."
        self.team = "Villagers"
        self.alters_roles = True

    def __str__(self):
        return "Troublemaker"

    def jsonify_request(self, player_id):
        d = self.game.jsonify_players_names().copy()
        d['names'].pop(str(player_id))
        d['role-description'] = self.description
        return d

    def process_player_response(self, player_id, player_response):
        id_sequence = f"{player_id}_Troublemaker"

        if id_sequence in self.game.turn_handler.needs_to_go:
            p1_id = int(player_response['playerId_1'])
            p2_id = int(player_response['playerId_2'])
            p1_name = self.game.players[p1_id].name
            p2_name = self.game.players[p2_id].name
            response_text = f"The troublemaker switched {p1_name} and {p2_name}'s cards."

            self.game.update_move(id_sequence, self.game.swap_roles, p1_id, p2_id)
            self.game.update_game_log(id_sequence, response_text)
            return {'response': response_text}
        else:
            return {"response": "Action unknown"}
