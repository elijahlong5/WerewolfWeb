class Insomniac:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Insomniac."
        self.description = "You learn the identity of your card before the discussion begins. Play this role."
        self.stage = None

    def __str__(self):
        return "Insomniac"

    def jsonify_request(self, player_id):
        if self.game.turn_handler.whose_turn() == "Insomniac":
            return {'current_role': str(self.game.players[player_id].current_role),
                    'ready': True}
        else:
            return {"ready": False}

    def process_player_response(self, player_id, player_response):
        """When the insomniac acknowledges that they have seen their card."""
        if "Insomniac" in self.game.turn_handler.needs_to_go:
            self.game.update_game_log("Insomniac", "The insomniac viewed their card")
            return {"Ay": "Ok"}
        else:
            return {"Ay": "Already updated game log"}
