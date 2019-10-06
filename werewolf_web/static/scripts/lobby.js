time_between_refreshes = 2000

async function refresh_player_div(access_token) {
    // adds new player li elements if there are new players in the lobby
    const response = await fetch('/api/lobbies/' + access_token + '/players/')
    const responsePlayersDict = await response.json()
    for (const key in responsePlayersDict) {
        if (! document.getElementById(key)) {
            const element = document.createElement("li");
            element.innerText = responsePlayersDict[key]['name'] + " (id: " + key + ")";
            element.id = key;
            document.getElementById("players").appendChild(element);
        }
    }
}

async function redirect_if_game_on(access_token) {
    const response = await fetch('/api/lobbies/' + access_token + '/game_on/');
    const is_game_on = await response.json();
    if (is_game_on['game_on']){
        console.log("game is on, redirecting to game on page.")
        const player_id_location_in_pathname = 4
        let player_id = null
        try {
            player_id = window.location.pathname.split('/')[player_id_location_in_pathname]
        }
        catch(e) {
            console.log('no player id')
        }
        window.location.href = '/game_on/' + access_token + '/player_id/' + player_id + '/'

    }
}

function refresh() {
    setTimeout(refresh, time_between_refreshes);
    const access_token_location_in_pathname = 2
    const access_token = window.location.pathname.split('/')[access_token_location_in_pathname]
    redirect_if_game_on(access_token)
    refresh_player_div(access_token)
}

document.addEventListener("DOMContentLoaded", function() {
    refresh()
})
