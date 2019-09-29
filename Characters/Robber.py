class Robber:
    def __init__(self):
        self.identity = "You are the Robber."
        self.description = "Choose someone to rob. Their identity is switched with yours. " \
                           " Now you are the role of this new card."
        self.stage = None
        self.alters_roles = True

    def __str__(self):
        return "Robber"

    def action_request(self, game_state, middle_cards, player_id):
        """Gives player a copy of whose cards are where, with which they can interact.
        :returns list[ the move they made, their id, the id of the person they robbed."""

        print("Please choose which person you would like to ROB.")
        print("-------------")
        starting_count = 1
        cur = starting_count

        for id, p in game_state.items():
            if p.original_role != self:
                line = f'({cur}) {p.name}'
                print(line)
                cur += 1

        choice = input()

        if 0 < int(choice) < len(game_state):
            cur = starting_count
            for id, p in game_state.items():
                if int(choice) == cur:
                    # tell them their
                    response = f'You are now the {p.original_role}'
                    print(response)
                    move = f'The Robber robbed {p.name}, who was the {p.original_role}.'
                    if p.original_role.identity == "You are the Werewolf":
                        move += "\nYikes!"
                    return [move, player_id, id]
                cur += 1
