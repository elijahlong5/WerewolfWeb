import abc


class Werewolf(abc.ABC):

    def __init__(self):
        self.identity = 'You are a Werewolf.'
        self.other_werewolves = []
        self.description = 'Dont let others find out your identity. Dont be killed at the end of the game.'
        self.stage = None

    def __str__(self):
        return "Werewolf"

    def jsonify_request(self, game_state, player_id):
        return game_state['middle_cards']


    def action_request(self, game_state, middle_cards, player_id):
        """Display who the other werewolf is. If the otherwerewolf is in the middle,
        then the werewolf can choose to see a card."""

        for id, p in game_state.items():
            if id == player_id:
                continue
            elif p.original_role.identity == 'You are a Werewolf.':
                print(f'{p.name} is a WEREWOLF!')
                return ['Werewolf identification']
        print('Looks like youre the only Werewolf. Select 1 card from the middle you would like to see.')

        print(f'(A) Middle Card A, (B) Middle Card B, (C) Middle Card C. ')
        choice = input()
        viewed_card = ''
        try:
            if choice[0] == "A":
                viewed_card = middle_cards[0]
                print("Card A is", middle_cards[0])
            elif choice[0] == "B":
                viewed_card = middle_cards[1]
                print("Card B is", middle_cards[1])
            elif choice[0] == "C":
                viewed_card = middle_cards[2]
                print("Card C is", middle_cards[2])
        except:
            print('invalid input')
        return [f'{game_state.get(player_id).name} saw the {viewed_card} in the middle.5555']
