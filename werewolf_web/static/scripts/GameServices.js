class GameServices{
    constructor(){
        this.access_token_location_in_pathname = 2
        this.player_id_location_in_pathname = 4;

    }

    addSimpleElement(elementName, parentNode, innerText, elementId=null) {
        const elem = document.createElement(elementName);
        elem.innerText = innerText;
        if (elementId) {
            elem.id = elementId;
        }
        document.getElementById(parentNode).appendChild(elem);
    }

    addElement(elementId, parentNode, elementType, classes=[], text=elementId) {
        const element = document.createElement(elementType);
        element.id = elementId;
        element.innerText = text;
        for (let i = 0; i < classes.length; i++) {
            element.classList.add(classes[i]);
        }

        document.getElementById(parentNode).appendChild(element);
    }

    addFormButton(buttonId, parentNode, formNodeId, classes, text) {
        // function creates post button that is initially disabled.
        // the classes are assigned to the button.
        this.addSimpleElement("div", parentNode,"", formNodeId);
        let form = document.createElement("form");
        form.setAttribute("method", "post");


        let button = document.createElement("button");
        button.setAttribute("type", "submit");
        button.id = buttonId;
        button.innerText = text;
        button.disabled = true;
        for (let i = 0; i < classes.length; i++) {
            button.classList.add(classes[i]);
        }

        form.appendChild(button);
        document.getElementById(parentNode).appendChild(form);

    }

    async fetchResponseFromServer(playerResponse) {

        const access_token = window.location.pathname.split('/')[this.access_token_location_in_pathname]
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[this.player_id_location_in_pathname]
        }
        catch(e) {
            console.log('no player id');
        }

        const response = await fetch('/api/lobbies/'
            + access_token
            + '/players/'
            + player_id
            + '/'
            + playerResponse
            +'/');

        const responseDict = await response.json();
        let gameResponse = responseDict;
        return gameResponse;
    }

    async fetchPostResponseFromServer(playerResponse) {

        const access_token = window.location.pathname.split('/')[this.access_token_location_in_pathname]
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[this.player_id_location_in_pathname]
        }
        catch(e) {
            console.log('no player id');
        }

        let url = '/api/lobbies/'
            + access_token
            + '/players/'
            + player_id
            + '/';

        let data = playerResponse;

        const response = await fetch(url,{
            method: 'post',
            body: JSON.stringify(data), // data can be `string` or {object}!
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const responseDict = await response.json();
        let gameResponse = responseDict;
        return gameResponse;
    }


}