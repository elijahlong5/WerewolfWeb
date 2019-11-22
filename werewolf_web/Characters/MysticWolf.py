class MysticWolf:
    def __init__(self, game):
        self.game = game
        self.identity = "You are the Mystic Wolf."
        self.description = "You are on the werewolf team, and you get to view another player's card."
        self.team = "Werewolves"

        self.alters_roles = False
        self.ack_str = "MysticWolf_Ack"

    def __str__(self):
        return "Mystic Wolf"

    def jsonify_request(self, player_id):
        # player_id is an int
        # Provides dictionary of wolves, with string player IDs as well as list of names
        d = {
            'wolves': {},
            'names': {},
            'role-description': self.description,
        }
        for p_id, p in self.game.players.items():
            if (p.original_role.team == self.team and
                    str(p.original_role) != "Minion" and
                    player_id != p_id):
                d['wolves'][str(p_id)] = p.name
            elif player_id != p_id:
                d['names'][str(p_id)] = {'name': p.name}
        if not len(d['names'].keys()):
            id_sequence = f"{player_id}_{str(self)}"
            ack_sequence = f"{player_id}_{self.ack_str}"
            self.game.turn_handler.needs_to_go.append(ack_sequence)
            self.game.update_game_log(id_sequence, "There was no one eligible"
                                                   " for the Mystic Wolf to see")
        return d

    def process_player_response(self, player_id, response):
        ack_sequence = f"{player_id}_{self.ack_str}"
        id_sequence = f"{player_id}_{str(self)}"

        if 'status' in response.keys() and response['status'] == 'acknowledged':
            if ack_sequence in self.game.turn_handler.needs_to_go:
                self.game.update_game_log(ack_sequence)
                return {"Ay": "Ok"}
        elif id_sequence in self.game.turn_handler.needs_to_go:
            p_id = int(response['viewThisId'])
            p_name = self.game.players[p_id].name
            p_role = self.game.players[p_id].original_role
            response_text = f"{p_name} is a {p_role}."
            self.game.turn_handler.needs_to_go.append(ack_sequence)
            self.game.update_game_log(id_sequence, f"The Mystic Wolf viewed {p_name}'s card ({p_role}).")

            return {'response': response_text}
        else:
            return {"response": "Action unknown"}
