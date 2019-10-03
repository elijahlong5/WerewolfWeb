class Insomniac:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Insomniac."
        self.description = "You learn the identity of your card before the discussion begins. Play this role."
        self.stage = None

    def __str__(self):
        return "Insomniac"

    def action_request(self, game_state, middle_cards, player_id):
        print(f'You are the {game_state.get(player_id).current_role}')
        return['Insomniac notified']
