/*
    The Minion displays the identities of the other werewolves.
 */
document.addEventListener("DOMContentLoaded", function() {

    let werewolfDict = window.initial_player_dict;
    let roleDivId = "role-div";

    GameServices.addSimpleElement('h2', roleDivId, "Werewolves:");
    if (Object.keys(werewolfDict['wolves']).length === 0){
        GameServices.addSimpleElement("li", roleDivId, "There are NO WEREWOLVES");
    } else {
        for (let key in werewolfDict['wolves']) {
            let nrText = werewolfDict['wolves'][key];
            GameServices.addSimpleElement("li", roleDivId, nrText);
        }
    }
    GameService.addOkButton(roleDivId);
});
