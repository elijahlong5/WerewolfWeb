document.addEventListener("DOMContentLoaded", function() {
    let masonDict = window.initial_player_dict;
    let roleDivId = GameService.roleDivId;

    GameServices.addRoleDescription(masonDict['role-description']);

    GameServices.addSimpleElement('h2', roleDivId, "Mason Info:");
    if (Object.keys(masonDict['masons']).length === 0){
        GameServices.addSimpleElement("li", roleDivId, "You are the only mason");
    } else {
        for (let key in masonDict['masons']) {
            let nrText = masonDict['masons'][key];
            GameServices.addSimpleElement("li", roleDivId, nrText);
        }
    }
    GameService.addOkButton(roleDivId);
});
