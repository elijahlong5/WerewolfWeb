document.addEventListener("DOMContentLoaded", function() {
    let tannerDict = window.initial_player_dict;
    GameServices.addRoleDescription(tannerDict['role-description']);
    GameService.addOkButton(GameService.roleDivId);
});