/*
    This displays the identities of the other werewolves (retrieved from the game logic)
    If there are no other werewolves, the player must choose one card from the middle.
 */
document.addEventListener("DOMContentLoaded", function() {

    // Display who the other werewolves are, or the 3 middle cards.
    let werewolfDict = window.initial_player_dict;
    GameServices.addRoleDescription(werewolfDict['role-description']);

    let buttonDivName = GameService.roleDivId;

    if (werewolfDict['lone_wolf'] === false) {
        GameServices.addSimpleElement("h2", buttonDivName, "Here are the other werewolves.")
        for (let key in werewolfDict['fellow_wolves']) {
            let nrText = werewolfDict['fellow_wolves'][key];
            GameServices.addSimpleElement("li", buttonDivName, nrText);
        }
        GameService.addOkButton(buttonDivName);
    } else {

        let buttonFormId = "button-form";

        GameServices.addSimpleElement('h2', buttonDivName, "You're the lone wolf");
        GameServices.addElement(buttonFormId, buttonDivName, "form",[],"",
            ["method", "post"]);

        // Add Middle Cards
        GameServices.addSimpleElement("div", buttonFormId, "", GameService.middleCardDivId);
        GameService.addMiddleCardButtons(makeRequest,["type", "submit"]);
    }
});

function makeRequest(cardRequested) {
    let cardRequestedDict = {"card": cardRequested};
    GameService.fetchPostResponseFromServer(cardRequestedDict).then(r => {
        let display = document.getElementById(GameService.roleDivId);
        display.innerHTML = "The " + r['requested_card'] + " card is: " + r['card_identity'];
        GameService.addOkButton(GameService.roleDivId);
    });
}

