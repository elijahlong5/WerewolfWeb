import Characters.Werewolf as W

class Minion:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Minion."
        self.description = "Help the werewolves. If they die, you lose"
        self.stage = None
        self.team = "Werewolves"

    def __str__(self):
        return "Minion"

    def jsonify_request(self, player_id):
        # Provides dictionary of wolves, with string player IDs
        d = {
             'wolves': {},
             }
        temp_wolf = W.Werewolf(self.game)
        for p_id, p in self.game.players.items():
            if type(p.original_role) == type(temp_wolf):
                d['wolves'][str(p_id)] = p.name
        return d

    def process_player_response(self, player_id, player_response):
        """When the minion acknowledges that they have seen their card."""
        if "Minion" in self.game.turn_handler.needs_to_go:
            self.game.update_game_log("Minion", f"The minion viewed the werewolves.")
            return {"Ay": "Ok"}
        else:
            return {"Ay": "Already updated game log"}