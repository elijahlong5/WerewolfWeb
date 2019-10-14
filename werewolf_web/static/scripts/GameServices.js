class GameServices{
    constructor(){
        this.access_token_location_in_pathname = 2;
        this.player_id_location_in_pathname = 4;

    }

    addSimpleElement(nodeType, parentNode, innerText, elementId=null) {
        const elem = document.createElement(nodeType);
        elem.innerText = innerText;
        if (elementId) {
            elem.id = elementId;
        }
        document.getElementById(parentNode).appendChild(elem);
    }

    addElement(elementId, parentNode, nodeType, classes=[], text=elementId, attributes=[]) {
        const element = document.createElement(nodeType);

        element.id = elementId;
        element.innerText = text;
        for (let i = 0; i < classes.length; i++) {
            element.classList.add(classes[i]);
        }
        for (let i = 0; i < attributes.length; i += 2){
            element.setAttribute(attributes[i], attributes[i+1]);
        }
        document.getElementById(parentNode).appendChild(element);
    }

    generatePostUrlForInitialDict(){
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[this.player_id_location_in_pathname];
        }
        catch(e) {
            console.log('no player id');
        }
        let url = this.generateLobbyPostUrl()
            +'players/'
            + player_id
            + '/';
        return url
    }

    generateLobbyPostUrl () {
        const access_token = window.location.pathname.split('/')[this.access_token_location_in_pathname];
        let url = '/api/lobbies/'
            + access_token
            + "/";
        return url
    }

    getAccessTokenFromUrl() {
        return window.location.pathname.split('/')[this.access_token_location_in_pathname];
    }

    getPlayerIdFromUrl() {
        return window.location.pathname.split('/')[this.player_id_location_in_pathname];

    }

    async fetchPostResponseFromServer(serverRequestDict, url=this.generatePostUrlForInitialDict()) {
        event.preventDefault();

        let data = serverRequestDict;

        const response = await fetch(url,{
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
                'Content-Type': 'application/json'
            },
            redirect: 'follow',
            referrer: 'no-referrer',
            body: JSON.stringify(data)
        });

        const responseDict = await response.json();
        let gameResponse = responseDict;
        return gameResponse;
    }
}
