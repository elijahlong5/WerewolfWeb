class Robber:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Robber."
        self.description = "Choose someone to rob. Their identity is switched with yours. " \
                           " Now you are the role of this new card."
        self.team = "Villagers"

        self.alters_roles = True
        self.ack_str = "Robber Ack"

    def __str__(self):
        return "Robber"

    def jsonify_request(self, player_id):
        d = self.game.jsonify_players_names().copy()
        d['names'].pop(str(player_id))
        d['role-description'] = self.description
        return d

    def process_player_response(self, player_id, response):
        ack_sequence = f"{player_id}_{self.ack_str}"
        id_sequence = f"{player_id}_Robber"

        print(response)
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            if ack_sequence in self.game.turn_handler.needs_to_go:
                self.game.update_game_log(ack_sequence)
                return {"Ay": "Ok"}
        elif id_sequence in self.game.turn_handler.needs_to_go:
            p1_id = player_id
            p2_id = int(response['robThisId'])
            p2_role = self.game.players[p2_id].original_role
            response_text = f"You are now the {p2_role}"

            self.game.update_move(id_sequence, self.game.swap_roles, p1_id, p2_id)
            rob_victim = self.game.players[p2_id].name

            self.game.turn_handler.needs_to_go.append(ack_sequence)
            self.game.update_game_log(id_sequence, f"The robber robbed {rob_victim} ({p2_role})")

            return {'response': response_text}
        else:
            return {"response": "Action unknown"}
