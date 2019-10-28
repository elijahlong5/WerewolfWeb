class Witch:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Witch."
        self.description = "You view one card in the middle and switch it with someone else's card."
        self.team = "Villagers"
        self.alters_roles = True
        self.ack_str = "Witch Ack"

        self.middle_card = None

    def __str__(self):
        return "Witch"

    def jsonify_request(self, player_id):
        d = self.game.jsonify_players_names().copy()
        d['names'].pop(str(player_id))
        d['role-description'] = self.description
        return d

    def process_player_response(self, player_id, player_response):
        """
        Multi part function.
        if card is in the player response then kick it back to the client.
        if player id is in the response then kick it to the game object and do the move.
        :param player_id:
        :param player_response:
        :return:
        """
        if "card" in player_response.keys():
            self.middle_card = player_response['card']  # Will be 'left right or middle'
            card_info = {
                'requested_card': self.middle_card,
                'card_identity': self.game.jsonify_middle_cards()[self.middle_card.lower()]
            }
            return card_info
        elif "playerId" in player_response.keys():
            p_id = int(player_response['playerId'])
            print(f'mid card is {self.middle_card}')

            p_name = self.game.players[p_id].name
            game_log = f"The witch switched the {self.middle_card} with {p_name}'s card."
            response_text = f"You've switched the {self.middle_card} with {p_name}'s card."
            self.game.turn_handler.needs_to_go.append(self.ack_str)
            self.game.update_move("Witch", self.game.swap_role_with_mid, self.middle_card, p_id)
            self.game.update_game_log("Witch", game_log)
            return {'response': response_text}
        elif "status" in player_response.keys():
            self.game.update_game_log(self.ack_str)
            return {'Ay': "response received"}
