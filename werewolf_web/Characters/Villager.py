class Villager:

    def __init__(self, game):
        self.game = game
        self.identity = "You are a villager."
        self.description = "lol"
        self.stage = None
        self.team = "Villagers"

    def __str__(self):
        return "Villager"

    def jsonify_request(self, player_id):
        return {"villager": "no info to show"}

    def process_player_response(self, player_id, response):
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            self.game.update_game_log("Villager", "Villager viewed their card")
            return {"Ay": "Ok"}
