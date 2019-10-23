document.addEventListener("DOMContentLoaded", function() {
    let initialPlayers = window.initialPlayers;
    let initialSpectators = window.initialSpectators;
    let playerId = null;
    try{
        playerId = GameService.getPlayerIdFromUrl();
    } catch (e){
        console.log('Player id not found.');
    }
    if (playerId !== null && initialPlayers[playerId]){
        GameServices.addElement("become-spectator", "toggle-spectator", "form",[],"",
            ["method", "post"]);
        GameServices.addElement("spectate", "become-spectator","button", ["button"],
            "Change to spectator", ["type", "submit"]);
        document.getElementById("spectate").addEventListener("click", function () {
            changeToSpectator(playerId);
        });
    } else {
        if (playerId !== null && initialSpectators[playerId]) {
            createChangeToPlayerDisplay(playerId)
        } else {
            GameServices.addElement("become-player", "toggle-spectator", "form",[],"",
                ["method", "post", "action", "/join-lobby/"]);
            GameServices.addElement("requested-name","become-player", "input", [],
                "",["type", "text", "name", "player_name_field"], true);
            GameServices.addElement("lobby-id","become-player", "input", [],
                "",["type", "hidden", "name", "access_token", "value", GameService.getAccessTokenFromUrl()]);
            GameServices.addElement("play", "become-player","button", ["button"],
                "Join lobby as a player", ["type", "submit"]);
        }
    }

    let characterChildren = document.getElementById("characters-dropdown").children;
    for (let i = 0; i < characterChildren.length; i++) {
        characterChildren[i].children[0].addEventListener("click", function () {
            requestAddPlayer(characterChildren[i].children[0].id, playerId);
        });
    }
    refresh();
});

function refresh() {
    setTimeout(refresh, GameService.timeBetweenRefreshes);
    redirectIfGameOn(access_token);
    refreshPlayersDiv(access_token);
    refreshCharacterDisplay(access_token);
}

function createChangeToPlayerDisplay(user_id) {
    document.getElementById("toggle-spectator").innerHTML = "";
    GameServices.addElement("become-player", "toggle-spectator", "form",[],"",
        ["method", "post"]);
    GameServices.addElement("play", "become-player","button", ["button"],
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
}

function changeToSpectator (user_id) {
    let req = {"user_id": user_id};
    let url = GameService.generateLobbyPostUrl() + "post_become_spectator/";
    GameService.fetchPostResponseFromServer(req, url).then(r => {
        createChangeToPlayerDisplay(user_id)
    });
}

function changeBackToPlayer (userId) {
    let req = {
        "user_id": userId,
    };
    let url = GameService.generateLobbyPostUrl() + "post_change_back_to_player/";
    GameService.fetchPostResponseFromServer(req, url).then(r => {
        document.getElementById("toggle-spectator").innerHTML = "";
        GameServices.addElement("become-spectator", "toggle-spectator", "form",[],"",
            ["method", "post"]);
        GameServices.addElement("spectate", "become-spectator","button", ["button"],
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
            GameServices.addElement(key, "players", "li", [],
                text, []);
        }
    }
}

async function refreshCharacterDisplay() {
    const response = await fetch(GameService.generateLobbyPostUrl() + 'characters/')
    const charactersDict = await response.json();
    let charactersInLobby = charactersDict['characters'];
    let validGameStartPoint = charactersDict['can_game_start'];
    console.log('is game at a valid starting point:', validGameStartPoint);

    let startGameButton = document.getElementById("start-game-button");
    if (validGameStartPoint && !startGameButton.classList.contains(GameService.validStartPointVar)) {
        startGameButton.classList.add(GameService.validStartPointVar);
    } else if (!validGameStartPoint && startGameButton.classList.contains(GameService.validStartPointVar)) {
        startGameButton.classList.remove(GameService.validStartPointVar);
    }

    let charactersDiv = document.getElementById("active-characters");
    charactersDiv.innerHTML = "";
    for (let c in charactersInLobby) {
        // Add character
        let divId = charactersInLobby[c] + "-" + c;
        GameServices.addElement(divId,
            charactersDiv.id, "div", [], charactersInLobby[c]);
        // Add remove button and event listener
        let characterName = document.getElementById(divId).innerText;
        GameServices.addElement(  characterName+'-remove-button-' + c,
            divId, "Button",[],"X");

        let button = document.getElementById(characterName+'-remove-button-' + c);
        button.addEventListener("click", function () {
            let removeThisPlayer = button.id.split("-")[0];
            requestRemoveCharacter(removeThisPlayer);
        });
    }
}

function requestAddPlayer(p, playerId) {
    console.log('trying to add char');
    if (playerId === null) {
        console.log("Can't add a character because player ID is null")
    }
    let requestDict = {
        "character": p,
    };
    console.log(requestDict);
    let addPlayerUrl = GameService.generateLobbyPostUrl() + 'request-add-character/';
    GameService.fetchPostResponseFromServer(requestDict, addPlayerUrl).then( r => {
        console.log('response is ', r);
    });
}

function requestRemoveCharacter(character) {
    let removeCharacterDict = {
        'character': character,
    };
    let removeCharacterUrl = GameService.generateLobbyPostUrl() + "request-remove-character/";
    GameService.fetchPostResponseFromServer(removeCharacterDict, removeCharacterUrl);
}




