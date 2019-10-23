document.addEventListener("DOMContentLoaded", function() {
    let element = document.createElement('h2');
    element.innerText = 'You are the Tanner.  You win if you die.';

    document.getElementById('role-div').appendChild(element);
    GameService.addOkButton('role-div');
});