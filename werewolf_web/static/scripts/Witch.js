document.addEventListener("DOMContentLoaded", function() {
    let divName = GameService.roleDivId;
    let witchDict = window.initial_player_dict;

    GameServices.addRoleDescription(witchDict['role-description']);

    let buttonDivName = "button-div";
    GameServices.addElement(buttonDivName, divName,"div",[],"");
    let buttonFormId = "button-form";
    GameServices.addElement(buttonFormId, buttonDivName, "form",[],"",
        ["method", "post"],);
    GameServices.addElement("Left", buttonFormId,"button", ["button"],
        "Left", ["type", "submit"]);
    GameServices.addElement("Middle", buttonFormId,"button",["button"],
        "Middle", ["type", "submit"]);
    GameServices.addElement("Right", buttonFormId,"button",["button"],
        "Right", ["type", "submit"]);

    document.getElementById("Left").addEventListener("click", function(){
        chooseMiddleCard("Left", witchDict);
    });
    document.getElementById("Middle").addEventListener("click",function(){
        chooseMiddleCard("Middle", witchDict);
    });
    document.getElementById("Right").addEventListener("click",function(){
        chooseMiddleCard("Right", witchDict);
    });
});

function chooseMiddleCard(cardRequested, player_names) {
    let cardRequestedDict = {"card": cardRequested};
    GameService.fetchPostResponseFromServer(cardRequestedDict).then(r => {
        let display = document.getElementById('button-div');
        display.innerHTML = "The " + r['requested_card'] + " card is  " + r['card_identity'] + ". </br>" +
            "Who do you want to give this card to?";
        displayWitchPhase2(player_names);
    });
}

function witchSwitch(playerIdDict) {
    GameService.fetchPostResponseFromServer(playerIdDict).then(r => {
        let display = document.getElementById('button-div');
        display.innerHTML = r['response'];
        GameService.addOkButton(display.id);
    });
}

function displayWitchPhase2(playerNames) {

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

