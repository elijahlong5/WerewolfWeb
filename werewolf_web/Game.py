from datetime import datetime
from datetime import timedelta

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

from datetime import datetime
from datetime import timedelta


class Role(Enum):
    INSOMNIAC = 'Insomniac'
    MINION = 'Minion'
    ROBBER = 'Robber'
    SEER = 'Seer'
    TROUBLEMAKER = 'Troublemaker'
    WEREWOLF = "Werewolf"
    VILLAGER = 'Villager'


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

        self.needs_to_go = []

    def next_turn(self):
        if self.turn_pointer.next is None:
            """Game should be over NOW"""
            return False
        else:
            self.turn_pointer = self.turn_pointer.next
            self.needs_to_go.append(self.turn_pointer.role)
            return True

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

        self.middle_cards = [0, 1, 2]
        self.game_log = []
        self.game_over_dictionary = {}

        self.disc_length = 0.5  # in minutes
        self.discussion_over_at = None

        self.characters.append(I.Insomniac(self))
        # self.characters.append(T.Troublemaker(self))
        self.characters.append(W.Werewolf(self))
        self.characters.append(W.Werewolf(self))

        self.characters.append(M.Minion(self))
        self.characters.append(R.Robber(self))
        # self.characters.append(S.Seer(self))

        # self.characters.append(W.Werewolf(self))
        # self.characters.append(W.Werewolf(self))
        # self.characters.append(V.Villager(self))
        # self.characters.append(V.Villager(self))

    def start_game(self):
        if self.is_game_on:
            return "Game is already in session."
        else:
            self.is_game_on = True
            self.DISCUSSION_PHASE = False
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

        if "Seer" in roles_in_play:
            self.turn_handler.needs_to_go.append("Seer")
        if "Minion" in roles_in_play:
            self.turn_handler.needs_to_go.append("Minion")
        for i in range(0, roles_in_play.count("Werewolf")):
            self.turn_handler.needs_to_go.append("Werewolf")
        for i in range(0, roles_in_play.count("Villager")):
            self.turn_handler.needs_to_go.append("Villager")
        for i in range(0, roles_in_play.count("Mason")):
            self.turn_handler.needs_to_go.append("Mason")

        print(f'just made needs to go list: {self.turn_handler.needs_to_go}')

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
            'left_current': str(self.middle_cards[0]),
            'middle_current': str(self.middle_cards[1]),
            'right_current': str(self.middle_cards[2]),
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
            print(f'name: {player.name} is the {player.current_role}')

    def get_player_specific_info(self, player_id):
        # This info the player uses to start their turn.
        return self.players[player_id].get_role_initial_dict()

    def get_game_response(self, player_id, player_response):
        player_original_role = self.players[player_id].original_role
        response = player_original_role.process_player_response(player_id, player_response)
        return response

    def update_move(self, role, move_method, arg1, arg2):
        """Handles players that need to switch the placement of the cards, does not handle the game log"""
        if role in self.turn_handler.needs_to_go:
            move_method(arg1, arg2)
            if not self.turn_handler.next_turn() and not len(self.turn_handler.needs_to_go):
                self.DISCUSSION_PHASE = True
                now = datetime.now()
                self.discussion_over_at = now + timedelta(seconds=self.disc_length*60)
                return
            while self.turn_handler.turn_pointer.stored_move is not None:
                print(f'The {self.turn_handler.whose_turn()} has a stored move, so that action is being taken.')
                stored_move = self.turn_handler.turn_pointer.stored_move
                stored_move['function'](stored_move['args'][0], stored_move['args'][1])
                # Remove them from needing to go.
                self.turn_handler.needs_to_go.pop(
                    self.turn_handler.needs_to_go.index(self.turn_handler.turn_pointer.role)
                )
                if not self.turn_handler.next_turn() and not len(self.turn_handler.needs_to_go):
                    print(f'Here is everyone that still needs to go {self.turn_handler.needs_to_go}')
                    self.DISCUSSION_PHASE = True
                    now = datetime.now()
                    self.discussion_over_at = now + timedelta(seconds=self.disc_length*60)
                return
        else:
            move = {
                "function": move_method,
                "args": [arg1, arg2],
            }
            self.turn_handler.store_a_move(role, move)

    def update_game_log(self, role, move_summary=None):

        if role in self.turn_handler.needs_to_go:
            print('game log appended')
            self.turn_handler.needs_to_go.pop(self.turn_handler.needs_to_go.index(role))
            if move_summary:
                self.game_log.append(move_summary)
            print(self.game_log)
        else:
            print("Updating game log, but not making the move happen.")
            self.game_log.append(move_summary)

        print(f'Here are the people who need to go {self.turn_handler.needs_to_go}')

        if not len(self.turn_handler.needs_to_go):
            print("no one else needs to go")
            self.DISCUSSION_PHASE = True
            now = datetime.now()
            self.discussion_over_at = now + timedelta(seconds=self.disc_length*60)

    def verify_startable_lobby(self):
        startable = True
        if len(self.characters) != len(self.players) + len(self.middle_cards):
            print(
                f'game not startable: player len {len(self.players)}'
                f'middle len {len(self.middle_cards)}'
                f'char len {len(self.characters)}'
            )
            startable = False
        # Checking to see that there is at least 1 werewolf in play.
        if "Werewolf" not in list(map(lambda c: str(c), self.characters)):
            startable = False
        return startable

    def discussion_dict(self):
        print(f'Discussion will be over at {self.discussion_over_at}')

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
                print("you've already voted!")
        else:
            # This should only happen if they haven't selected anyone at the end of the discussion time.
            self.players[int(cast_vote_dict["player_id"])].voted_for = "No one"

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
                    if str(p.current_role) == "Werewolf":
                        winning_team = "Villagers"

        # To maintain state while we display the game over screen
        self.game_over_dictionary = {
            'game_state': self.jsonify_full_game_state(),
            'died_list_id': who_died,
            'winning_team': winning_team,
        }

        for p in self.players.values():
            p.original_role = None
            p.current_role = None

        self.turn_handler = None
        self.is_game_on = False
        self.DISCUSSION_PHASE = False
        self.game_log = []
        # Dont need to reset spectators

        """
        Question to answer
        1. Who won, their original role, their current role.
        2. Who each player ended up as
        3. How many votes each person had, and who they voted for.
        :return:
        """
        # TODO: I think this should just be game state and handled in the server api?
        #   No it should be done here
