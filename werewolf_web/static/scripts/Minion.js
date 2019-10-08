/*
    The Minion displays the identities of the other werewolves.
 */
let GameService = new GameServices();

document.addEventListener("DOMContentLoaded", function() {

    let werewolfDict = window.initial_player_dict;
    let roleDivId = "role-div"

    GameService.addSimpleElement('h2', roleDivId, "Werewolves:");
    if (Object.keys(werewolfDict['wolves']).length === 0){
        GameService.addSimpleElement("li", roleDivId, "There are NO WEREWOLVES");
    } else {
        for (let key in werewolfDict['wolves']) {
            let nrText = werewolfDict['wolves'][key];
            GameService.addSimpleElement("li", roleDivId, nrText);
        }
    }
});
