import random
import string
import json
from flask import Flask, render_template, redirect, url_for, request, jsonify
from Game import WerewolfGame, Role

ACCESS_TOKEN_LENGTH = 5

lobbies = {}

app = Flask(__name__)


@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html')

# GAME ACTIONS
@app.route('/create-lobby/', methods=['post'])
def create_lobby_request():
    access = get_new_access_token()  # Returns a NEW access token
    lobbies[access] = WerewolfGame()

    game = lobbies[access]
    game.add_player("Jackie")
    game.add_player("Jilliam")
    game.add_player("Snoopy")
    game.add_player("Tonya")
    game.add_player("Taek")
    game.add_player("Sam")
    print(f'New lobby was added.  Access token: {access}')
    return redirect(url_for('lobby', access_token=access))


@app.route('/join-lobby/', methods=['post'])
def join_lobby():
    """
    Redirects to home, if access token is invalid
    Directs to lobby.
    Includes their player
    """
    access = request.form['access_token']
    print(f'Requested access code is {access}')
    if access in lobbies.keys():
        game = lobbies[access]
        print('Requested Access Token is valid.  Redirecting to lobby.')
        requested_name = request.form['player_name_field']
        if requested_name:
            p_id = game.add_player(requested_name)
            if p_id == -1:
                print("Name already used in lobby")
                print("Redirecting to lobby")
                return redirect(url_for('lobby',
                                        access_token=access))
            else:
                return redirect(url_for('lobby',
                                        access_token=access,
                                        player_id=p_id))

    else:
        print('Requested Access Token or Name not found.')
        return redirect(url_for('home'))


@app.route('/start_game/', methods=['post'])
def start_game():
    access_token = request.form['access_token']
    player_id = request.form['player_id']
    game = lobbies[access_token]
    if player_id is None or player_id == 'undefined' or player_id == 'spectator':
        return redirect(url_for('lobby',
                                access_token=access_token,
                                player_id=player_id,
                                werewolf_characters=Role,
                                players=lobbies[access_token].jsonify_players()))

    if int(player_id) in game.players.keys():
        if game.verify_startable_lobby():
            if not game.is_game_on:
                game.start_game()
                print(f"Game {access_token} is started.")
            return redirect(url_for('game_on',
                                    access_token=access_token,
                                    player_id=player_id))
    return redirect(url_for('lobby',
                            access_token=access_token,
                            player_id=player_id,
                            werewolf_characters=Role,
                            players=lobbies[access_token].jsonify_players()))


# GAME PHASES
@app.route('/lobby/<access_token>/')
@app.route('/lobby/<access_token>/player_id/<player_id>/')
def lobby(access_token, player_id=None):
    if access_token not in lobbies.keys():
        # Lobby has closed
        return redirect(url_for("home"))
    else:
        game = lobbies[access_token]

    if game.is_game_on:
        # Redirecting because the game is on
        if player_id is None or player_id == 'undefined':
            return redirect(url_for('game_on',
                                    access_token=access_token))
        else:
            return redirect(url_for('game_on',
                                    access_token=access_token,
                                    player_id=player_id))
    else:  # Game is not on
        if player_id == 'undefined' or player_id == "spectator" or (
                player_id is not None and (
                int(player_id) not in game.players.keys() and int(player_id) not in game.spectators.keys()
                )
        ):
            # Reidrecting because invalid user ID
            return redirect(url_for('lobby',
                                    access_token=access_token))
        return render_template('lobby.html',
                               access_token=access_token,
                               player_id=player_id,
                               werewolf_characters=Role,
                               active_characters=game.characters,
                               players=lobbies[access_token].jsonify_players(),
                               spectators=lobbies[access_token].jsonify_spectators())


@app.route('/game_on/<access_token>/')
@app.route('/game_on/<access_token>/player_id/<player_id>/')
def game_on(access_token, player_id=None):
    if access_token not in lobbies.keys():
        # Lobby has closed
        return redirect(url_for("home"))

    game = lobbies[access_token]

    if not game.is_game_on:
        # Redirecting back to lobby
        return redirect(url_for('lobby',
                                access_token=access_token,
                                player_id=player_id))
    if player_id is None:
        # Spectator without ID.
        return render_template('game_on.html',
                               access_token=access_token,
                               original_role="Spectator",
                               initial_player_dict=game.jsonify_full_game_state())
    elif player_id == 'undefined' or (
            int(player_id) not in game.players.keys() and int(player_id) not in game.spectators.keys()
    ):
        # Redirecting to this page but without a player ID.
        return redirect(url_for('game_on',
                                access_token=access_token))

    try:
        player_role = str(game.players[int(player_id)].original_role)
        player_dict = game.players[int(player_id)].get_role_initial_dict()
    except Exception as e:
        print(e)
        print('INVALID PLAYER ID WAS NOT REDIRECTED.')
        player_role = 'Spectator'
        player_dict = game.jsonify_full_game_state()
    return render_template('game_on.html',
                           access_token=access_token,
                           player_id=player_id,
                           original_role=player_role,
                           initial_player_dict=player_dict)


@app.route('/discussion/<access_token>/')
@app.route('/discussion/<access_token>/player_id/<player_id>/')
def wake_up(access_token, player_id=None):
    if player_id:
        return render_template('wake_up.html',
                               access_token=access_token,
                               player_id=player_id,
                               discussion_dict=lobbies[access_token].discussion_dict())


