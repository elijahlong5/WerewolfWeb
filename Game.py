import GameHandlers.HumanPlayer as Player

import Characters.Insomniac as I
import Characters.Minion as M
import Characters.Robber as R
import Characters.Seer as S
import Characters.Troublemaker as T
import Characters.Werewolf as W
import Characters.Villager as V


import random


class WerewolfGame:

    def __init__(self):
        self.GAME_ON = False
        self.game_stage = 0
        self.characters = []
        self.players = {}
        self.middle_cards = []
        self.game_tracker = []
        self.discussion_stage = 0
        # improve this ^ and bad stage tracker method

        # Add the characters to the game
        # TODO: make this doable by the game host
        self.characters.append(I.Insomniac())
        self.characters.append(M.Minion())
        self.characters.append(R.Robber())
        self.characters.append(S.Seer())
        self.characters.append(T.Troublemaker())
        self.characters.append(W.Werewolf())
        self.characters.append(W.Werewolf())
        self.characters.append(W.Werewolf())
        self.characters.append(V.Villager())
        self.characters.append(V.Villager())

    def get_game_state(self):
        """
        :return: The game state in dictionary format for use within the json structure. Game state will be passed
        across the different players.
        """
        game_state = {
            'game_info': {
                'is_game_on': self.GAME_ON,
                'stage': self.game_stage,
            },
            'players': self.json_players_conversion(),
        }
        return game_state

    def json_players_conversion(self):
        p_conversion = {}
        for p_id, player in self.players.items():
            p_conversion[p_id] = {
                'name': player.name,
                'original_role': player.original_role,
                'current_role': player.current_role,
            }
        return p_conversion

    def add_player(self, name):
        MAX_ID = 100
        new_player_id = random.randint(0, MAX_ID)
        if new_player_id not in self.players.keys():
            self.players[new_player_id] = Player.HumanPlayer(name, new_player_id)
        else:
            self.add_player(name)

    def start_game(self):
        if self.GAME_ON:
            return "Game is in session."
        else:
            if len(self.characters) != self.players.__len__() + 3:
                err_mes = f'Error: There are {len(self.characters)} Characters and {self.players.__len__()} Players.' \
                      f'\nThere need to be {len(self.characters) - 3} Players.'
                print(err_mes)
                return
            self.game_stage = 1
            self.GAME_ON = True
            self.attribute_game_stages()
            self.assign_characters()

            self.game_opener()
            self.become_a_listener()

    def attribute_game_stages(self):
        # For now they are pretty static, but when Drunk, and Witch get implemented
        # some calculation will be needed here.
        for c in self.characters:
            # TODO: Use switch case here
            # Want if c is "Insomniac":
            if c.identity == "You are the Insomniac.":
                c.stage = 3
            elif c.identity == "You are the Troublemaker.":
                c.stage = 2
            else:
                c.stage = 1
            self.discussion_stage = 4
        return

    def game_opener(self):
        print("The game has begun")
        print("Here are the IDs and player names:")

        for id, player in self.players.items():
            print("ID:", str(id), "   , Player:", player.name)
        print("____________________________________")

    def assign_characters(self):
        # TODO: randomize
        cur_char = 0
        # QUESTION: can I remove "id" here
        for id, player in self.players.items():
            player.assign_initial_role(self.characters[cur_char])
            cur_char += 1
            s = f'{player.name} is the {player.original_role}'
            print(s)

        self.middle_cards = self.characters[cur_char:]
        print("[Middle Cards]")
        # QUESTION: Why does this work?
        print(self.middle_cards[0], self.middle_cards[1], self.middle_cards[2])
        # QUESTION: But this doesnt
        # print(self.middle_cards)

    def print_sitch(self):
        print('_____Game state_____')
        # Prints current game state
        for id, p in self.players.items():
            print(f'({id}), {p.name}:  {p.current_role}')
        print("Middle Cards")
        for c in self.middle_cards:
            print(f'{c}')

    def swap_roles(self, p1_id, p2_id):
        # Switches 2 player's roles by their player_id
        roleA = self.players.get(p1_id).current_role
        roleB = self.players.get(p2_id).current_role

        self.players.get(p1_id).current_role = roleB
        self.players.get(p2_id).current_role = roleA

        # QUESTION: why doesn't this work
        # temp_roll = self.players.get(p1_id).current_role
        # self.players.get(p1_id).current_role = self.players.get(p2_id).current_role
        # self.players.get(p2_id).current_roll = temp_roll

    def become_a_listener(self):
        """Listening for one of the human players to identify themselves"""
        listening = True
        while listening:
            print('listening... enter ID')
            x = input()

            if x == "Increment stage":
                self.game_stage += 1
                print(f'we are now in stage {self.game_stage}')
                print(f'we are now in stage {self.game_stage}')
                # Everyone has gone. Now discussion time
                if self.game_stage == self.discussion_stage:
                    listening = False
                    print('Everyone WAKE UP and discuss what happened during the night.')
            else:
                try:
                    self.listen_for_request(self.players[int(x)])
                except:
                    print("enter another ID")

    def listen_for_request(self, player):
        """Handling one of the human players' interactions"""
        listening = True
        while listening:
            p_roll = player.original_role
            print(f'We are in stage {self.game_stage}')
            if self.game_stage == 1:
                print(p_roll.identity)
            if p_roll.stage == self.game_stage:
                player_action = p_roll.action_request(self.players, self.middle_cards, player.player_id)
                # Keep a log of what's happening in the game
                self.game_tracker.append(player_action[0])

                if p_roll.alters_roles:
                    # Switch the 2 player's roles
                    self.swap_roles(player_action[1], player_action[2])
                    self.print_sitch()
            else:
                s = (f'This player goes in stage {player.original_role.stage}, '
                     f'But it is currently stage {self.game_stage}'
                     )
                print(s)

            listening = False


