class Tanner:

    def __init__(self, game):
        self.game = game
        self.identity = "You are the Tanner."
        self.description = "lol"
        self.team = "Tanner"

    def __str__(self):
        return "Tanner"

    def jsonify_request(self, player_id):
        return {"Tanner": "You win if you die"}

    def process_player_response(self, player_id, response):
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            self.game.update_game_log("Tanner", "Tanner viewed their card")
            return {"Ay": "Ok"}
