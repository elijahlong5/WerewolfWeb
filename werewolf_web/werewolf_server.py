import random
import string
import json
from flask import Flask, render_template, redirect, url_for, request, jsonify
from Game import WerewolfGame, Role

ACCESS_TOKEN_LENGTH = 5

lobbies = {}
# TODO: Need to close out lobbies when there is no one left using them.

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
    # TODO: Have player created here. Create player.
    # TODO: And redirect to the join lobby page.  Want the "Name" field to handle both
    # TODO: Leaving space for a spectator mode.
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
        # TODO: If the game has already started then it should direct them to the spectator lobby
        print('Requested Access Token is valid.  Redirecting to lobby.')
        if request.form['player_name_field']:
            lobbies[access].add_player(request.form['player_name_field'])
            # TODO: Error if there are more players with the same name.  May return wrong ID.
            # TODO: Probably make it so people must enter unique names.
            for k, v in lobbies[access].players.items():
                if request.form['player_name_field'] == v.name:
                    # TODO: assign initial role to spectator
                    return redirect(url_for('lobby',
                                            access_token=access,
                                            player_id=k))
        return redirect(url_for('lobby',
                                access_token=access))
    else:
        print('Requested Access Token or Name not found.')
        return redirect(url_for('home'))


@app.route('/lobby/<access_token>/')
@app.route('/lobby/<access_token>/player_id/<player_id>/')
def lobby(access_token, player_id=None): # TODO: Player_id cant be None (including spectators)
    game = lobbies[access_token]
    if game.GAME_ON:
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


@app.route('/game_on/<access_token>/player_id/<player_id>/')
def game_on(access_token, player_id):
    game = lobbies[access_token]
    game_state = game.jsonify_full_game_state()
    # TODO: use player_dict here!
    try:
        player_role = game_state['players'][int(player_id)]['original_role']
        # TODO: This should be where the player dict is passed.
        # TODO: unless the dict needs to be refreshed to ask for. ie with the insomniac.
        player_dict = game.players[int(player_id)].get_dict()
    except Exception as e:
        print(e)
        player_role = 'spectator'
        player_dict = {'spectating': 'yup'}

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
