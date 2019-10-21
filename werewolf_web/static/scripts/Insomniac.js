document.addEventListener("DOMContentLoaded", function () {
   let identity = window.initial_player_dict;

    GameServices.addSimpleElement("div", 'role-div',
        "You are notified of your identity right before the discussion," +
        "Please wait until your card is shown.");
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
    document.getElementById('role-div').innerHTML = "";
    GameServices.addElement("info",'role-div','div',[],
        'your card is ' + dict['current_role']);
    insomniacsCardDisplayed = true;
    GameService.addOkButton("role-div");
}
