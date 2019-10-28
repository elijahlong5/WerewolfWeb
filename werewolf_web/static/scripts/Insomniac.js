document.addEventListener("DOMContentLoaded", function () {
    let initialPlayerDict = window.initial_player_dict;
    GameServices.addRoleDescription(initialPlayerDict['role-description']);
    let minTimeBeforeShowing = Math.floor(Math.random() * 3000) + 3000;
    setTimeout(refresh, minTimeBeforeShowing);
});

let insomniacsCardDisplayed = false;

async function refreshPlayerDict() {
    // adds new player li elements if there are new players in the lobby
    let base_url = GameService.generatePostUrlForInitialDict();

    let url = base_url + 'get_dict/';
    const response = await fetch(url);
    const dict = await response.json();
    if (dict['ready'] === true && !insomniacsCardDisplayed) {
        return showCard(dict);
    }
}

function refresh() {
    setTimeout(refresh, GameService.timeBetweenRefreshes);
    if (!insomniacsCardDisplayed){
        refreshPlayerDict();
    }
}

function showCard(dict) {
    document.getElementById(GameService.roleDivId).innerHTML = "";
    GameServices.addElement("info",GameService.roleDivId,'div',[],
        'your card is ' + dict['current_role']);
    insomniacsCardDisplayed = true;
    GameService.addOkButton(GameService.roleDivId);
}
