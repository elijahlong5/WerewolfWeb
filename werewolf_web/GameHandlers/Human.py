class Human:
    def __init__(self, name, player_id):
        self.original_role = None
        self.current_role = None
        # self.win_count = 0
        # self.correct_votes = 0
        self.name = name
        self.player_id = player_id

        self.votes_against = 0
        self.voted_for = None

        self.active_player = True

    def get_json_dict(self):
        vf = None
        if self.voted_for is not None:
            vf = self.voted_for.player_id
        return {
            'original_role': str(self.original_role),
            'current_role': str(self.current_role),
            'name': self.name,
            'votes_for': self.votes_against,
            'voted_for_id': vf,
        }

    def assign_initial_role(self, role):
        self.original_role = role
        self.current_role = self.original_role

        # Reset end of game stats.
        self.votes_against = 0
        self.voted_for = None

    def get_role_initial_dict(self):
        if self.original_role:
            return self.original_role.jsonify_request(self.player_id)
