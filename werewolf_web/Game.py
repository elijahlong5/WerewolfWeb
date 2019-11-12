from datetime import datetime
from datetime import timedelta

from enum import Enum

import GameHandlers.Human as Human

import Characters.Drunk as D
import Characters.Insomniac as I
import Characters.Mason as Ma
import Characters.Minion as M
import Characters.MysticWolf as My
import Characters.Robber as R
import Characters.Seer as S
import Characters.Troublemaker as T
import Characters.Tanner as Ta
import Characters.Werewolf as W
import Characters.Witch as Wi
import Characters.Villager as V

import random

from datetime import datetime
from datetime import timedelta


class Role(Enum):
    DRUNK = "Drunk"
    INSOMNIAC = 'Insomniac'
    MASON = "Mason"
    MINION = 'Minion'
    MYSTICWOLF = "Mystic Wolf"
    ROBBER = 'Robber'
    SEER = 'Seer'
    TROUBLEMAKER = 'Troublemaker'
    TANNER = 'Tanner'
    WEREWOLF = "Werewolf"
    WITCH = "Witch"
    VILLAGER = 'Villager'


class Node:
    def __init__(self, role=None, cant_go_until_others_go=False):
        self.role = role
        self.next = None
        self.stored_move = None
        self.cant_go_until_others_go = cant_go_until_others_go


class TurnList:
    """ a Linked list of what roles can go when."""
    def __init__(self):
        self.head = Node()
        self.turn_pointer = self.head
        self.needs_to_go = []
        self.has_done_role = []

    def next_turn(self):
        if self.turn_pointer.next is None:
            return False
        else:
            self.turn_pointer = self.turn_pointer.next
            if self.turn_pointer.cant_go_until_others_go:
                self.needs_to_go.append(self.turn_pointer.role)
            return True

    def whose_turn(self):
        return self.turn_pointer.role

    def append(self, role, cant_go_until_others_go=False):
        new_node = Node(role, cant_go_until_others_go)
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node
        if not cant_go_until_others_go:
            # This player can make their move initially (ie robber, and NOT the insomniac.)
            self.needs_to_go.append(role)

    def get_node_at_role(self, role):
        cur = self.head
        while cur.role != role:
            cur = cur.next
        return cur

    def store_a_move(self, role, move):
        """This is used when someone makes a move, but it can't be processed yet.
        The move is stored and applied to the game once the turn pointer is at that role."""
        node = self.get_node_at_role(role)
        node.stored_move = move

    def has_next(self):
        if self.turn_pointer.next is None:
            return False
        else:
            return True


