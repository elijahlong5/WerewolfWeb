import abc

# import Game.Role as Role


class Werewolf(abc.ABC):

    def __init__(self):
        self.identity = 'You are a Werewolf.'
        self.other_werewolves = []
        self.description = 'Dont let others find out your identity. Dont be killed at the end of the game.'
        self.stage = None

    def __str__(self):
        return "Werewolf"

    def jsonify_request(self, game, player_id):
        d = {'lone_wolf': True,
             'fellow_wolves': {},
             }

        for p_id, p in game.players.items():
            print(f'{p.name}, is a {p.original_role}')
            if p_id == player_id:
                continue
                # TODO: Handle dreamwolf, alpha wolf etc.
            elif type(p.original_role) == type(self):
                d['fellow_wolves'][p_id] = p.name
                d['lone_wolf'] = False
        return d

    def process_player_response(self, game, player_id, response):
        return {
            'response': 'hello',
            'id': player_id,
            'clicked_was': response,
        }

