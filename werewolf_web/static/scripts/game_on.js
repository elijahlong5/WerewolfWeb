let timeBetweenRefreshesGAMEON = 2000;
const access_token = GameService.getAccessTokenFromUrl();
document.addEventListener("DOMContentLoaded", function() {
    redirectRefresh();
});

function redirectRefresh() {
    console.log('refreshing');
    setTimeout(redirectRefresh, timeBetweenRefreshesGAMEON);
    redirectIfDiscussionPhase();
}

async function redirectIfDiscussionPhase() {
    const response = await fetch('/api/lobbies/' + access_token + '/discussion/');
    const is_discussion = await response.json();
    console.log(is_discussion);
    console.log('checking discussion: ' + is_discussion['discussion'] );
    if (is_discussion['discussion']){
        console.log("game is on, redirecting to game on page.");
        const player_id_location_in_pathname = 4;
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[player_id_location_in_pathname];
        }
        catch(e) {
            console.log('no player id');
        }
        if (player_id === null) {
            window.location.href = '/discussion/' + access_token + '/';

        } else {
            window.location.href = '/discussion/' + access_token + '/player_id/' + player_id + '/';
        }
    }
}
