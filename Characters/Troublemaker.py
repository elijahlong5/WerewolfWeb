class Troublemaker:
    def __init__(self):
        self.identity = "You are the Troublemaker."
        self.definition = "You switch 2 players cards."
        self.stage = None
        self.alters_roles = True

    def __str__(self):
        return "Troublemaker"

    def action_request(self, game_state, middle_cards, player_id):
        """Gives player a copy of whose cards are where, with which they can interact.
        :returns list[str of what card(s) they saw.]"""

        print("Please choose which 2 player's card you would like to switch.")
        print('Enter them in together ie (12 or 35)')
        print("----------")
        starting_count = 1
        cur = starting_count

        for id, p in game_state.items():
            if p.original_role != self:
                line = f'({cur}) {p.name}'
                print(line)
                cur += 1

        choice = input()

        if 0 < int(choice[0]) < len(game_state) and 0 < int(choice[1]) < len(game_state):
            cur = starting_count
            for id, p in game_state.items():
                if p.original_role != self:
                    if int(choice[0]) == cur:
                        p1_id = id
                    elif int(choice[1]) == cur:
                        p2_id = id
                    cur += 1
            move = f'{game_state.get(player_id).name} switched'
            f'{game_state.get(p1_id).name} and '
            f'{game_state.get(p2_id).name}s cards'
            return [move, p1_id, p2_id]