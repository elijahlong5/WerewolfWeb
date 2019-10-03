/*
    Displays the players in the lobby excluding themselves.
 */

document.addEventListener("DOMContentLoaded", function() {
    // set variables
    const access_token_location_in_pathname = 2;
    const player_id_location_in_pathname = 4;

    const access_token = window.location.pathname.split('/')[access_token_location_in_pathname];
    let player_id = null;
    try {
        player_id = window.location.pathname.split('/')[player_id_location_in_pathname];
    }
    catch(e) {
        console.log('no player id');
    }


    let meta_elem = document.getElementById('initial-player-dict');

    let player_names_json = meta_elem.getAttribute('data-names');
    newstr = JSON.stringify(player_names_json)
    let x = 0;
    while (newstr.search("'") && x < 40) {
        newstr = newstr.replace("'",'"');
        x ++;
    }
    newstr= newstr.substr(1, newstr.length - 2)
    let player_names = JSON.parse(newstr);


    let button_div_name = 'name-buttons';
    add_structure_div('role-div', button_div_name);

    let selected_count = 0;

    add_structure_div('role-div', 'submit-div');
    add_form_button('submit-div','form-submit-button');
    document.getElementById('form-submit-button').addEventListener("click", function () {
        if (selected_count != 2) {
            document.getElementById('form-submit-button').innerText = "Choose 2 players before clicking."
        }
    });
    let first_selected = null;
    let second_selected  = null;

    for (let key in player_names['names']) {
        // name elements are toggleable between selected and not.
        let name = player_names['names'][key]['name'];
        const name_element = document.createElement('button');
        name_element.innerText = name;
        name_element.id = key;
        name_element.classList.add("button");
        name_element.classList.add("not-selected");
        document.getElementById(button_div_name).appendChild(name_element);
        document.getElementById(key).addEventListener("click", function () {
            // toggles selected class
            let element = document.getElementById(key);
            // TODO: when someone clicks a non selected button, it selects it, and
            //  deselects the on that has been selected the longest



            // Deselect if already selected
            if (element.classList.contains('selected')) {
                // Deselect
                element.classList.remove('selected');
                element.classList.add('not-selected');
                selected_count --;

                if (first_selected === key && selected_count === 0) {
                    first_selected = null;
                } else if (first_selected === key && selected_count === 1) {
                    first_selected = second_selected;
                    second_selected = null;
                }
            } else if (selected_count === 0) {
                // select: case: none are selected
                element.classList.remove('not-selected');
                element.classList.add('selected');
                selected_count ++;
                first_selected = key;
            } else if (selected_count === 1) {
                // select: case: 1 is selected
                element.classList.remove('not-selected');
                element.classList.add('selected');
                selected_count ++;
                second_selected = key;
            } else if (selected_count === 2) {
                // select: case: 2 are already selected
                element.classList.remove('not-selected');
                element.classList.add('selected');

                document.getElementById(first_selected).classList.remove('selected');
                document.getElementById(first_selected).classList.add('not-selected');

                first_selected = second_selected;
                second_selected = key;
            }

            // if (element.classList.contains('selected')) {
            //     // Deselect
            //     element.classList.remove('selected');
            //     element.classList.add('not-selected');
            //     selected_count --;
            // } else if (selected_count < 2 && element.classList.contains('not-selected')){
            //     // Select
            //
            //
            //     element.classList.remove('not-selected');
            //     element.classList.add('selected');
            //     selected_count ++;
            // }

            document.getElementById('form-submit-button').disabled = (selected_count !== 2)

        });
    }

});

function add_form_button(div_name, button_id) {

    let form =document.createElement('form');
    form.setAttribute('method',"post");

    let button = document.createElement('button');
    button.setAttribute('Type', "submit");
    button.classList.add('button');
    button.id = button_id
    button.innerText = "Troublemake!";

    button.disabled = true;

    form.appendChild(button);

    document.getElementById(div_name).appendChild(form)
    //form.setAttribute('action',
    // "/api/lobbies/ACCESS_TOKEN/players/PLAYER_ID/PLAYER_RESPONSE");
}



function add_structure_div(parent_node, id) {
    const elem = document.createElement('div');
    elem.id = id;
    document.getElementById(parent_node).appendChild(elem);
}


