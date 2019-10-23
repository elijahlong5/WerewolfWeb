class Werewolf:

    def __init__(self, game):
        self.game = game
        self.identity = 'You are a Werewolf.'
        self.description = 'Dont let others find out your identity. Dont be killed at the end of the game.'
        self.ack_str = "Lone Werewolf"
        self.team = "Werewolves"

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
            elif type(p.original_role) == type(self):
                d["fellow_wolves"][p_id] = p.name
                d["lone_wolf"] = False
        return d

    def process_player_response(self, player_id, response):

        # Case 1: werewolf acknowledges they are a werewolf.
        print(response)
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            if self.ack_str in self.game.turn_handler.needs_to_go:
                print('response acknowledged, and removed from list')
                self.game.update_game_log(self.ack_str)
            else:
                self.game.update_game_log("Werewolf", f"Werewolves saw the other werewolves.")
            return {'Ay': "response received"}
        # Case 2: werewolf is choosing a card
        else:
            middle_cards = self.game.jsonify_middle_cards()
            card_dict = {
                'requested_card': response['card'],
                'card_identity': middle_cards[response['card'].lower()]
            }
            # Add the card acknowledge to 'needs_to_go' list
            self.game.turn_handler.needs_to_go.append(self.ack_str)
            # Append to game log what card they viewed
            self.game.update_game_log("Werewolf", f"The werewolf viewed the {response['card']} card which"
                                      f" was the {card_dict['card_identity']}")

            return card_dict


