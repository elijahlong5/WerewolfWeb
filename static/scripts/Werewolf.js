/*
    This displays the identities of the other werewolves (retrieved from the game logic)
    If there are no other werewolves, the player must choose one card from the middle.
 */
document.addEventListener("DOMContentLoaded", function() {

    // Display who the other werewolves are, or the 3 middle cards.

    let meta_elem = document.getElementById('initial-player-dict');

    let player_dict = meta_elem.getAttribute('data-names');

    if (player_dict['lone_wolf'] === false) {
        add_simple_element('h2','role-div', "Here are the other werewolves.")
        for (let key in player_dict['fellow_wolves']) {
            let nr_text = player_dict['fellow_wolves'][key];
            add_simple_element("li", 'role-div', nr_text);
        }
    } else {
        add_simple_element('h2', 'role-div', "You're the lone wolf")
        // const button_form = document.createElement('form');
        // button_form.id = 'button-form';
        // //button_form.addEventListener('onClick')

        let button_div_name = 'role-div'

        const left_card = document.createElement('button');
        left_card.innerText = "Left";
        left_card.classList.add("Button");
        left_card.id = left_card.innerText;
        document.getElementById(button_div_name).appendChild(left_card)

        const middle_card = document.createElement('button');
        middle_card.innerText = "Middle";
        middle_card.classList.add("Button");
        middle_card.id = middle_card.innerText;
        document.getElementById(button_div_name).appendChild(middle_card)

        const right_card = document.createElement('button');
        right_card.innerText = "Right";
        right_card.classList.add("Button");
        right_card.id = right_card.innerText;
        document.getElementById(button_div_name).appendChild(right_card)


        document.getElementById("Left").addEventListener("click", function(){
            make_request('left');
        });
        document.getElementById("Middle").addEventListener("click",function(){
            make_request('middle');
        });
        document.getElementById("Right").addEventListener("click",function(){
            make_request('right');
        });


    }
});

function add_simple_element(el, parent_node, inner_text) {
    const elem = document.createElement(el);
    elem.innerText = inner_text;
    document.getElementById(parent_node).appendChild(elem);
}

function make_request(button_id) {
    request_middle_card_identity(button_id).then(r => {
        let display = document.getElementById('role-div');
        display.innerHTML = "The " + button_id + " card is: " + game_response['card'];
    });
}

// When the player chooses a card (left, middle or right). This function
// retrieves the identity of this card.
async function request_middle_card_identity(button_id) {
    const access_token_location_in_pathname = 2;
    const player_id_location_in_pathname = 4;

    const access_token = window.location.pathname.split('/')[access_token_location_in_pathname]
    let player_id = null
    try {
        player_id = window.location.pathname.split('/')[player_id_location_in_pathname]
    }
    catch(e) {
        console.log('no player id');
    }
    // adds new player li elements if there are new players in the lobby
    const response = await fetch('/api/lobbies/'
        + access_token
        + '/players/'
        + player_id
        + '/'
        + button_id
        +'/');

    const card_identity = await response.json();
    // TODO: why isn't this variable below referenced if i insert var?
    game_response = card_identity;
}


// time_between_refreshes = 2000
// let player_dict = {}
// let game_response = {}
// async function request_werewolf_info_dict() {
//     const access_token_location_in_pathname = 2
//     const player_id_location_in_pathname = 4
//
//     const access_token = window.location.pathname.split('/')[access_token_location_in_pathname]
//     let player_id = null
//     try {
//         player_id = window.location.pathname.split('/')[player_id_location_in_pathname]
//     }
//     catch(e) {
//         console.log('no player id')
//     }
//     // adds new player li elements if there are new players in the lobby
//     const response = await fetch('/api/lobbies/'
//         + access_token
//         + '/players/'
//         + player_id
//         + '/player_specific_dict/')
//
//     const responsePlayersDict = await response.json()
//     player_dict = responsePlayersDict
// }

// document.addEventListener("DOMContentLoaded", function() {
//
//     request_werewolf_info_dict().then(r => {
//         // once dict is returned...
//         if (player_dict['lone_wolf'] === false) {
//             add_simple_element('h2','role-div', "Here are the other werewolves.")
//             for (let key in player_dict['fellow_wolves']) {
//                 let nr_text = player_dict['fellow_wolves'][key];
//                 add_simple_element("li", 'role-div', nr_text);
//             }
//         } else {
//             add_simple_element('h2', 'role-div', "You're the lone wolf")
//             // const button_form = document.createElement('form');
//             // button_form.id = 'button-form';
//             // //button_form.addEventListener('onClick')
//
//             let button_div_name = 'role-div'
//
//             const left_card = document.createElement('button');
//             left_card.innerText = "Left";
//             left_card.classList.add("Button");
//             left_card.id = left_card.innerText;
//             document.getElementById(button_div_name).appendChild(left_card)
//
//             const middle_card = document.createElement('button');
//             middle_card.innerText = "Middle";
//             middle_card.classList.add("Button");
//             middle_card.id = middle_card.innerText;
//             document.getElementById(button_div_name).appendChild(middle_card)
//
//             const right_card = document.createElement('button');
//             right_card.innerText = "Right";
//             right_card.classList.add("Button");
//             right_card.id = right_card.innerText;
//             document.getElementById(button_div_name).appendChild(right_card)
//
//
//             document.getElementById("Left").addEventListener("click", function(){
//                 make_request('left');
//             });
//             document.getElementById("Middle").addEventListener("click",function(){
//                 make_request('middle');
//             });
//             document.getElementById("Right").addEventListener("click",function(){
//                 make_request('right');
//             });
//         }
//     });
// });
