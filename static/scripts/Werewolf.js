/*
    This displays the identities of the other werewolves (retrieved from the game logic)
    If there are no other werewolves, the player must choose one card from the middle.

 */

time_between_refreshes = 2000
let player_dict = {}
async function request_werewolf_info_dict() {
    const access_token_location_in_pathname = 2
    const player_id_location_in_pathname = 4

    const access_token = window.location.pathname.split('/')[access_token_location_in_pathname]
    let player_id = null
    try {
        player_id = window.location.pathname.split('/')[player_id_location_in_pathname]
    }
    catch(e) {
        console.log('no player id')
    }
    // adds new player li elements if there are new players in the lobby
    const response = await fetch('/api/lobbies/'
        + access_token
        + '/players/'
        + player_id
        + '/player_specific_dict/')

    const responsePlayersDict = await response.json()
    player_dict = responsePlayersDict
}

request_werewolf_info_dict().then(r => {
    // once dict is returned...
    console.log('dictionary returned')
    console.log(player_dict)

})

document.addEventListener("DOMContentLoaded", function() {
    refresh()
})