class WerewolfGame:

    def __init__(self):
        self.turn_handler = None

        self.is_game_on = False
        self.DISCUSSION_PHASE = False
        self.still_voting = True
        self.characters = []
        self.players = {}
        self.spectators = {}

        self.did_not_vote_str = "No one"
        self.min_player_count = 3

        self.middle_cards = [0, 1, 2]
        self.game_log = []
        self.game_over_dictionary = {}

        self.disc_length = 5  # in minutes
        self.discussion_over_at = None

        # BASE CHARACTERS
        self.characters.append(W.Werewolf(self))
        self.characters.append(W.Werewolf(self))
        self.characters.append(W.Werewolf(self))
        self.characters.append(W.Werewolf(self))
        self.characters.append(My.MysticWolf(self))
        self.characters.append(M.Minion(self))

    def start_game(self):
        if self.is_game_on:
            return "Game is already in session."
        else:
            self.is_game_on = True
            self.DISCUSSION_PHASE = False
            self.assign_characters()
            self.initialize_linked_list()
            # PRINT GAME STATE:
            # print('[-----game state------]')
            # for p_id, player in self.players.items():
            #     print(f'id:{p_id}, name: {player.name}: Role   {player.original_role}')
            # print('----Middle Cards:----')
            # print(f'(Left): {str(self.middle_cards[0])} (Middle): {str(self.middle_cards[1])}'
            #       f' (Right): {str(self.middle_cards[2])}')

    def assign_characters(self):
        shuffles = 50
        for i in range(0, shuffles):
            card1 = random.randint(0, len(self.characters) - 1)
            card2 = random.randint(0, len(self.characters) - 1)

            temp = self.characters[card1]
            self.characters[card1] = self.characters[card2]
            self.characters[card2] = temp

        current_character = 0

        for player in self.players.values():
            player.assign_initial_role(self.characters[current_character])
            current_character += 1

        self.middle_cards[0] = self.characters[current_character]
        self.middle_cards[1] = self.characters[current_character + 1]
        self.middle_cards[2] = self.characters[current_character + 2]

    def initialize_linked_list(self):
        self.turn_handler = TurnList()  # clear current list:
        # Find out what roles are accounted for (avoiding roles in the middle, or not used in the game)

        # USING PLAYER ID_ROLE to prevent players from going more than once.
        roles_in_play = []
        parallel_p_id_list = []
        for p_id, player in self.players.items():
            roles_in_play.append(str(player.original_role))
            parallel_p_id_list.append(f'{p_id}_{str(player.original_role)}')

        # Ordering the roles as they go in the game.
        # If they are able to go immediately when game starts,
        # then their role is appended to needs_to_go.
        if "Robber" in roles_in_play:
            self.turn_handler.append(parallel_p_id_list[roles_in_play.index("Robber")])
        if "Troublemaker" in roles_in_play:
            self.turn_handler.append(parallel_p_id_list[roles_in_play.index("Troublemaker")])
        if "Witch" in roles_in_play:
            self.turn_handler.append(parallel_p_id_list[roles_in_play.index("Witch")])
        if "Drunk" in roles_in_play:
            self.turn_handler.append(parallel_p_id_list[roles_in_play.index("Drunk")])
        if "Insomniac" in roles_in_play:
            self.turn_handler.append(parallel_p_id_list[roles_in_play.index("Insomniac")], True)

        # Go to first turn.
        self.turn_handler.next_turn()

        if "Seer" in roles_in_play:
            self.turn_handler.needs_to_go.append(parallel_p_id_list[roles_in_play.index("Seer")])
        if "Minion" in roles_in_play:
            self.turn_handler.needs_to_go.append(parallel_p_id_list[roles_in_play.index("Minion")])
        if "Mystic Wolf" in roles_in_play:
            self.turn_handler.needs_to_go.append(parallel_p_id_list[roles_in_play.index("Mystic Wolf")])
        if "Tanner" in roles_in_play:
            self.turn_handler.append(parallel_p_id_list[roles_in_play.index("Tanner")])
        for i in range(0, roles_in_play.count("Werewolf")):
            cur_index = roles_in_play.index("Werewolf")
            self.turn_handler.needs_to_go.append(parallel_p_id_list[cur_index])
            # pop from both arrays
            parallel_p_id_list.pop(cur_index)
            roles_in_play.pop(cur_index)
        for i in range(0, roles_in_play.count("Villager")):
            cur_index = roles_in_play.index("Villager")
            self.turn_handler.needs_to_go.append(parallel_p_id_list[cur_index])
            parallel_p_id_list.pop(cur_index)
            roles_in_play.pop(cur_index)
        for i in range(0, roles_in_play.count("Mason")):
            cur_index = roles_in_play.index("Mason")
            self.turn_handler.needs_to_go.append(parallel_p_id_list[cur_index])
            parallel_p_id_list.pop(cur_index)
            roles_in_play.pop(cur_index)
        print(f'Just made needs to go list: {self.turn_handler.needs_to_go}')

    def jsonify_full_game_state(self):
        """
        :return: The game state in dictionary format for use within the json structure. Game state will be passed
        across the different players.
        """
        game_state = {
            'players': self.jsonify_players(),
            'game_log': self.game_log,
            'middle_cards': self.jsonify_middle_cards(),
        }
        return game_state

    def jsonify_players(self):
        p_conversion = {}
        for p_id, player in self.players.items():
            p_conversion[p_id] = player.get_json_dict()
        return p_conversion

    def jsonify_spectators(self):
        spectators_dict = {}
        for p_id, player in self.spectators.items():
            spectators_dict[p_id] = player.get_json_dict()
        return spectators_dict

    def jsonify_players_names(self):
        """
        Returns dictionary of playing players.
        key is str id
        value is name
        every player in self.players is playing
        """
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
            'left_original': str(self.middle_cards[0]),
            'middle_original': str(self.middle_cards[1]),
            'right_original': str(self.middle_cards[2]),
        }
        return middle_card_conversion

    def add_player(self, name):
        if (
            # Name is original
                name in list(map(lambda p: p.name, self.players.values()))
                or name in list(map(lambda p: p.name, self.spectators.values()))
        ):
            print("Name found already in use.")
            return -1
        else:
            MAX_ID = 100
            new_player_id = random.randint(1, MAX_ID)
            if (
                # ID is original
                    new_player_id not in self.players.keys()
                    and new_player_id not in self.spectators.keys()
            ):
                if self.is_game_on:
                    self.spectators[new_player_id] = Human.Human(name, new_player_id)
                else:
                    self.players[new_player_id] = Human.Human(name, new_player_id)
                return new_player_id
            else:
                return self.add_player(name)

    def add_character(self, character):
        """
        Takes in string char name.
        Adds that character to self.characters.
        """
        character_strs = list(map(lambda c: str(c), self.characters))
        if character in character_strs:
            print('this character is already in here.')
            # Handles Characters that can be in the game multiple times
            # Masons, Werewolves and Villagers.
            if character == "Mason" and character_strs.count("Mason") <= 4:
                self.characters.append(Ma.Mason(self))
            elif character == "Werewolf" and character_strs.count("Werewolf") <= 4:
                #  Don't want more than 4 werewolves in the game
                self.characters.append(W.Werewolf(self))
            elif character == "Villager" and character_strs.count("Villager") <= 4:
                self.characters.append(V.Villager(self))

        else:
            # Handles Characters that can only be in the game once.
            # Will add all characters if they are not in
            # Robber, Seer, Insomniac, Minion, Troublemaker, Witch
            if character == "Drunk":
                self.characters.append(D.Drunk(self))
            elif character == "Insomniac":
                self.characters.append(I.Insomniac(self))
            elif character == "Robber":
                self.characters.append(R.Robber(self))
            elif character == "Mason":
                self.characters.append(Ma.Mason(self))
            elif character == "Minion":
                self.characters.append(M.Minion(self))
            elif character == "Mystic Wolf":
                self.characters.append(My.MysticWolf(self))
            elif character == "Witch":
                self.characters.append(Wi.Witch(self))
            elif character == "Tanner":
                self.characters.append(Ta.Tanner(self))
            elif character == "Troublemaker":
                self.characters.append(T.Troublemaker(self))
            elif character == "Seer":
                self.characters.append(S.Seer(self))
            elif character == "Werewolf":
                self.characters.append(W.Werewolf(self))
            elif character == "Villager":
                self.characters.append(V.Villager(self))

    def remove_character(self, character):
        character_strs = list(map(lambda c: str(c), self.characters))
        if (character == "Werewolf" and 1 < character_strs.count("Werewolf")) or character in character_strs:
            self.characters.pop(character_strs.index(character))

    def swap_role_with_mid(self, middle_card_choice, player_id):
        middle_card_choice = middle_card_choice.lower()
        cur_player = self.players[player_id]
        player_role_temp = self.players[player_id].current_role
        if middle_card_choice == "left":
            cur_index = 0
        elif middle_card_choice == "middle":
            cur_index = 1
        elif middle_card_choice == "right":
            cur_index = 2

        cur_player.current_role = self.middle_cards[cur_index]
        self.middle_cards[cur_index] = player_role_temp
        return

    def swap_roles(self, p1_id, p2_id):
        # Switches 2 player's roles by their player_id
        roleA = self.players.get(p1_id).current_role
        roleB = self.players.get(p2_id).current_role

        self.players.get(p1_id).current_role = roleB
        self.players.get(p2_id).current_role = roleA

    def get_player_specific_info(self, player_id):
        # This info the player uses to start their turn.
        return self.players[player_id].get_role_initial_dict()

    def get_game_response(self, player_id, player_response):
        player_original_role = self.players[player_id].original_role
        response = player_original_role.process_player_response(player_id, player_response)
        return response

    def enter_endgame(self):
        self.DISCUSSION_PHASE = True
        now = datetime.now()
        self.discussion_over_at = now + timedelta(seconds=self.disc_length*60)
        print(f'Discussion will be over at {self.discussion_over_at}')

    def update_move(self, role, move_method, arg1, arg2):
        """Handles players that need to switch the placement of the cards,
        does not handle the game log

        This is only called when the player's move is able to be processed,
        but not necessarily when the move can be executed.

        move is only executed if it is the player's turn to move.
        Otherwise move is stored, if they have not already gone.
        """

        if role in self.turn_handler.needs_to_go:
            # The move is able to be processed (not necessarily executed).
            if role == self.turn_handler.whose_turn():
                # Execute the move.
                move_method(arg1, arg2)
                # Now go to the next turn.
                if not self.turn_handler.next_turn() and not len(self.turn_handler.needs_to_go):
                    self.enter_endgame()
                    return
                while self.turn_handler.turn_pointer.stored_move is not None:
                    # There is a stored move for this role.
                    # Execute the stored move
                    stored_move = self.turn_handler.turn_pointer.stored_move
                    stored_move['function'](stored_move['args'][0], stored_move['args'][1])
                    # Go to the next Turn
                    has_next = self.turn_handler.has_next()
                    self.turn_handler.next_turn()
                    if not has_next and not len(self.turn_handler.needs_to_go):
                        # End game because everyone has gone.
                        self.enter_endgame()
                        return
                    elif not has_next:
                        # There are no more changing roles that need to go,
                        # but we are still waiting on people to go.
                        return
            else:
                # It is not their turn yet, but they were able to make their move.
                # Storing it for later.
                move = {
                    "function": move_method,
                    "args": [arg1, arg2],
                }
                self.turn_handler.store_a_move(role, move)
        else:
            print('role not in needs_to_go')

    def update_game_log(self, role, move_summary=None):
        if role in self.turn_handler.needs_to_go:
            self.turn_handler.needs_to_go.pop(self.turn_handler.needs_to_go.index(role))
            if move_summary:
                self.game_log.append(move_summary)
            print(self.game_log)
        else:
            self.game_log.append(move_summary)

        if not len(self.turn_handler.needs_to_go):
            self.enter_endgame()

    def verify_valid_game_starting_point(self):
        valid_starting_point = True
        if len(self.characters) != len(self.players) + len(self.middle_cards):
            valid_starting_point = False
        # Checking to see that there is at least 1 werewolf in play.
        character_strs = list(map(lambda c: str(c), self.characters))
        if ("Werewolf" not in character_strs
                or (2 >= len(self.players.keys()) and "Troublemaker" in character_strs)
                or len(self.players.keys()) <
                self.min_player_count
        ):
            # must reach min_player_count
            # There must be at least 1 werewolf
            # If the troublemaker is in play, then there must be at least 3 players
            valid_starting_point = False
        return valid_starting_point

    def discussion_dict(self):
        d = self.discussion_over_at
        if d is None:
            d = datetime.now()
            print('discussion time was not set.')
        exp_time = (
            f'{d.strftime("%b")} {d.strftime("%d")}, {d.strftime("%Y")}'
            f' {d.strftime("%H")}:{d.strftime("%M")}:{d.strftime("%S")}'
        )
        print(exp_time)
        vote_dict = {
            'exp_time': exp_time,
            'players': self.jsonify_players_names()  # Getting voting names.
        }
        return vote_dict

    def handle_vote_cast(self, cast_vote_dict):
        if cast_vote_dict['vote_for_id']:
            if self.players[int(cast_vote_dict["player_id"])].voted_for is None:
                self.players[int(cast_vote_dict["vote_for_id"])].votes_against += 1
                self.players[int(cast_vote_dict["player_id"])].voted_for = self.players[int(cast_vote_dict["vote_for_id"])]
            else:
                print("This player already voted!")
        else:
            # This should only happen if they haven't selected anyone at the end of the discussion time.
            self.players[int(cast_vote_dict["player_id"])].voted_for = self.did_not_vote_str
        status = False
        for p in self.players.values():
            if p.voted_for is None:
                status = True

        self.still_voting = status
        if not self.still_voting:
            self.calculate_winner()

    def calculate_winner(self):
        """
        Sets game_over_dict
        Resets game state.
        """
        # Find the highest and lowest number of votes.
        most_votes = 0
        least_votes = 0
        for p in self.players.values():
            print(f'votes against for {p.name} is {p.votes_against}')
            if p.votes_against > most_votes:
                most_votes = p.votes_against
        # Find who died and what is the winning team.
        who_died = []
        winning_team = "Werewolves"
        if most_votes == least_votes:
            # This means everyone received the same number of votes,  no one dies.
            who_died = []
        else:
            # Someone died.
            for p_id, p in self.players.items():
                if p.votes_against == most_votes:
                    # This player dies.
                    who_died.append(p_id)
                    if str(p.current_role) == "Werewolf" or str(p.current_role) == "Mystic Wolf":
                        winning_team = "Villagers"
                    elif str(p.current_role) == "Tanner":
                        winning_team = "Tanner"
                        break
        # To maintain state while we display the game over screen
        self.game_over_dictionary = {
            'game_state': self.jsonify_full_game_state(),
            'died_list_id': who_died,
            'winning_team': winning_team,
        }
        # Reset values
        for p in self.players.values():
            p.original_role = None
            p.current_role = None

        self.turn_handler = None
        self.is_game_on = False
        self.DISCUSSION_PHASE = False
        self.game_log = []
