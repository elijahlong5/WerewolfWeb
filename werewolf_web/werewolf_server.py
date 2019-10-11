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


@app.route('/lobby/<access_token>/')
@app.route('/lobby/<access_token>/player_id/<player_id>/')
def lobby(access_token, player_id=None):
    game = lobbies[access_token]
    if game.GAME_ON:
        if player_id is None:
            player_id = 'spectating'
        return redirect(url_for('game_on',
                                access_token=access_token,
                                player_id=player_id))
    else:
        return render_template('lobby.html',
                               access_token=access_token,
                               player_id=player_id,
                               werewolf_characters=Role,
                               players=lobbies[access_token].jsonify_players())


@app.route('/start_game/', methods=['post'])
def start_game():
    access_token = request.form['access_token']
    player_id = request.form['player_id']
    game = lobbies[access_token]
    if game.acceptable_starting_point():
        if not game.GAME_ON:
            game.start_game()
            print(f"Game {access_token} is started.")

        return redirect(url_for('game_on',
                                access_token=access_token,
                                player_id=player_id))
    else:
        return redirect(url_for('lobby',
                                access_token=access_token,
                                player_id=player_id,
                                werewolf_characters=Role,
                                players=lobbies[access_token].jsonify_players()))


@app.route('/game_on/<access_token>/')
@app.route('/game_on/<access_token>/player_id/<player_id>/')
def game_on(access_token, player_id):
    game = lobbies[access_token]
    try:
        player_role = str(game.players[int(player_id)].original_role)
        player_dict = game.players[int(player_id)].get_dict()
    except Exception as e:
        print(e)
        player_role = 'Spectator'
        player_dict = game.jsonify_full_game_state()

    return render_template('game_on.html',
                           access_token=access_token,
                           player_id=player_id,
                           original_role=player_role,
                           initial_player_dict=player_dict)


@app.route('/api/lobbies/<access_token>/players/')
def get_lobby_players(access_token):
    return lobbies[access_token].jsonify_players()


@app.route('/api/lobbies/<access_token>/game_on/')
def get_is_game_on(access_token):
    return {'game_on': lobbies[access_token].GAME_ON}


@app.route('/api/lobbies/<access_token>/players/<player_id>/player_specific_dict/')
def request_player_info_dict(access_token, player_id):
    game = lobbies[access_token]
    return jsonify(game.player_specific_info(int(player_id)))


@app.route('/api/lobbies/<access_token>/players/<player_id>/', methods=['post'])
def request_game_response(access_token, player_id):
    player_response = request.json
    game = lobbies[access_token]
    return game.game_response_from_player_action(int(player_id), player_response)


@app.route('/api/lobbies/<access_token>/players/<player_id>/get_dict/')
def get_player_initial_dict(access_token, player_id):
    """ This is used for characters that don't go in the first round, and 
    must wait for other players to go before they can go.
    :returns the player dict, which should be incomplete if it isn't their turn yet.
    """
    game = lobbies[access_token]
    initial_player_dict = game.players[int(player_id)].get_dict()
    return jsonify(initial_player_dict)


@app.route('/api/lobbies/<access_token>/get_game_state/')
def get_game_state(access_token):
    game = lobbies[access_token]
    return jsonify(game.jsonify_full_game_state())

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
    game.add_player("Jackie")
    game.add_player("Jilliam")
    game.add_player("Snoopy")
    game.add_player("Tonya")
    game.add_player("Taek")
    game.add_player("Sam")
    app.run(debug=True, port=8080)