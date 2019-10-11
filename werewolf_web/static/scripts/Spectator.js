const new_element = document.createElement("li");
new_element.innerText = 'YOU ARE SPECTATING THE GAME.';
document.getElementById("role-div").appendChild(new_element);


document.addEventListener("DOMContentLoaded", function() {
    let gameState = window.initial_player_dict;
    console.log(gameState);
    refresh();
});

timeBetweenRefreshes = 4000;
let GameService = new GameServices();
async function refreshGameState(access_token) {

    // adds new player li elements if there are new players in the lobby
    const response = await fetch('/api/lobbies/' + access_token + '/get_game_state/')
    const gameState = await response.json();

    document.getElementById('role-div').innerHTML = "";
    let playerDivId = "player-div";
    GameService.addElement(playerDivId, 'role-div','div',
        [],"Players:");
    for (let item in gameState['players']) {
        let cur_player = "Player name: " + gameState['players'][item]["name"] + " is the " + gameState['players'][item]["original_role"];
        GameService.addElement(item, playerDivId, 'div',[], cur_player);
    }

}

function refresh() {
    setTimeout(refresh, timeBetweenRefreshes);
    const access_token_location_in_pathname = 2;
    const access_token = window.location.pathname.split('/')[access_token_location_in_pathname];
    refreshGameState(access_token);
}