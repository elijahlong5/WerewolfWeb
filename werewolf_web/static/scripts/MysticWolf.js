let namesDivId = 'name-buttons';
document.addEventListener("DOMContentLoaded", function() {
    let mysticWolfDict = window.initial_player_dict;
    let roleDivId = GameService.roleDivId;

    GameServices.addRoleDescription(mysticWolfDict['role-description']);

    GameServices.addSimpleElement('h2', roleDivId, "Werewolves:");
    if (Object.keys(mysticWolfDict['wolves']).length === 0){
        GameServices.addSimpleElement("li", roleDivId, "There are NO WEREWOLVES");
    } else {
        for (let key in mysticWolfDict['wolves']) {
            let nrText = mysticWolfDict['wolves'][key];
            GameServices.addSimpleElement("li", roleDivId, nrText);
        }
    }

    GameServices.addSimpleElement("div", roleDivId, "", namesDivId);
    let formId = 'submit-form';
    GameServices.addElement(formId, namesDivId, "form",[],"",
        ["method", "post"]);

    for (let key in mysticWolfDict['names']) {
        GameServices.addElement(key, formId,"button", ["button"],
            mysticWolfDict['names'][key]['name'],
            ["type", "submit"]);
        document.getElementById(key).addEventListener("click", function () {
            event.preventDefault();
            view({'viewThisId': key});
        });
    }

});

function view(cardRequestedDict){
    GameService.fetchPostResponseFromServer(cardRequestedDict).then(r => {
        let display = document.getElementById(namesDivId);
        display.innerHTML = r['response'];
        GameService.addOkButton(namesDivId);
    });

}