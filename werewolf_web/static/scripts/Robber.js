document.addEventListener("DOMContentLoaded", function() {

    let robberDict = window.initial_player_dict;

    GameServices.addRoleDescription(robberDict['role-description']);
    let roleDivId = GameService.roleDivId;
    let buttonDivId = 'name-buttons';

    GameServices.addSimpleElement("div", roleDivId, "", buttonDivId);

    let formId = 'submit-form';
    GameServices.addElement(formId, buttonDivId, "form",[],"",
        ["method", "post"]);

    for (let key in robberDict['names']) {
        GameServices.addElement(key, formId,"button", ["button"],
            robberDict['names'][key]['name'],
            ["type", "submit"]);

        document.getElementById(key).addEventListener("click", function () {
            event.preventDefault();
            rob({'robThisId': key});
        });
    }
});

function rob(victimId) {
    GameService.fetchPostResponseFromServer(victimId).then(r => {
        let display = document.getElementById(GameService.roleDivId);
        display.innerHTML = r['response'];
        GameService.addOkButton(GameService.roleDivId);
    });
}