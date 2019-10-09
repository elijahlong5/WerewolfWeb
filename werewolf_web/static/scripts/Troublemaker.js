/*
    Displays the players in the lobby excluding themselves.
 */
let GameService = new GameServices();

document.addEventListener("DOMContentLoaded", function() {
    let playerDict = window.initial_player_dict;

    let buttonDivName = 'name-buttons';
    GameService.addSimpleElement("div",'role-div', "", buttonDivName);

    let selectedCount = 0;

    let firstSelected = null;
    let secondSelected  = null;

    for (let key in playerDict['names']) {
        // name elements are toggleable between selected and not.
        GameService.addElement(key, buttonDivName, "button",
            ['button', 'not-selected'],
            playerDict['names'][key]['name']
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
    GameService.addElement(formId, buttonDivName, "form",[],"",
        ["method", "post"]);
    GameService.addElement(submitFormButtonId, formId, "button",["button"],
        "Troublemake!",["type","submit"]);
    document.getElementById(submitFormButtonId).addEventListener("click", function(){
        event.preventDefault();
        troublemake({"playerId_1": firstSelected, "playerId_2": secondSelected});
    });
});

function troublemake(swapCardsDict) {
    GameService.fetchPostResponseFromServer(swapCardsDict).then(r => {
        let display = document.getElementById('role-div');
        display.innerHTML = r['response'];
    });
}
