document.addEventListener("DOMContentLoaded", function() {
    let gameCompleteDict = window.gameCompleteDict;
    console.log(gameCompleteDict);

    // COMPILE APPROPRIATE VARIABLES:
    const container = document.getElementById('game-complete-container');
    let playerId = null;
    try{
        playerId = GameService.getPlayerIdFromUrl();

    } catch (e){
        console.log('Player id not found.');
    }
    let players = null;// gameCompleteDict['game_state']['players'];
    try{
        players = gameCompleteDict['game_state']['players'];

    } catch (e){
        console.log('game stat undefined. Redirecting...');
        window.location.href = '/lobby/' + access_token + '/player_id/' + playerId + '/';
    }
    const diedIds = gameCompleteDict['died_list_id'];
    const winningTeam = gameCompleteDict['winning_team'];


    let myPlayer = players[playerId];
    let myTeam = myPlayer['team'];

    if (playerId !== null) {
        // Handle display for players
        // Display my player's win status.
        let winStatus = "Lost";
        if (myTeam === winningTeam) {
            winStatus = "Won";
        }
        let text = myPlayer['name'] + ", You " + winStatus + " the game!";
        GameServices.addElement("player-game-status", container.id, "H1",
            ["Werewolf"], text);

        // Display winning team.
        let winningTeamText = "The " + winningTeam + " wins the game!";
        GameServices.addElement("winning-team-status", container.id, "H3",
            ["Werewolf"], winningTeamText);

        // Display Who died
        if (diedIds.length) {
            for (let i = 0; i < diedIds.length; i++) {
                let whoDiedText = "";
                if (diedIds[i] === playerId ) {
                    whoDiedText = "YOU died... rip";
                } else {
                    whoDiedText = players[diedIds[i]]['name']+ " Died.";
                }
                GameServices.addElement("dead-player-"+i, container.id, "H1",
                    ["Werewolf"], whoDiedText);
            }
        } else {
            GameServices.addElement("who-died", container.id, "H2",
                ["Werewolf"], "Nobody died?!");
        }
        // Display the card they ended up as.
        let finalCharacterText = "Your card is the " + myPlayer['current_role'];
        GameServices.addElement("player-character-status", container.id, "H2",
            ["Werewolf"], finalCharacterText);
    } else {
        // Handle display for spectators
    }

    //Add fancy display for votes for vs who voted for whom.
    let votesDivId = "additional-info";
    let votesUlId = "votes-ul";
    GameServices.addElement(votesDivId, container.id, "div",[], "");
    GameServices.addElement("vote-totals-button", votesDivId, "button",[], "Show vote totals");
    GameServices.addElement("vote-ballets-button", votesDivId, "button",[], "Show ballet results");
    GameServices.addElement("current-roles-button", votesDivId, "button",[], "People's current roles");
    GameServices.addElement("original-roles-button", votesDivId, "button",[], "People's original roles");
    GameServices.addElement(votesUlId, votesDivId, "UL",[], "");

    displayWhoVotedForWhom(players, votesUlId, playerId);

    document.getElementById("vote-ballets-button").addEventListener("click", function () {
        displayWhoVotedForWhom(players, votesUlId, playerId);
    });
    document.getElementById("vote-totals-button").addEventListener("click", function () {
        displayVoteTotals(players, votesUlId, playerId);
    });
    document.getElementById("current-roles-button").addEventListener("click", function () {
        displayCurrentRoles(players, votesUlId, playerId);
    });
    document.getElementById("original-roles-button").addEventListener("click", function () {
        displayOriginalRoles(players, votesUlId, playerId);
    });
});

function displayWhoVotedForWhom(players, votesUlId, playerId) {
    let votesUl = document.getElementById(votesUlId);
    votesUl.innerHTML = "";
    for (let p in players) {
        let text = "";

        let votedForName = "no one";
        if (players[p]['voted_for_id'] === null) {

        } else if ("name" in players[players[p]['voted_for_id']]) {
            votedForName = players[players[p]['voted_for_id']]['name'];
        }
        if (p === playerId){
            text = "You voted for "+votedForName;
        } else {
            text = players[p]['name']+" voted for "+votedForName;
        }
        GameServices.addElement("votes-"+p, votesUl.id, "LI",
            [], text);
    }
}


function displayVoteTotals(players, votesUlId, playerId){
    let votesUl = document.getElementById(votesUlId);
    votesUl.innerHTML = "";
    for (let p in players) {
        let text = "";
        if (players[p]['votes_for'] === 0){
            text = players[p]['name']+" - received no votes";
        } else {
            text = players[p]['name']+" - received "+players[p]['votes_for']+" votes"
        }
        GameServices.addElement("votes-"+p, votesUl.id,
            "LI",[], text);
    }
}


function displayCurrentRoles(players, votesUlId, playerId){
    let votesUl = document.getElementById(votesUlId);
    votesUl.innerHTML = "";
    for (let p in players) {
        let text = "";
        if (p === playerId){
            text = "You are" + stringifyRole(players[p]['current_role']);
        } else {
            text = players[p]['name']+" is" + stringifyRole(players[p]['current_role']);
        }
        GameServices.addElement("votes-"+p, votesUl.id,
            "LI",[], text);
    }
}


function displayOriginalRoles(players, votesUlId, playerId){
    let votesUl = document.getElementById(votesUlId);
    votesUl.innerHTML = "";
    for (let p in players) {
        let text = "";
        if (p === playerId){
            text = "You were" + stringifyRole(players[p]['original_role']);
        } else {
            text = players[p]['name']+" was" + stringifyRole(players[p]['original_role']);
        }
        GameServices.addElement("votes-"+p, votesUl.id,
            "LI",[], text);
    }
}


function stringifyRole(role) {
    let joiner = " a ";
    if (['A','E','I','O','U'].includes(role.charAt(0))) {
        joiner = " an ";
    }
    if (["Minion","Seer","Troublemaker","Insomniac","Robber"].includes(role)){
        joiner = " the ";
    }
    return joiner + role;s
}