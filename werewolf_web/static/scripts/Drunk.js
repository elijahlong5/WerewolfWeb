document.addEventListener("DOMContentLoaded", function() {
    let drunkDict = window.initial_player_dict;
    GameServices.addRoleDescription(drunkDict["role-description"]);

    let buttonDivName = GameService.roleDivId;

    let buttonFormId = "button-form";

    GameServices.addSimpleElement('h2', buttonDivName, "Choose a card");
    GameServices.addElement(buttonFormId, buttonDivName, "form",[],"",
        ["method", "post"]);
    // Add Middle Cards
    GameServices.addSimpleElement("div", buttonFormId, "", GameService.middleCardDivId);
    GameService.addMiddleCardButtons(processRequest,["type", "submit"]);
});

function processRequest(cardRequested) {
    let cardRequestedDict = {"card": cardRequested};
    GameService.fetchPostResponseFromServer(cardRequestedDict).then(r => {
        let display = document.getElementById(GameService.roleDivId);
        display.innerHTML = r["response"];
        GameService.addOkButton(GameService.roleDivId);
    });
}