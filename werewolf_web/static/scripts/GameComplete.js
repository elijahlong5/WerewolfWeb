document.addEventListener("DOMContentLoaded", function() {
    let gameCompleteDict = window.gameCompleteDict;
    console.log(gameCompleteDict);

    const players = gameCompleteDict['game_state']['players'];
    const diedIds = gameCompleteDict['died_list_id'];
    console.log('players:',players);
    for (let p in players) {
        if (diedIds.includes(Number(p))) {
            GameServices.addElement(p,'game-complete',"li",[],players[p]['name'] + ' died',);
            console.log(players[p]['name'] + ' died');
        }
        console.log('id is', p,"and diedIds is",diedIds)
        if (Number(p) in diedIds) {
            console.log(players[p]['name'] + ' (number) died');
        }

        console.log(players[p]['name']);
    }

    // for (let id in diedIds) {
    //     console.log(typeof id)
    //     console.log('id in player')
    //     console.log(id in Object.keys(players))
    //     if (id in Object.keys(players)) {
    //         console.log('aqui');
    //         let x = document.getElementById("game-complete");
    //
    //         for ( let p in players){
    //             console.log('p is', p);
    //             console.log(typeof p);
    //             if (p === id) {
    //                 console.log('alike')
    //             }
    //         }
    //         // x.innerText = players[id]['name'] + " died";
    //         // console.log(players[id])
    //     }
    // }
});