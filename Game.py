from enum import Enum

import GameHandlers.Human as Human

import Characters.Insomniac as I
import Characters.Minion as M
import Characters.Robber as R
import Characters.Seer as S
import Characters.Troublemaker as T
import Characters.Werewolf as W
import Characters.Villager as V

import Characters.Spectator as Sp


import random


class Role(Enum):
    INSOMNIAC = 'Insomniac'
    MINION = str(M.Minion())
    ROBBER = str(R.Robber())
    SEER = str(S.Seer())
    TROUBLEMAKER = 'Troublemaker'
    WEREWOLF = "Werewolf"
    VILLAGER = str(V.Villager())

    SPECTATOR = str(Sp.Spectator())


class WerewolfGame:

    def __init__(self):
        self.GAME_ON = False
        self.game_stage = 0
        self.characters = []
        self.players = {}
        self.middle_cards = [0, 1, 2]
        self.game_tracker = []
        self.discussion_stage = 0
        # improve this ^ and bad stage tracker method

        # Add the characters to the game
        # TODO: make this doable by the game host

        self.characters.append(I.Insomniac())
        self.characters.append(M.Minion())
        self.characters.append(R.Robber())

        self.characters.append(S.Seer())
        self.characters.append(T.Troublemaker(self))
        self.characters.append(W.Werewolf(self))
        self.characters.append(W.Werewolf(self))

        self.characters.append(W.Werewolf(self))
        self.characters.append(V.Villager())
        self.characters.append(V.Villager())

        self.characters.append(Sp.Spectator())

    def jsonify_full_game_state(self):
        """
        :return: The game state in dictionary format for use within the json structure. Game state will be passed
        across the different players.
        """
        game_state = {
            'game_info': {
                'is_game_on': self.GAME_ON,
                'stage': self.game_stage,
            },
            'players': self.jsonify_players(),
            'middle_cards': self.jsonify_middle_cards(),
        }
        return game_state

    def jsonify_players(self):
        p_conversion = {}
        for p_id, player in self.players.items():
            p_conversion[p_id] = {
                'name': player.name,
                'original_role': player.original_role,
                'current_role': player.current_role,
            }
        return p_conversion

    def jsonify_players_names(self):
        p_conversion = {}
        for p_id, player in self.players.items():
            p_conversion[p_id] = {
                'name': player.name
            }
        return p_conversion

    def jsonify_middle_cards(self):
        middle_card_conversion = {
            'left': str(self.middle_cards[0]),
            'middle': str(self.middle_cards[1]),
            'right': str(self.middle_cards[2]),
            'left_current': str(self.middle_cards[0]),
            'middle_current': str(self.middle_cards[1]),
            'right_current': str(self.middle_cards[2]),
        }
        return middle_card_conversion

    def add_player(self, name):
        MAX_ID = 100
        new_player_id = random.randint(0, MAX_ID)
        if new_player_id not in self.players.keys():
            self.players[new_player_id] = Human.Human(name, new_player_id)
        else:
            self.add_player(name)

    def start_game(self):
        if self.GAME_ON:
            return "Game is already in session."
        else:
            self.GAME_ON = True
            # TODO: assign spectators as that, and other roles as such.
            self.assign_characters()

    def assign_characters(self):
        # TODO: randomize
        # cur_char = 0
        # for player in self.players.values():
        #     player.assign_initial_role(self.characters[cur_char])
        #     cur_char += 1
        #     s = f'{player.name} is the {player.original_role}'
        #     print(s)

        werewolf_no = 5
        trouble_no = 4
        my_identity = trouble_no
        spect_no = 10
        for id, player in self.players.items():
            print(f'name: {player.name}')
            if player.name == 'Jah':
                self.players[id].assign_initial_role(self.characters[my_identity])
                print(f'My role is {player.original_role}')
            elif player.name == 'Taek':
                self.players[id].assign_initial_role(self.characters[spect_no])
            else:
                self.players[id].assign_initial_role(self.characters[spect_no])

        # TODO: assign middle card current values.
        self.middle_cards[0] = self.characters[7]
        self.middle_cards[1] = self.characters[8]
        self.middle_cards[2] = self.characters[9]

    def swap_roles(self, p1_id, p2_id):
        # Switches 2 player's roles by their player_id
        roleA = self.players.get(p1_id).current_role
        roleB = self.players.get(p2_id).current_role

        self.players.get(p1_id).current_role = roleB
        self.players.get(p2_id).current_role = roleA

        # QUESTION: why doesn't this work
        # temp_roll = self.players.get(p1_id).current_role
        # self.players.get(p1_id).current_role = self.players.get(p2_id).current_role
        # self.players.get(p2_id).current_role = temp_role

    def player_specific_info(self, player_id):
        print('here 2')
        return self.players[player_id].get_dict()

    def game_response_from_player_action(self, player_id, player_response):
        player_original_role = self.players[player_id].original_role
        response = player_original_role.process_player_response(self, player_id, player_response)
        return response
        #self.players[player_id].process_player_response()
