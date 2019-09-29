class Minion:
    def __init__(self):
        self.identity = "You are the Minion."
        self.description = "Help the werewolves. If they die, you lose"
        self.stage = None

    def __str__(self):
        return "Minion"

    def action_request(self, game_state, middle_cards, player_id):
        """Display who the werewolves are."""

        for id, p in game_state.items():
            if p.original_role.identity == 'You are a Werewolf.':
                print(f'{p.name} is a werewolf!')
        return ['Minion identification']