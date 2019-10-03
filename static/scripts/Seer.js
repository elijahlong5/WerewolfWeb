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
    newstr = JSON.stringify(player_names_json)
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
    add_form_button('submit-div','form-submit-button');
    document.getElementById('form-submit-button').addEventListener("click", function () {
        if (selected_count != 1) {
            document.getElementById('form-submit-button').innerText = "Choose 1 players before clicking."
        }
    });

    // ADD PLAYER NAME BUTTONS
    for (let key in player_names['names']) {
        let name = player_names['names'][key]['name'];
        const name_element = document.createElement('button');
        name_element.innerText = name;
        name_element.id = key;
        name_element.classList.add("button");
        name_element.classList.add("not-selected");
        document.getElementById(button_div_name).appendChild(name_element);
        document.getElementById(key).addEventListener("click", function () {
            handle_button_clicked(key);
        });
    }
});

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

function add_form_button(div_name, button_id) {

    let form =document.createElement('form');
    form.setAttribute('method',"post");

    let button = document.createElement('button');
    button.setAttribute('Type', "submit");
    button.classList.add('button');
    button.id = button_id
    button.innerText = "See card(s)";
    button.disabled = true;

    form.appendChild(button);

    document.getElementById(div_name).appendChild(form)
}



function add_structure_div(parent_node, id) {
    const elem = document.createElement('div');
    elem.id = id;
    document.getElementById(parent_node).appendChild(elem);
}