/*
    This displays the identities of the other werewolves (retrieved from the game logic)
    If there are no other werewolves, the player must choose one card from the middle.
 */
document.addEventListener("DOMContentLoaded", function() {

    // Display who the other werewolves are, or the 3 middle cards.
    let playerDict = window.initial_player_dict;

    let buttonDivName = 'role-div';

    if (playerDict['lone_wolf'] === false) {
        GameServices.addSimpleElement("h2", buttonDivName, "Here are the other werewolves.")
        for (let key in playerDict['fellow_wolves']) {
            let nrText = playerDict['fellow_wolves'][key];
            GameServices.addSimpleElement("li", buttonDivName, nrText);
        }
        GameService.addOkButton(buttonDivName);
    } else {

        let buttonFormId = "button-form";
        GameServices.addSimpleElement('h2', buttonDivName, "You're the lone wolf");
        GameServices.addElement(buttonFormId, buttonDivName, "form",[],"",
            ["method", "post"]);
        GameServices.addElement("Left", buttonFormId,"button", ["button"],
            "Left", ["type", "submit"]);
        GameServices.addElement("Middle", buttonFormId,"button",["button"],
            "Middle", ["type", "submit"]);
        GameServices.addElement("Right", buttonFormId,"button",["button"],
            "Right", ["type", "submit"]);

        document.getElementById("Left").addEventListener("click", function(){
            makeRequest("Left");
        });
        document.getElementById("Middle").addEventListener("click",function(){
            makeRequest("Middle");
        });
        document.getElementById("Right").addEventListener("click",function(){
            makeRequest("Right");
        });
    }
});

function makeRequest(cardRequested) {
    let cardRequestedDict = {"card": cardRequested};
    GameService.fetchPostResponseFromServer(cardRequestedDict).then(r => {
        let display = document.getElementById('role-div');
        display.innerHTML = "The " + r['requested_card'] + " card is: " + r['card_identity'];
    });
}
