class Werewolf:

    def __init__(self, game):
        self.game = game
        self.identity = 'You are a Werewolf.'
        self.other_werewolves = []
        self.description = 'Dont let others find out your identity. Dont be killed at the end of the game.'
        self.stage = None

    def __str__(self):
        return "Werewolf"

    def jsonify_request(self, player_id):
        """
        This is sent to the player at the start of the game, if they are a werewolf.
        :param player_id: an int
        :return: python dict, the id is cast as a string.
        """
        d = {"lone_wolf": True,
             "fellow_wolves": {},
             }
        for p_id, p in self.game.players.items():
            if p_id == player_id:
                continue
                # TODO: Handle dreamwolf, alpha wolf etc.
            elif type(p.original_role) == type(self):
                d["fellow_wolves"][p_id] = p.name
                d["lone_wolf"] = False
        return d

    def process_player_response(self, player_id, response):
        # TODO: Append to game log who saw the card,
        middle_cards = self.game.jsonify_middle_cards()
        card_dict = {
            'requested_card': response['card'],
            'card_identity': middle_cards[response['card'].lower()]
        }
        return card_dict


