document.addEventListener("DOMContentLoaded", function() {
    let divName = GameService.roleDivId;
    let witchDict = window.initial_player_dict;

    GameServices.addRoleDescription(witchDict['role-description']);

    let buttonDivName = "button-div";
    GameServices.addElement(buttonDivName, divName,"div",[],"");
    let buttonFormId = "button-form";
    GameServices.addElement(buttonFormId, buttonDivName, "form",[],"",
        ["method", "post"],);

    GameServices.addElement(buttonFormId, buttonDivName, "form",[],"",
        ["method", "post"]);

    // Add Middle Cards
    GameServices.addSimpleElement("div", buttonFormId, "", GameService.middleCardDivId);
    GameService.addMiddleCardButtons(chooseMiddleCard,["type", "submit"]);

    window.witchDict = witchDict;
    // Add Middle Cards
    GameServices.addSimpleElement("div", buttonFormId, "", GameService.middleCardDivId);
    GameService.addMiddleCardButtons(makeRequest,["type", "submit"]);
});

function chooseMiddleCard(cardRequested) {
    let cardRequestedDict = {"card": cardRequested};
    GameService.fetchPostResponseFromServer(cardRequestedDict).then(r => {
        let display = document.getElementById('button-div');
        display.innerHTML = "The " + r['requested_card'] + " card is " + r['card_identity'] + ".</br>" +
            "Who do you want to give this card to?";
        displayWitchPhase2();
    });
}

function witchSwitch(playerIdDict) {
    GameService.fetchPostResponseFromServer(playerIdDict).then(r => {
        let display = document.getElementById('button-div');
        display.innerHTML = r['response'];
        GameService.addOkButton(display.id);
    });
}

function displayWitchPhase2() {
    let playerNames = window.witchDict;

    let buttonDivId = "button-div";
    let formId = 'submit-form';
    GameServices.addElement(formId, buttonDivId, "form",[],"",
        ["method", "post"]);

    for (let key in playerNames['names']) {
        GameServices.addElement(key, formId,"button", ["button"],
            playerNames['names'][key]['name'],
            ["type", "submit"]);

        document.getElementById(key).addEventListener("click", function () {
            event.preventDefault();
            witchSwitch({'playerId': key});
        });
    }
}

