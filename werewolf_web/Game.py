from enum import Enum

import GameHandlers.Human as Human

import Characters.Insomniac as I
import Characters.Minion as M
import Characters.Robber as R
import Characters.Seer as S
import Characters.Troublemaker as T
import Characters.Werewolf as W
import Characters.Villager as V

import random


class Role(Enum):
    INSOMNIAC = 'Insomniac'
    MINION = 'Minion'
    ROBBER = 'Robber'
    SEER = 'Seer'
    TROUBLEMAKER = 'Troublemaker'
    WEREWOLF = "Werewolf"
    VILLAGER = 'Villager'

    SPECTATOR = 'Spectator'


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

        self.characters.append(I.Insomniac(self))
        self.characters.append(M.Minion(self))
        self.characters.append(R.Robber(self))

        self.characters.append(S.Seer(self))
        self.characters.append(T.Troublemaker(self))
        self.characters.append(W.Werewolf(self))
        self.characters.append(W.Werewolf(self))

        self.characters.append(W.Werewolf(self))
        self.characters.append(V.Villager(self))
        self.characters.append(V.Villager(self))

        shuffles = 100
        # for i in range(0, shuffles):
        #     card1 = random.randint(0, len(self.characters)-1)
        #     card2 = random.randint(0, len(self.characters)-1)
        #
        #     temp = self.characters[card1]
        #     self.characters[card1] = self.characters[card2]
        #     self.characters[card2] = temp


        #self.characters.append(Sp.Spectator(self))

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
        # TODO: Skip players that are spectators
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
            # PRINT GAME STATE:
            print('-----game state------')
            for p_id, player in self.players.items():
                print(f'id:{p_id}, name: {player.name}: Role   {player.original_role}')

            print('----Middle Cards:----')
            print(f'(Left){str(self.middle_cards[0])} (Middle){str(self.middle_cards[1])} (Right){str(self.middle_cards[0])}')

    def assign_characters(self):
        # TODO: randomize
        # cur_char = 0
        # for player in self.players.values():
        #     player.assign_initial_role(self.characters[cur_char])
        #     cur_char += 1
        #     s = f'{player.name} is the {player.original_role}'
        #     print(s)

        minion_no = 1
        rob_no = 2
        seer_no = 3
        werewolf_no = 5
        trouble_no = 4
        my_identity = werewolf_no
        spect_no = 10

        current_character = 0
        for id, player in self.players.items():
            self.players[id].assign_initial_role(self.characters[trouble_no])
            # print(f'name: {player.name}  is { self.characters[current_character]}')
            current_character += 1
            if player.name == 'Jah':
                self.players[id].assign_initial_role(self.characters[my_identity])
                print(f'My role is {player.original_role}')

            elif player.name == 'Taek':
                self.players[id].assign_initial_role(self.characters[werewolf_no])
            # else:
            #     self.players[id].assign_initial_role(self.characters[spect_no])

        # TODO: assign middle card current values.
        self.middle_cards[0] = self.characters[current_character]
        self.middle_cards[1] = self.characters[current_character + 1]
        self.middle_cards[2] = self.characters[current_character + 2]
        print(self.players)

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
        # This info the player uses to start their turn.
        return self.players[player_id].get_dict()

    def game_response_from_player_action(self, player_id, player_response):
        player_original_role = self.players[player_id].original_role
        response = player_original_role.process_player_response(player_id, player_response)
        return response

    def acceptable_starting_point(self):
        startable = True

        if len(self.characters) != len(self.players) + len(self.middle_cards):
            print(
                f'game not startable: player len {len(self.players)}'
                f'middle len {len(self.middle_cards)}'
                f'char len {len(self.characters)}'

            )
            startable = False
        # TODO: Check there is at least 1 werewolf.
        return startable
