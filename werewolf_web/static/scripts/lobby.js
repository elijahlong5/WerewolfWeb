let timeBetweenRefreshes = 2000;

let GameService = new GameServices();
const access_token = GameService.getAccessTokenFromUrl();
document.addEventListener("DOMContentLoaded", function() {
    // If this is a player, add the 'become a spectator' option

    let initialPlayers = window.initialPlayers;
    let playerId = null;
    try{
        playerId = GameService.getPlayerIdFromUrl();
    } catch (e){
        console.log('Player id not found.');
    }
    if (playerId !== null && initialPlayers[playerId]){
        GameService.addElement("become-spectator", "toggle-spectator", "form",[],"",
            ["method", "post"]);
        GameService.addElement("spectate", "become-spectator","button", ["button"],
            "Change to spectator", ["type", "submit"]);
        document.getElementById("spectate").addEventListener("click", function () {
            changeToSpectator(playerId);
        });
    } else {
        GameService.addElement("become-player", "toggle-spectator", "form",[],"",
            ["method", "post", "action", "/join-lobby/"]);
        GameService.addElement("requested-name","become-player", "input", [],
            "",["type", "text", "name", "player_name_field"]);
        GameService.addElement("lobby-id","become-player", "input", [],
            "",["type", "hidden", "name", "access_token", "value", GameService.getAccessTokenFromUrl()]);
        GameService.addElement("play", "become-player","button", ["button"],
            "Join lobby as a player", ["type", "submit"]);
    }




    // Otherwise add become player button.
    refresh();
});


function changeToSpectator (user_id) {
    let req = {"user_id": user_id};
    let url = GameService.generateLobbyPostUrl() + "post_become_spectator/";
    GameService.fetchPostResponseFromServer(req, url).then(r => {
        document.getElementById("toggle-spectator").innerHTML = "";
        GameService.addElement("become-player", "toggle-spectator", "form",[],"",
            ["method", "post"]);
        GameService.addElement("play", "become-player","button", ["button"],
            "Change to player", ["type", "submit"]);
        document.getElementById("play").addEventListener("click", function () {
            let playerId = null;
            try{
                playerId = GameService.getPlayerIdFromUrl();
            } catch (e){
                console.log('Player id not found.');
            }
            changeBackToPlayer(playerId);
        });
    });
}

function changeBackToPlayer (userId) {
    let req = {
        "user_id": userId,
    };
    let url = GameService.generateLobbyPostUrl() + "post_change_back_to_player/";
    GameService.fetchPostResponseFromServer(req, url).then(r => {
        document.getElementById("toggle-spectator").innerHTML = "";
        GameService.addElement("become-spectator", "toggle-spectator", "form",[],"",
            ["method", "post"]);
        GameService.addElement("spectate", "become-spectator","button", ["button"],
            "Change to spectator", ["type", "submit"]);
        document.getElementById("spectate").addEventListener("click", function () {
            changeToSpectator(userId);
        });
    });
}

async function redirectIfGameOn(access_token) {
    const response = await fetch('/api/lobbies/' + access_token + '/game_on/');
    const is_game_on = await response.json();
    if (is_game_on['game_on']){
        console.log("game is on, redirecting to game on page.");
        const player_id_location_in_pathname = 4;
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[player_id_location_in_pathname];
        }
        catch(e) {
            console.log('no player id');
        }
        window.location.href = '/game_on/' + access_token + '/player_id/' + player_id + '/';
    }
}

function refresh() {
    setTimeout(refresh, timeBetweenRefreshes);
    redirectIfGameOn(access_token);
    refreshPlayersDiv(access_token);

}

async function refreshPlayersDiv(access_token) {
    // Get dictionary of active players
    const response = await fetch('/api/lobbies/' + access_token + '/players/')
    const responsePlayersDict = await response.json();

    let playersDiv = document.getElementById("players");
    // Removes 'spectators' from the div
    let playerChildren = playersDiv.children;
    for (let i = 0; i < playerChildren.length; i++ ) {
        if (playerChildren[i].tagName === "LI") {
            if (!(playerChildren[i].id in responsePlayersDict)) {
                let elem = document.getElementById(playerChildren[i].id);
                elem.parentNode.removeChild(elem);
            }
        }
    }
    // adds new player li elements if there are new players in the lobby
    for (const key in responsePlayersDict) {
        if (! document.getElementById(key)) {
            let text = responsePlayersDict[key]['name'] + " (id: " + key + ")";
            GameService.addElement(key, "players", "li", [],
                text, []);
        }
    }

}
