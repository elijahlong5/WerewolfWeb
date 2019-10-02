class Human:
    def __init__(self, name, player_id):
        self.original_role = None
        self.current_role = None
        # TODO:
        # self.win_count = 0
        # self.correct_votes = 0
        self.name = name
        self.player_id = player_id

        self.active_player = True

    def assign_initial_role(self, role):
        self.original_role = role
        self.current_role = self.original_role

    def get_dict(self, game):
        if self.original_role:
            return self.original_role.jsonify_request(game, self.player_id)

    def process_player_response(self):
        print('getting response from human class')
        return {'hey': 1}
        # return self.original_role.process_player_response(game, self.player_id, response)
