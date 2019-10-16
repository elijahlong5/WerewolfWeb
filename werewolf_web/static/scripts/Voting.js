let timeBetweenRefreshesVOTING = 2000;

let GameService = new GameServices();
const access_token = GameService.getAccessTokenFromUrl();
document.addEventListener("DOMContentLoaded", function() {
    let votingDict = window.votingDict;

    let selectedId = null; // Who they are voting for.

    let countDownDate = new Date(votingDict['exp_time']).getTime();
    // Update the count down every 1 second
    let x = setInterval(function() {
        // Get today's date and time
        let now = new Date().getTime();
        // Find the distance between now and the count down date
        let distance = countDownDate - now;

        // Time calculations for minutes and seconds
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Output the result in an element with id="demo"
        document.getElementById("countdown").innerHTML = minutes + "m " + seconds + "s ";

        // If the count down is over, write some text
        if (distance < 0) {
            clearInterval(x);
            castVote(selectedId, playerId);
            document.getElementById("countdown").innerHTML = "TIME EXPIRED";
        }
    }, 1000);


    let buttonDivName = 'name-buttons';
    GameService.addSimpleElement("div",'vote-ballet', "", buttonDivName);

    let playerId = GameService.getPlayerIdFromUrl();

    for (let key in votingDict['players']['names']) {
        console.log('key', key, "playerid:", playerId);

        GameService.addElement(key, buttonDivName, "button",
            ['button', 'not-selected'],
            votingDict['players']['names'][key]['name']
        );
        document.getElementById(key).addEventListener("click", function () {
            // toggles selected class
            let element = document.getElementById(key);
            // Deselect if already selected
            if (element.classList.contains('selected')) {
                // Deselect
                element.classList.remove('selected');
                element.classList.add('not-selected');
                selectedId = null;
            } else if (selectedId === null) {
                // select: case: none are selected
                element.classList.remove('not-selected');
                element.classList.add('selected');
                selectedId = key;
            } else if (selectedId !== null) {
                element.classList.remove('not-selected');
                element.classList.add('selected');
                let oldSelected = document.getElementById(selectedId);
                selectedId = key;
                oldSelected.classList.remove('selected');
                oldSelected.classList.add('not-selected');
            }
            document.getElementById(submitFormButtonId).disabled = (selectedId === null)
        });


    }
    let formId = "submit-form";
    let submitFormButtonId = "form-submit-button";
    GameService.addElement(formId, buttonDivName, "form",[],"",
        ["method", "post"]);
    GameService.addElement(submitFormButtonId, formId, "button",["button"],
        "Cast Vote!",["type","submit"]);
    document.getElementById(submitFormButtonId).addEventListener("click", function(){
        event.preventDefault();
        castVote(selectedId, playerId);

    });

});

function castVote(voteId, playerId) {
    let voteDict = {
        'vote_for_id': voteId,
    };

    let castVoteUrl = GameService.generateLobbyPostUrl() + 'players/' + playerId + "/cast-vote/";
    GameService.fetchPostResponseFromServer(voteDict, castVoteUrl).then(r => {
        document.getElementById("vote-ballet").innerHTML = "You've voted!" +
            " Wait until the time has run out, or everyone is done voting";
            refreshForGameComplete();
    });
}

function refreshForGameComplete() {
    setTimeout(refreshForGameComplete, timeBetweenRefreshesVOTING);
    redirectIfGameComplete(access_token);
}

async function redirectIfGameComplete(access_token) {
    console.log("refreshing for game complete")
    const response = await fetch('/api/lobbies/' + access_token + '/check-voting-status/');
    const is_still_voting = await response.json();
    console.log(is_still_voting)
    if (!is_still_voting['still-voting']){
        console.log("Everyone has voted! Redirecting to page");
        const player_id_location_in_pathname = 4;
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[player_id_location_in_pathname];
        }
        catch(e) {
            console.log('no player id');
        }
        window.location.href = '/game-complete/' + access_token + '/player_id/' + player_id + '/';
    }
}
