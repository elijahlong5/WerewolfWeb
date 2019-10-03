/*
    Displays the players in the lobby excluding themselves.
 */

document.addEventListener("DOMContentLoaded", function() {
    let meta_elem = document.getElementById('initial-player-dict');

    let player_names_json = meta_elem.getAttribute('data-names');
    newstr = JSON.stringify(player_names_json)
    // console.log(JSON.stringify(player_names_json))

    // console.log(newstr)
    let x = 0;
    while (newstr.search("'") && x < 40) {
        newstr = newstr.replace("'",'"');
        x ++;
    }

    // console.log(newstr)
    newstr= newstr.substr(1, newstr.length - 2)
    // console.log(newstr)


    let button_div_name = 'role-div';
    let selected_count = 0;
    let player_names = JSON.parse(newstr)
    console.log('player names')
    console.log(player_names)


    for (let key in player_names['names']) {
        // name elements are toggleable between selected and not.
        let name = player_names['names'][key]['name'];
        console.log(name)
        const name_element = document.createElement('button');
        name_element.innerText = name;
        name_element.id = key;
        name_element.classList.add("Button");
        name_element.classList.add("not-selected");
        document.getElementById(button_div_name).appendChild(name_element);
        document.getElementById(key).addEventListener("click", function () {
            // toggles selected class
            let element = document.getElementById(key);

            if (element.classList.contains('selected')) {
                // Deselect
                element.classList.remove('selected');
                element.classList.add('not-selected');
                selected_count --;
            } else if (selected_count < 2 && element.classList.contains('not-selected')){
                element.classList.remove('not-selected');
                element.classList.add('selected');
                selected_count ++;
                console.log('selected count up 1')
                console.log(selected_count)
            }
        });
    }
});

