class Spectator:
    def __init__(self):
        self.identity = "You are the Spectating the game."
        self.description = "View the madness"
        self.stage = None

    def __str__(self):
        return "Spectator"

    def action_request(self, game_state, middle_cards, player_id):
        return
