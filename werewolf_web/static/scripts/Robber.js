let GameService = new GameServices();

document.addEventListener("DOMContentLoaded", function() {

    let player_names = window.initial_player_dict;

    let roleDivId = "role-div";
    let buttonDivId = 'name-buttons';

    GameService.addSimpleElement("div", roleDivId, "", buttonDivId);

    let formId = 'submit-form';
    GameService.addElement(formId, buttonDivId, "form",[],"",
        ["method", "post"]);

    for (let key in player_names['names']) {
        GameService.addElement(key, formId,"button", ["button"],
            player_names['names'][key]['name'],
            ["type", "submit"]);

        document.getElementById(key).addEventListener("click", function () {
            event.preventDefault();
            rob({'robThisId': key});
        });
    }
});

function rob(victimId) {
    GameService.fetchPostResponseFromServer(victimId).then(r => {
        let display = document.getElementById('role-div');
        display.innerHTML = r['response'];
    });
}