@app.route('/game-complete/<access_token>/')
@app.route('/game-complete/<access_token>/player_id/<player_id>/')
def game_complete(access_token, player_id=None):
    game = lobbies[access_token]
    # players_imprint = game.players
    # spectators_imprint = game.spectators
    # game.is_game_on = False
    #
    # # TODO: Display end of game stuff after game is complete
    # #   Who won, who voted for whom, etc
    # print('-----game log-------')
    # for l in game.game_log:
    #     print(l)
    #     print()
    # print('----- game status at upon completion ------')
    # for p in game.players.values():
    #     try:
    #         print(f'{p.name} received {p.votes_against} vote(s) against them, and they voted for {p.voted_for.name}')
    #     except Exception as e:
    #         print(f'{p.name} received {p.votes_against} vote(s) against them, and they voted for NO ONE')
    #
    # # RESET GAME FUNCTIONS BEFORE REDIRECTING TO LOBBY.
    # lobbies[access_token] = WerewolfGame()
    # lobbies[access_token].is_game_on = False
    # lobbies[access_token].players = players_imprint
    #
    # lobbies[access_token].spectators = spectators_imprint
    #
    # for p in lobbies[access_token].players.values():
    #     p.original_role = None
    #     p.current_role = None
    print(game.game_over_dictionary)
    return render_template('game_complete.html',
                           access_token=access_token,
                           player_id=player_id,
                           game_complete_dict=game.game_over_dictionary)

# GAME API REQUESTS
@app.route('/api/lobbies/<access_token>/players/')
def get_lobby_players(access_token):
    """
    :param access_token: lobby id
    :return: dictionary of active (non-spectating) players
    """
    return lobbies[access_token].jsonify_players()


@app.route('/api/lobbies/<access_token>/post_become_spectator/', methods=['post'])
def post_change_to_spectator(access_token):
    """Toggles the posted id between spectating and playing dictionaries in the game object."""
    user_id = request.json['user_id']
    game = lobbies[access_token]
    game.spectators[int(user_id)] = game.players[int(user_id)]
    game.players.pop(int(user_id))
    return jsonify({"status": "success"})


@app.route('/api/lobbies/<access_token>/post_change_back_to_player/', methods=['post'])
def post_change_back_to_player(access_token):
    user_id = request.json['user_id']
    game = lobbies[access_token]
    if int(user_id) not in game.spectators.keys():
        return redirect(url_for('lobby',
                                access_token=access_token))
    game.players[int(user_id)] = game.spectators[int(user_id)]
    game.spectators.pop(int(user_id))
    return jsonify({"status": "success"})


@app.route('/api/lobbies/<access_token>/game_on/')
def get_is_game_on(access_token):
    return {'game_on': lobbies[access_token].is_game_on}


@app.route('/api/lobbies/<access_token>/discussion/')
def get_is_discussion(access_token):
    if access_token in lobbies.keys():
        return {'discussion': lobbies[access_token].DISCUSSION_PHASE}
    else:
        return redirect(url_for('home'))


@app.route('/api/lobbies/<access_token>/players/<player_id>/player_specific_dict/')
def request_player_info_dict(access_token, player_id):
    game = lobbies[access_token]
    return jsonify(game.get_player_specific_info(int(player_id)))


@app.route('/api/lobbies/<access_token>/players/<player_id>/', methods=['post'])
def request_game_response(access_token, player_id):
    if access_token not in lobbies.keys():
        return redirect(url_for('home'))

    player_response = request.json
    game= lobbies[access_token]

    if not game.is_game_on:
        return redirect(url_for('lobby',
                                access_token=access_token,
                                player_id=player_id))
    return game.get_game_response(int(player_id), player_response)


@app.route('/api/lobbies/<access_token>/players/<player_id>/get_dict/')
def get_player_initial_dict(access_token, player_id):
    """ This is used for characters that don't go in the first round, and 
    must wait for other players to go before they can go.
    :returns the player dict, which should be incomplete if it isn't their turn yet.
    """
    game = lobbies[access_token]
    if access_token not in lobbies.keys():
        return redirect(url_for('home'))
    if game.is_game_on:
        initial_player_dict = game.players[int(player_id)].get_role_initial_dict()
        return jsonify(initial_player_dict)
    else:
        return redirect(url_for('home'))


@app.route('/api/lobbies/<access_token>/get_game_state/')
def get_game_state(access_token):
    game = lobbies[access_token]
    return jsonify(game.jsonify_full_game_state())


@app.route('/api/lobbies/<access_token>/players/<player_id>/cast-vote/', methods=['post'])
def cast_vote(access_token, player_id):
    game = lobbies[access_token]
    if int(player_id) in game.players.keys():
        vote_post = request.json
        cast_vote_dict = {
            'player_id': player_id,
            'vote_for_id': vote_post['vote_for_id'],
        }
        game.handle_vote_cast(cast_vote_dict)
        return jsonify({"status": "success"})
    else:
        print('Player id for casting vote not found in active players.')
        return jsonify({"status": "vote not submitted"})


@app.route('/api/lobbies/<access_token>/check-voting-status/')
def check_voting_status(access_token):
    # Returns false if everyone has voted
    game = lobbies[access_token]
    return jsonify({'still-voting': game.still_voting})


def get_new_access_token():
    if "RING1" not in lobbies.keys():
        return "RING1"
    t = ''.join(random.choices(string.ascii_uppercase + string.digits, k=ACCESS_TOKEN_LENGTH))
    if t not in lobbies.keys():
        return t
    else:
        return get_new_access_token()


if __name__ == "__main__":
    # TODO: Remove, just here for testing
    lobbies['RING1'] = WerewolfGame()
    game = lobbies['RING1']
    # game.add_player("Jackie")
    # game.add_player("Jilliam")
    # game.add_player("Snoopy")
    # game.add_player("Tonya")
    # game.add_player("Taek")
    # game.add_player("Sam")
    # app.run(debug=True, host='0.0.0.0', port=8080)
    app.run(debug=True, port=8080)
