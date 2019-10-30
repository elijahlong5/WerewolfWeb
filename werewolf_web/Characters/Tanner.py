class Tanner:

    def __init__(self, game):
        self.game = game
        self.identity = "You are the Tanner."
        self.description = "You win if you die."
        self.team = "Tanner"

    def __str__(self):
        return "Tanner"

    def jsonify_request(self, player_id):
        return {
            'role-description': self.description,
        }

    def process_player_response(self, player_id, response):
        id_sequence = f"{player_id}_Tanner"
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            if id_sequence in self.game.turn_handler.needs_to_go:
                self.game.update_game_log(id_sequence, "Tanner viewed their card")
                return {"Ay": "Ok"}
            else:
                return {"response": "Action unknown"}