from Game import WerewolfGame

my_game = WerewolfGame()

# -------- Open game lobby ---------
# Here the host can add and remove Characters
# Here there is a listener waiting for players to join the lobby.
# They are issued an ID with which they can communicate with the hosting device.

my_game.add_player("Jackie")
my_game.add_player("Jilliam")
my_game.add_player("Snoopy")
my_game.add_player("Tonya")
my_game.add_player("Taek")
my_game.add_player("Sam")

# When the host chooses "Start Game", the real fun begins.
my_game.start_game()

