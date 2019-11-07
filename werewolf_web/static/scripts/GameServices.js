class GameServices{

    middleCardDivId = "middle-card-buttons";
    middleCardButtonClasses = ["button", "middle-card"];
    constructor(){
        this.accessTokenLocationInPathname = 2;
        this.playerIdLocationInPathname = 4;

        this.timeBetweenRefreshes = 2000;
        this.roleDescriptionId = "role-header";
        this.roleDivId = "role-div";
        this.acknowledgedDict = {"status": "acknowledged"};
        this.notifyFormId = "notify-form";

        this.validStartPointVar = "valid-starting-point"; // Matches class name in lobby style page.
    }

    // Adding elements to the page
    static addSimpleElement(nodeType, parentNode, innerText, elementId=null) {
        const elem = document.createElement(nodeType);
        elem.innerText = innerText;
        if (elementId) {
            elem.id = elementId;
        }
        document.getElementById(parentNode).appendChild(elem);
    }

    static addElement(elementId, parentNode, nodeType, classes=[], text=elementId, attributes=[], required=false) {
        const element = document.createElement(nodeType);

        element.id = elementId;
        element.innerText = text;
        for (let i = 0; i < classes.length; i++) {
            element.classList.add(classes[i]);
        }
        for (let i = 0; i < attributes.length; i += 2){
            element.setAttribute(attributes[i], attributes[i+1]);
        }
        if (required) {
            element.required = true;
        }

        document.getElementById(parentNode).appendChild(element);
    }

    static addRoleDescription(description) {
        GameServices.addSimpleElement("h4", GameService.roleDescriptionId,
            description);
    }

    addMiddleCardButtons(  middleCardClickedFunction, attributes=[]) {
        let middleCardDivId = this.middleCardDivId;
        let middleCardButtonClasses = this.middleCardButtonClasses;
        GameServices.addElement("Left", middleCardDivId,"button", middleCardButtonClasses,
            "Left", attributes);
        GameServices.addElement("Middle",middleCardDivId,"button", middleCardButtonClasses,
            "Middle", attributes);
        GameServices.addElement("Right", middleCardDivId,"button", middleCardButtonClasses,
            "Right", attributes);

        document.getElementById("Left").addEventListener("click", function(){
            middleCardClickedFunction("Left");
        });
        document.getElementById("Middle").addEventListener("click",function(){
            middleCardClickedFunction("Middle");
        });
        document.getElementById("Right").addEventListener("click",function(){
            middleCardClickedFunction("Right");
        });
    }


    addOkButton(parentNodeId) {
        let formId = this.notifyFormId;
        let submitFormButtonId = "form-submit-button";
        GameServices.addElement(formId, parentNodeId, "form",[],"",
            ["method", "post"]);
        GameServices.addElement(submitFormButtonId, formId, "button",["button"],
            "ok!",["type","submit"]);
        document.getElementById(submitFormButtonId).addEventListener("click", function(){
            event.preventDefault();
            GameService.notifyServer(GameService.acknowledgedDict);
        });
    }

    // Helper functions for posting and fetching from the server.
    generatePostUrlForInitialDict(){
        let player_id = null;
        try {
            player_id = window.location.pathname.split('/')[this.playerIdLocationInPathname];
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
        const access_token = window.location.pathname.split('/')[this.accessTokenLocationInPathname];
        let url = '/api/lobbies/'
            + access_token
            + "/";
        return url
    }

    getAccessTokenFromUrl() {
        return window.location.pathname.split('/')[this.accessTokenLocationInPathname];
    }

    getPlayerIdFromUrl() {
        return window.location.pathname.split('/')[this.playerIdLocationInPathname];
    }

    notifyServer(notificationDict) {
        // Notify server that client has viewed the information,
        // and hide the form.
        this.fetchPostResponseFromServer(notificationDict).then(r => {
            console.log(r);
            document.getElementById(this.notifyFormId).innerHTML = "";
        });
    }

    async fetchPostResponseFromServer(serverRequestDict, url=this.generatePostUrlForInitialDict()) {
        try{
            event.preventDefault();
        }
        catch {
        }
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

const GameService = new GameServices();
const access_token = GameService.getAccessTokenFromUrl();
