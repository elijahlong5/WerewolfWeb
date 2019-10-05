class Seer:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Seer."
        self.description = "Look at 2 middle roles or 1 players role."
        self.stage = None
        self.alters_roles = False

    def __str__(self):
        return "Seer"

    def jsonify_request(self, player_id):
        names_copy = self.game.jsonify_players_names().copy()
        d = {'names': {}}
        for key in names_copy.keys():
            d['names'][str(key)] = names_copy[key]

        d['names'].pop(str(player_id))
        return d

    def process_player_response(self, player_id, response):
        # TODO: Append to game log who saw the card,
        card_identities = {}
        try:
            print(f'player id is {response["player_id"]}')
            p = self.game.players[int(response["player_id"])]
            card_identities["player_id"] = str(p.original_role)
        except KeyError:
            middle_cards = self.game.jsonify_middle_cards()

            card_identities["middle_card_1"] = middle_cards[response["middle_card_1"].lower()]
            card_identities["middle_card_2"] = middle_cards[response["middle_card_2"].lower()]

        return card_identities
