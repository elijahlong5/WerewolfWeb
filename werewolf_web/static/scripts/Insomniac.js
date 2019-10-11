let GameService = new GameServices();
document.addEventListener("DOMContentLoaded", function () {
   let identity = window.initial_player_dict;

    GameService.addSimpleElement("div", 'role-div',
        "You are notified of your identity right before the discussion," +
        "<br/>Please wait until your card is shown.");
    refresh();
});

let timeBetweenRefreshes = 2000

async function refreshPlayerDict() {
    // adds new player li elements if there are new players in the lobby
    const access_token = window.location.pathname.split('/')[2];

    const player_id = window.location.pathname.split('/')[4];

    let url = '/api/lobbies/'
        + access_token
        + '/players/'
        + player_id
        + '/get_dict/';
    const response = await fetch(url);
    const dict = await response.json();
    console.log(dict)
    if (dict['ready'] == true) {
        return showCard(dict);
    }
}

function refresh() {
    setTimeout(refresh, timeBetweenRefreshes);
    refreshPlayerDict();
}

function showCard(dict) {
    GameService.addElement("info",'role-div','div',[],
        'your card is ' + dict['current_role']);
    let formId = "submit-form";
    let submitFormButtonId = "form-submit-button";
    GameService.addElement(formId, 'role-div', "form",[],"",
        ["method", "post"]);
    GameService.addElement(submitFormButtonId, formId, "button",["button"],
        "ok!",["type","submit"]);
    document.getElementById(submitFormButtonId).addEventListener("click", function(){
        event.preventDefault();
        notify({"status": "acknowledged"});
    });
}

function notify(dict) {
    GameService.fetchPostResponseFromServer(dict).then(r => {
        console.log(r)
    });
}
