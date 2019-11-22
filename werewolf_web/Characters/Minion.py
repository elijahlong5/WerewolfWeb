import Characters.MysticWolf as M
import Characters.Werewolf as W


class Minion:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Minion."
        self.description = "Help the werewolves win."
        self.team = "Werewolves"

    def __str__(self):
        return "Minion"

    def jsonify_request(self, player_id):
        # Provides dictionary of wolves, with string player IDs
        d = {
             'wolves': {},
             'role-description': self.description,
             }
        for p_id, p in self.game.players.items():
            if (p.original_role.team == self.team and
                    str(p.original_role) != "Minion"):
                d['wolves'][str(p_id)] = p.name
        return d

    def process_player_response(self, player_id, player_response):
        """When the minion acknowledges that they have seen their card."""
        id_sequence = f"{player_id}_Minion"
        if id_sequence in self.game.turn_handler.needs_to_go:
            self.game.update_game_log(id_sequence, f"The minion viewed the werewolves.")
            return {"Ay": "Ok"}
        else:
            return {"Ay": "Already updated game log"}