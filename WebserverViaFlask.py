import random
import string

from flask import Flask, render_template, redirect, url_for, request
from Game import WerewolfGame

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
    lobbies[access].add_player("Jackie")
    lobbies[access].add_player("Jilliam")
    lobbies[access].add_player("Snoopy")
    lobbies[access].add_player("Tonya")
    lobbies[access].add_player("Taek")
    lobbies[access].add_player("Sam")
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


# @app.route('/lobby/')
@app.route('/lobby/<access_token>/')
@app.route('/lobby/<access_token>/player_id/<player_id>')
def lobby(access_token, player_id=None):
    return render_template('lobby.html',
                           access_token=access_token,
                           player_id=player_id,
                           players=lobbies[access_token].get_game_state()['players'])


@app.route('/start_game/', methods=['post'])
def start_game():
    access_token = request.form['access_token']
    player_id = request.form['player_id']
    if not lobbies[access_token].GAME_ON:

        # TODO:lobbies[access_token].start_game()
        print(f"Game {access_token} is started.")
    return redirect(url_for('game_on',
                            access_token=access_token,
                            player_id=player_id))


@app.route('/game_on/<access_token>/player_id/<player_id>/')
def game_on(access_token, player_id):
    return render_template('game_on.html',
                           access_token=access_token,
                           player_id=player_id)


def get_new_access_token():
    if "RING1" not in lobbies.keys():
        return "RING1"
    t = ''.join(random.choices(string.ascii_uppercase + string.digits, k=ACCESS_TOKEN_LENGTH))
    if t not in lobbies.keys():
        return t
    else:
        return get_new_access_token()


if __name__ == "__main__":
    app.run(debug=True, port=8080)
