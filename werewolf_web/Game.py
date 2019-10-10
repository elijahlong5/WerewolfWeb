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


class Node:
    def __init__(self, role=None):
        self.role = role
        self.next = None
        self.stored_move = None


class TurnList:
    """ a Linked list of what roles can go when."""
    def __init__(self):
        self.head = Node()
        self.turn_pointer = self.head

    def next_turn(self):
        if self.turn_pointer.next is None:
            print("Game Over")
        else:
            self.turn_pointer = self.turn_pointer.next

    def whose_turn(self):
        return self.turn_pointer.role

    def append(self, role):
        new_node = Node(role)
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def get_node_at_role(self, role):
        cur = self.head
        while cur.role is not role:
            cur = cur.next
        return cur

    def store_a_move(self, role, move):
        """this is used when someone makes a move, but it can't be processed yet.
        The move is stored and applied to the game once the turn pointer is at that role."""
        node = self.get_node_at_role(role)
        node.stored_move = move


class WerewolfGame:

    def __init__(self):
        self.turn_handler = None

        self.GAME_ON = False
        self.game_stage = 0
        self.characters = []
        self.players = {}

        self.middle_cards = [0, 1, 2]
        self.game_log = []
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

        # self.characters.append(Sp.Spectator(self))

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
        """
        Returns dictionary of playing players.
        key is str id
        value is name
        """
        # TODO: Skip players that are spectators
        name_dict = {'names': {}}
        for p_id, player in self.players.items():
            name_dict['names'][str(p_id)] = {
                'name': player.name
            }
        return name_dict

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
            self.initialize_linked_list()

            # PRINT GAME STATE:
            print('-----game state------')
            for p_id, player in self.players.items():
                print(f'id:{p_id}, name: {player.name}: Role   {player.original_role}')

            print('----Middle Cards:----')
            print(f'(Left): {str(self.middle_cards[0])} (Middle): {str(self.middle_cards[1])}'
                  f' (Right): {str(self.middle_cards[2])}')

    def assign_characters(self):

        shuffles = 0
        for i in range(0, shuffles):
            card1 = random.randint(0, len(self.characters)-1)
            card2 = random.randint(0, len(self.characters)-1)

            temp = self.characters[card1]
            self.characters[card1] = self.characters[card2]
            self.characters[card2] = temp

        minion_no = 1
        robber = 2
        seer_no = 3
        werewolf_no = 5
        trouble_no = 4
        my_identity = robber
        taek_identity = trouble_no
        spect_no = 10

        current_character = 0

        for id, player in self.players.items():
            if player.name == "Jah":
                self.players[id].assign_initial_role(self.characters[my_identity])
            elif player.name == "Taek":
                self.players[id].assign_initial_role(self.characters[taek_identity])
            else:
                self.players[id].assign_initial_role(self.characters[current_character])
            # print(f'name: {player.name}  is { self.characters[current_character]}')
            current_character += 1

        self.middle_cards[0] = self.characters[current_character]
        self.middle_cards[1] = self.characters[current_character + 1]
        self.middle_cards[2] = self.characters[current_character + 2]

    def initialize_linked_list(self):
        # clear it just in case:
        self.turn_handler = TurnList()
        # Find out what roles are accounted for (avoiding roles in the middle, or not used in the game)
        roles_in_play = []
        for player in self.players.values():
            roles_in_play.append(str(player.original_role))

        # Just ordering them
        if "Robber" in roles_in_play:
            self.turn_handler.append("Robber")
        if "Troublemaker" in roles_in_play:
            self.turn_handler.append("Troublemaker")
        if "Insomniac" in roles_in_play:
            self.turn_handler.append("Insomniac")

        self.turn_handler.next_turn()

    def swap_roles(self, p1_id, p2_id):
        # Switches 2 player's roles by their player_id
        roleA = self.players.get(p1_id).current_role
        roleB = self.players.get(p2_id).current_role

        self.players.get(p1_id).current_role = roleB
        self.players.get(p2_id).current_role = roleA

        # QUESTION: why doesn't this work
        # temp_role = self.players.get(p1_id).current_role
        # self.players.get(p1_id).current_role = self.players.get(p2_id).current_role
        # self.players.get(p2_id).current_role = temp_role

        print('swap happened')
        for id, player in self.players.items():
            print(f'name: {player.name} is the { player.current_role}')

    def player_specific_info(self, player_id):
        # This info the player uses to start their turn.
        return self.players[player_id].get_dict()

    def game_response_from_player_action(self, player_id, player_response):
        player_original_role = self.players[player_id].original_role
        response = player_original_role.process_player_response(player_id, player_response)
        return response

    def update_move(self, role, move_method, arg1, arg2):

        if self.turn_handler.whose_turn() == role:
            move_method(arg1, arg2)

            self.turn_handler.next_turn()

            while self.turn_handler.turn_pointer.stored_move is not None:
                print(f'The {self.turn_handler.whose_turn()} has a stored move, so that action is being taken.')
                stored_move = self.turn_handler.turn_pointer.stored_move
                stored_move['function'](stored_move['args'][0], stored_move['args'][1])
                self.turn_handler.next_turn()
        else:
            move = {
                "function": move_method,
                "args": [arg1, arg2],
            }
            self.turn_handler.store_a_move(role, move)



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
