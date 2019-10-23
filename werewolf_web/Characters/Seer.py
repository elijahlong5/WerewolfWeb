class Seer:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Seer."
        self.description = "Look at 2 middle roles or 1 players role."
        self.team = "Villagers"

        self.alters_roles = False
        self.ack_str = "Seer ack"

    def __str__(self):
        return "Seer"

    def jsonify_request(self, player_id):
        d = self.game.jsonify_players_names().copy()
        d['names'].pop(str(player_id))
        return d

    def process_player_response(self, player_id, response):
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            if self.ack_str in self.game.turn_handler.needs_to_go:
                self.game.update_game_log(self.ack_str)
                return {"Ay": "Ok"}
        card_identities = {}
        game_log_update = "The Seer viewed"
        try:
            p = self.game.players[int(response["player_id"])]
            card_identities["player_id"] = str(p.original_role)
            card_str = f"{p.name}'s card is the {p.original_role}"
            game_log_update += f"{p.name}'s card (is the ){p.original_role})"
        except KeyError:
            middle_cards = self.game.jsonify_middle_cards()
            c1 = response['middle_card_1']
            c2 = response['middle_card_2']
            c1_value = middle_cards[c1.lower()]
            c2_value = middle_cards[c2.lower()]
            card_str = f"The {c1} card is {c1_value}, and the {c2} card is the {c2_value}"
            game_log_update += f"the {c1} card ({c1_value}), and the {c2} card ({c2_value})."
            card_identities["middle_card_1"] = middle_cards[response['middle_card_2'].lower()]
            card_identities["middle_card_2"] = middle_cards[response["middle_card_2"].lower()]

        self.game.turn_handler.needs_to_go.append(self.ack_str)
        self.game.update_game_log("Seer", card_str)
        return {"response": card_str}
