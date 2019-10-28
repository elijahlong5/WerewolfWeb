document.addEventListener("DOMContentLoaded", function() {
    GameServices.addRoleDescription(window.initial_player_dict['role-description']);
    GameService.addOkButton(GameService.roleDivId);
});