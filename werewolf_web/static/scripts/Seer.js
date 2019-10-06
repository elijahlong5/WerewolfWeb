let selected_keys = []
document.addEventListener("DOMContentLoaded", function() {
    // set variables
    const access_token_location_in_pathname = 2;
    const player_id_location_in_pathname = 4;

    const access_token = window.location.pathname.split('/')[access_token_location_in_pathname];
    let player_id = null;
    try {
        player_id = window.location.pathname.split('/')[player_id_location_in_pathname];
    } catch (e) {
        console.log('no player id');
    }


    let meta_elem = document.getElementById('initial-player-dict');

    let player_names_json = meta_elem.getAttribute('data-names');
    newstr = JSON.stringify(player_names_json);
    let x = 0;
    while (newstr.search("'") && x < 40) {
        newstr = newstr.replace("'", '"');
        x++;
    }
    newstr = newstr.substr(1, newstr.length - 2)
    let player_names = JSON.parse(newstr);

    let button_div_name = 'name-buttons';
    add_structure_div('role-div', button_div_name);

    let middle_card_div = 'middle-card-buttons';
    add_structure_div('role-div', middle_card_div);



    // ADD MIDDLE CARDS
    const left_card = document.createElement('button');
    left_card.innerText = "Left";
    left_card.classList.add("button");
    left_card.classList.add("middle-card");
    left_card.id = left_card.innerText;
    document.getElementById(middle_card_div).appendChild(left_card);
    document.getElementById(left_card.id).addEventListener("click", function(){
        handle_button_clicked(left_card.id);
    });


    const middle_card = document.createElement('button');
    middle_card.innerText = "Middle";
    middle_card.classList.add("button");
    middle_card.classList.add("middle-card");
    middle_card.id = middle_card.innerText;
    document.getElementById(middle_card_div).appendChild(middle_card);
    document.getElementById(middle_card.id).addEventListener("click", function(){
        handle_button_clicked(middle_card.id);
    });


    const right_card = document.createElement('button');
    right_card.innerText = "Right";
    right_card.classList.add("button");
    right_card.classList.add("middle-card");
    right_card.id = right_card.innerText;
    document.getElementById(middle_card_div).appendChild(right_card);
    document.getElementById(right_card.id).addEventListener("click", function(){
        handle_button_clicked(right_card.id);
    });

    add_structure_div('role-div', 'submit-div');
    add_form_button('submit-div','form-submit-button','See Card(s)!');
    document.getElementById('form-submit-button').addEventListener("click", function () {
        make_request(selected_keys);
    });

    // ADD PLAYER NAME BUTTONS
    for (let key in player_names['names']) {
        add_element(button_div_name, key,
            'button',
            player_names['names'][key]['name'],
            ['button', 'not-selected']);
        document.getElementById(key).addEventListener("click", function () {
            handle_button_clicked(key);
        });
    }
});

function make_request(key_array) {
    d = {'player_id': null,
        'middle_card_1': null,
        'middle_card_2': null,
    };

    if (key_array.length === 1) {
        d = {'player_id': key_array[0].toString()}
    } else if (key_array.length === 2) {
        d = {'middle_card_1': key_array[0].toString(),
                'middle_card_2': key_array[1].toString(),}
    }
    json_str_dict = JSON.stringify(d);
    request_middle_card_identity(json_str_dict).then(r => {
        console.log(game_response)
    });
}

async function request_middle_card_identity(player_response) {
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
        + player_response
        +'/');

    const card_identity = await response.json();
    // TODO: why isn't this variable below referenced if i insert var?
    game_response = card_identity;
}

function handle_button_clicked(key) {
    let seeable = false;

    let is_middle_card = (key === 'Left' || key === 'Middle' || key === 'Right');

    let element = document.getElementById(key);

    if (selected_keys.indexOf(key) >= 0) {
        element.classList.remove('selected');
        element.classList.add('not-selected');

        remove = selected_keys.indexOf(key)
        if (remove === 1) {
            selected_keys.pop()
        } else if (selected_keys.length === 2){
            selected_keys[0] = selected_keys[1]
            selected_keys.pop()
        } else {
            selected_keys.pop()
        }
    } else if (selected_keys.length === 0) {
        element.classList.remove('not-selected');
        element.classList.add('selected');
        selected_keys.push(key)
    } else if (!is_middle_card) {
        // if not a middle card, then erase all of selected keys
        element.classList.remove('not-selected');
        element.classList.add('selected');

        for (var i = 0; i < selected_keys.length; i++) {
            let k = selected_keys[i]
            document.getElementById(k).classList.remove('selected');
            document.getElementById(k).classList.add('not-selected');
        }
        selected_keys = [key]
    } else if (selected_keys.length === 1 && is_middle_card && (selected_keys[0] === 'Left' || selected_keys[0] === 'Middle' || selected_keys[0] === 'Right' )){
        element.classList.remove('not-selected');
        element.classList.add('selected');

        selected_keys.push(key)
    } else if (selected_keys.length === 2 && is_middle_card) {
        element.classList.remove('not-selected');
        element.classList.add('selected');

        document.getElementById(selected_keys[0]).classList.remove('selected');
        document.getElementById(selected_keys[0]).classList.add('not-selected');

        selected_keys[0] = selected_keys[1];
        selected_keys[1] = key;
    } else {
        element.classList.remove('not-selected');
        element.classList.add('selected');

        document.getElementById(selected_keys[0]).classList.remove('selected');
        document.getElementById(selected_keys[0]).classList.add('not-selected');
        selected_keys[0] = key;
    }


    seeable =(!is_middle_card || selected_keys.length === 2);



    document.getElementById('form-submit-button').disabled = !seeable
}

function add_element(parent_node, id, element_type, inner_text=null, classes=null) {
    // used in robber, seer and troublemaker classes.
    let element = document.createElement(element_type);
    element.id = id;
    if (inner_text) { element.innerText = inner_text;}
    if (classes !== null) {
        for (let i = 0; i < classes.length; i++){
            element.classList.add(classes[i]);
        }
    }
    document.getElementById(parent_node).appendChild(element);
}

function add_form_button(div_name, button_id, inner_text) {
    // let form =document.createElement('form');
    // form.setAttribute('method',"post");

    let button = document.createElement('button');
    // button.setAttribute('Type', "submit");
    button.classList.add('button');
    button.id = button_id
    button.innerText = inner_text;
    button.disabled = true;

    //form.appendChild(button);

    document.getElementById(div_name).appendChild(button)
}

function add_structure_div(parent_node, id) {
    const elem = document.createElement('div');
    elem.id = id;
    document.getElementById(parent_node).appendChild(elem);
}