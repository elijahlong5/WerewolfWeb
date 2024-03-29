class Insomniac:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Insomniac."
        self.description = "You learn the identity of your card before the discussion begins."
        self.team = "Villagers"

    def __str__(self):
        return "Insomniac"

    def jsonify_request(self, player_id):
        d = {'current_role': str(self.game.players[player_id].current_role),
             'role-description': self.description,
             'ready': (f"{player_id}_Insomniac" in self.game.turn_handler.needs_to_go)}
        return d

    def process_player_response(self, player_id, player_response):
        """When the insomniac acknowledges that they have seen their card."""
        if f"{player_id}_Insomniac" in self.game.turn_handler.needs_to_go:
            self.game.update_game_log(f"{player_id}_Insomniac", "The insomniac viewed their card")
            return {"Ay": "Ok"}
        else:
            return {"Ay": "Already updated game log"}
