/*
    Displays the players in the lobby excluding themselves.
 */
document.addEventListener("DOMContentLoaded", function() {
    let troublemakerDict = window.initial_player_dict;
    GameServices.addRoleDescription(troublemakerDict['role-description']);


    let buttonDivName = 'name-buttons';
    GameServices.addSimpleElement("div",GameService.roleDivId, "", buttonDivName);

    let selectedCount = 0;

    let firstSelected = null;
    let secondSelected  = null;

    for (let key in troublemakerDict['names']) {
        // name elements are toggleable between selected and not.
        GameServices.addElement(key, buttonDivName, "button",
            ['button', 'not-selected'],
            troublemakerDict['names'][key]['name']
            );


        document.getElementById(key).addEventListener("click", function () {
            // toggles selected class
            let element = document.getElementById(key);
            // Deselect if already selected
            if (element.classList.contains('selected')) {
                // Deselect
                element.classList.remove('selected');
                element.classList.add('not-selected');
                selectedCount --;
                if (firstSelected === key && selectedCount === 0) {
                    firstSelected = null;
                } else if (firstSelected === key && selectedCount === 1) {
                    firstSelected = secondSelected;
                    secondSelected = null;
                }
            } else if (selectedCount === 0) {
                // select: case: none are selected
                element.classList.remove('not-selected');
                element.classList.add('selected');
                selectedCount ++;
                firstSelected = key;
            } else if (selectedCount === 1) {
                // select: case: 1 is selected
                element.classList.remove('not-selected');
                element.classList.add('selected');
                selectedCount ++;
                secondSelected = key;
            } else if (selectedCount === 2) {
                // select: case: 2 are already selected
                element.classList.remove('not-selected');
                element.classList.add('selected');

                document.getElementById(firstSelected).classList.remove('selected');
                document.getElementById(firstSelected).classList.add('not-selected');

                firstSelected = secondSelected;
                secondSelected = key;
            }
            document.getElementById(submitFormButtonId).disabled = (selectedCount !== 2)
        });
    }
    let formId = "submit-form";
    let submitFormButtonId = "form-submit-button";
    GameServices.addElement(formId, buttonDivName, "form",[],"",
        ["method", "post"]);
    GameServices.addElement(submitFormButtonId, formId, "button",["button"],
        "Troublemake!",["type","submit"]);
    document.getElementById(submitFormButtonId).addEventListener("click", function(){
        event.preventDefault();
        troublemake({"playerId_1": firstSelected, "playerId_2": secondSelected});
    });
});

function troublemake(swapCardsDict) {
    GameService.fetchPostResponseFromServer(swapCardsDict).then(r => {
        let display = document.getElementById(GameService.roleDivId);
        display.innerHTML = r['response'];
    });
}
