let selectedKeys = [];
document.addEventListener("DOMContentLoaded", function() {

    let seerDict = window.initial_player_dict;

    GameServices.addRoleDescription(seerDict['role-description']);

    let roleDivId = GameService.roleDivId;
    let buttonDivId = 'name-buttons';
    GameServices.addSimpleElement("div", roleDivId, "", buttonDivId);

    let middleCardDivId = 'middle-card-buttons';
    GameServices.addSimpleElement("div", roleDivId, "", middleCardDivId);

    // Add Middle Cards
    let middleCardButtonClasses = ["button", "middle-card"];
    GameServices.addElement("Left", middleCardDivId,"button", middleCardButtonClasses,
        "Left");
    GameServices.addElement("Middle", middleCardDivId,"button", middleCardButtonClasses,
        "Middle");
    GameServices.addElement("Right", middleCardDivId,"button", middleCardButtonClasses,
        "Right");

    document.getElementById("Left").addEventListener("click", function(){
        handleButtonClicked("Left");
    });
    document.getElementById("Middle").addEventListener("click",function(){
        handleButtonClicked("Middle");
    });
    document.getElementById("Right").addEventListener("click",function(){
        handleButtonClicked("Right");
    });

    // Add submit button
    let formId = "submit-form";
    let submitFormButtonId = "form-submit-button";
    GameServices.addElement(formId, buttonDivId, "form",[],"",
        ["method", "post"]);
    GameServices.addElement(submitFormButtonId, formId, "button",["button"],
        "See Card(s)",["type","submit"]);
    document.getElementById(submitFormButtonId).addEventListener("click", function(){
        event.preventDefault();

        if (selectedKeys.length !== 0) {
            let is_middle_card = (selectedKeys[0] === 'Left' ||
                selectedKeys[0] === 'Middle' ||
                selectedKeys[0] === 'Right');
            if(selectedKeys.length === 1 && is_middle_card){

            } else {
                makeRequest(selectedKeys);
            }
        }
    });

    // Add Player Name Buttons
    let buttonClasses = ['button', 'not-selected'];
    for (let key in seerDict['names']) {
        GameServices.addElement(key, buttonDivId, "button",
            buttonClasses, seerDict['names'][key]['name']);
        document.getElementById(key).addEventListener("click", function () {
            handleButtonClicked(key);
        });
    }
});

function makeRequest(key_array) {
    let d = {'player_id': null,
        'middle_card_1': null,
        'middle_card_2': null,
    };

    if (key_array.length === 1) {
        d = {'player_id': key_array[0].toString()}
    } else if (key_array.length === 2) {
        d = {'middle_card_1': key_array[0].toString(),
                'middle_card_2': key_array[1].toString(),}
    }

    GameService.fetchPostResponseFromServer(d).then(r => {
        let display = document.getElementById(GameService.roleDivId);
        display.innerHTML = r['response'];
        GameService.addOkButton(GameService.roleDivId);
    });
}

function handleButtonClicked(key) {
    /*
        Player can see 2 of the middle cards, or 1 of the player cards.
        As the player selects cards, this function handles keeping track of which are selected,
        automatically deselecting the older choices.
     */

    let seeable = false;
    let is_middle_card = (key === 'Left' || key === 'Middle' || key === 'Right');
    let element = document.getElementById(key);

    if (selectedKeys.indexOf(key) >= 0) {
        // Deselecting: The button is already selected
        element.classList.remove('selected');
        element.classList.add('not-selected');

        let remove = selectedKeys.indexOf(key);
        if (remove === 1) {
            selectedKeys.pop();
        } else if (selectedKeys.length === 2){
            selectedKeys[0] = selectedKeys[1];
            selectedKeys.pop();
        } else {
            selectedKeys.pop();
        }
    } else if (selectedKeys.length === 0) {
        element.classList.remove('not-selected');
        element.classList.add('selected');
        selectedKeys.push(key)
    } else if (!is_middle_card) {
        // if not a middle card, then erase all of selected keys
        element.classList.remove('not-selected');
        element.classList.add('selected');

        for (let i = 0; i < selectedKeys.length; i++) {
            let k = selectedKeys[i]
            document.getElementById(k).classList.remove('selected');
            document.getElementById(k).classList.add('not-selected');
        }
        selectedKeys = [key]
    } else if (selectedKeys.length === 1 && is_middle_card && (selectedKeys[0] === 'Left' || selectedKeys[0] === 'Middle' || selectedKeys[0] === 'Right' )){
        element.classList.remove('not-selected');
        element.classList.add('selected');

        selectedKeys.push(key)
    } else if (selectedKeys.length === 2 && is_middle_card) {
        element.classList.remove('not-selected');
        element.classList.add('selected');

        document.getElementById(selectedKeys[0]).classList.remove('selected');
        document.getElementById(selectedKeys[0]).classList.add('not-selected');

        selectedKeys[0] = selectedKeys[1];
        selectedKeys[1] = key;
    } else {
        element.classList.remove('not-selected');
        element.classList.add('selected');

        document.getElementById(selectedKeys[0]).classList.remove('selected');
        document.getElementById(selectedKeys[0]).classList.add('not-selected');
        selectedKeys[0] = key;
    }

    seeable =(!is_middle_card || selectedKeys.length === 2);

    document.getElementById('form-submit-button').disabled = !seeable
}
