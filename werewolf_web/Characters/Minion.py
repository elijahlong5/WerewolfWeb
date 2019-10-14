import Characters.Werewolf as W

class Minion:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Minion."
        self.description = "Help the werewolves. If they die, you lose"
        self.stage = None

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
        self.game.update_game_log("Minion", f"The minion viewed the werewolves.")
        return d
