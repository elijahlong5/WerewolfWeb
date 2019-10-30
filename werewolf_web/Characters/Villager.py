class Villager:

    def __init__(self, game):
        self.game = game
        self.identity = "You are a villager."
        self.description = "Good luck!"
        self.team = "Villagers"

    def __str__(self):
        return "Villager"

    def jsonify_request(self, player_id):
        return {
            'role-description': self.description,
        }

    def process_player_response(self, player_id, response):
        if 'status' in response.keys() and response['status'] == 'acknowledged':
            self.game.update_game_log(f"{player_id}_Villager", "Villager viewed their card")
            return {"Ay": "Ok"}
