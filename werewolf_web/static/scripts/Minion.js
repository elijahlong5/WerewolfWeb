
document.addEventListener("DOMContentLoaded", function() {

    // Display who the other werewolves are, or the 3 middle cards.

    let meta_elem = document.getElementById('initial-player-dict');

    let player_dict = meta_elem.getAttribute('data-names');
    new_str = JSON.stringify(player_dict);
    let x = 0;
    while (new_str.search("'") && x < 40) {
        new_str = new_str.replace("'",'"');
        x ++;
    }
    new_str = new_str.substr(1, new_str.length - 2)
    let werewolf_dict = JSON.parse(new_str);

    add_simple_element('h2', 'role-div', "Werewolves:");
    if (Object.keys(werewolf_dict['wolves']).length === 0){
        add_simple_element("li", 'role-div', "There are NO WEREWOLVES");
    } else {
        for (let key in werewolf_dict['wolves']) {
            let nr_text = werewolf_dict['wolves'][key];
            add_simple_element("li", 'role-div', nr_text);
        }
    }


});

function add_simple_element(el, parent_node, inner_text) {
    const elem = document.createElement(el);
    elem.innerText = inner_text;
    document.getElementById(parent_node).appendChild(elem);
}