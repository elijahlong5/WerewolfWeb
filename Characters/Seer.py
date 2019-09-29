class Seer:
    def __init__(self):
        self.identity = "You are the Seer."
        self.description = "Look at 2 middle roles or 1 players role."
        self.stage = None
        self.alters_roles = False

    def __str__(self):
        return "Seer"

    def action_request(self, game_state, middle_cards, player_id):
        """Gives player a copy of whose cards are where, with which they can interact.
        :returns list[str of what card(s) they saw.]"""

        print("Please choose which card(s) you would like to see.")
        print("If you wish to see 2 of the middle cards, please enter their letters together (Ie. AB)")
        print("----------")
        starting_count = 1
        cur = starting_count

        for id, p in game_state.items():
            if p.original_role != self:
                line = f'({cur}) {p.name}'
                print(line)
                cur += 1
        line = f'(A) Middle Card A, (B) Middle Card B, (C) Middle Card C. '
        print(line)

        choice = input()

        # QUESTION: Why can't this go below the if statement?
        try:
            if choice[0] == "A":
                print("Card A is", middle_cards[0])
            elif choice[0] == "B":
                print("Card B is", middle_cards[1])
            elif choice[0] == "C":
                print("Card C is", middle_cards[2])
            if choice[1] == "A":
                print("Card A is", middle_cards[0])
            elif choice[1] == "B":
                print("Card B is", middle_cards[1])
            elif choice[1] == "C":
                print("Card C is", middle_cards[2])
            if choice[0] == "A" or choice[0] == "B":
                return [f'{p.name} saw cards {choice}']
        except:
            pass

        if 0 < int(choice) < len(game_state):
            cur = starting_count
            for id, p in game_state.items():
                if p.original_role != self:
                    if int(choice) == cur:
                        response = f'{p.name} is a {p.original_role}'
                        print(response)
                        move = f'The Seer saw that {p.name} was the {p.original_role}.'
                        if p.original_role.identity == "You are the Werewolf":
                            move += "\nGet SEERED!"
                        return [move]
                    cur += 1
