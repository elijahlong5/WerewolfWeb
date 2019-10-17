document.addEventListener("DOMContentLoaded", function() {
    redirectRefresh();
});

function redirectRefresh() {
    setTimeout(redirectRefresh, GameService.timeBetweenRefreshes);
    redirectIfDiscussionPhase();
}

async function redirectIfDiscussionPhase() {
    const response = await fetch('/api/lobbies/' + access_token + '/discussion/');
    const is_discussion = await response.json();
    if (is_discussion['discussion']){
        let player_id = null;
        try {
            player_id = GameService.getPlayerIdFromUrl();
            window.location.href = '/discussion/' + access_token + '/player_id/' + player_id + '/';
        }
        catch(e) {
            // No player id found.
            window.location.href = '/discussion/' + access_token + '/';
        }
    }
}
