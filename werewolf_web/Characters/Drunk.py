class Drunk:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Drunk."
        self.description = "You switch your card with one of the center cards."
        self.team = "Villagers"
        self.alters_roles = True
        self.ack_str = "Drunk_Ack"

    def __str__(self):
        return "Drunk"

    def jsonify_request(self, player_id):
        return {
            "role-description": self.description,
        }

    def process_player_response(self, player_id, player_response):
        """
        Swap the card in the middle with the drunk's card.
        """
        ack_sequence = f"{player_id}_{self.ack_str}"
        id_sequence = f"{player_id}_Drunk"

        if "card" in player_response.keys() and id_sequence in self.game.turn_handler.needs_to_go:
            card = player_response["card"]
            p_id = player_id
            game_log_text = f"The drunk switched their card with the {card} card"
            response_text = f"You've switched your card with the {card} card."
            self.game.turn_handler.needs_to_go.append(ack_sequence)
            self.game.update_move(id_sequence, self.game.swap_role_with_mid, card, p_id)
            self.game.update_game_log(id_sequence, game_log_text)
            return {'response': response_text}
        elif "status" in player_response.keys():
            self.game.update_game_log(ack_sequence)
            return {'Ay': "response received"}
        else:
            return {"response": "Action unknown"}

