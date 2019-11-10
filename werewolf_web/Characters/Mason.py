class Mason:
    def __init__(self, game):
        self.game = game
        self.identity = "You are a Mason."
        self.description = "You are on the villager team."
        self.team = "Villagers"

    def __str__(self):
        return "Mason"

    def jsonify_request(self, player_id):
        # Provides dictionary of masons, with string player IDs
        d = {
            'masons': {},
            'role-description': self.description,
        }
        temp_mason = Mason(self.game)
        for p_id, p in self.game.players.items():
            if type(p.original_role) == type(temp_mason) and p_id != player_id:
                d['masons'][str(p_id)] = p.name
        return d

    def process_player_response(self, player_id, player_response):
        """When the Mason acknowledges they've seen the other masons."""
        id_sequence = f"{player_id}_Mason"
        if id_sequence in self.game.turn_handler.needs_to_go:
            self.game.update_game_log(id_sequence, f"The mason viewed the other masons.")
            return {"Ay": "Ok"}
        else:
            return {"Ay": "Already updated game log"}