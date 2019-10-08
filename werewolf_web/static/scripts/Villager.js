document.addEventListener("DOMContentLoaded", function() {
    let element = document.createElement('h2');
    element.innerText = 'You are the villager.';

    document.getElementById('role-div').appendChild(element)
});