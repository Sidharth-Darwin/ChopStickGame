from collections.abc import Sequence
from typing import Self, Optional
from base_components import ChopStickGame, Player


class TermninalPlayer(Player):
    def __init__(self, display_evaluation_message: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_evaluation_message = display_evaluation_message
    
    def exit_game(self, players_list: Sequence[Self], message="") -> None:
        if self.verbose:
            if message:
                print(message)
            else:
                print(f"{self.name} has left the game!")
        if self in players_list:
            players_list.remove(self)

    def display_evaluation(self, opponent: Player, my_hand_action: int, opponent_hand: int, opponents: Sequence[Player]) -> None:
        if not self.display_evaluation_message:
            return
        evaluation, message_str = self.evaluate_move_verbose(opponent, my_hand_action, opponent_hand, opponents)
        print(f"{self.name} evaluation is {evaluation}\n{message_str}")


class TerminalChopStickGame(ChopStickGame):
    def __init__(self, players: Sequence[Player], verbose: bool = True, *args, **kwargs):
        super().__init__(players, *args, **kwargs)
        self.verbose = verbose

    def display_game(self, current_player: Optional[Player] = None, opponent_player: Optional[Player] = None) -> None:
        if not self.verbose:
            return
        print("-" * 47)
        print("|    Player Name     | Left Hand | Right Hand |")
        for player in self.players:
            print(player, end="")
            if player == current_player:
                print(" (Attacked by)")
            elif player == opponent_player:
                print(" (Attacked on)")
            else:
                print()
        print("-" * 47)