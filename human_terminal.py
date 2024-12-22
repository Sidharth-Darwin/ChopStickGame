from collections.abc import Sequence
from typing import Self
from base_components import Player
from terminal_components import TerminalChopStickGame, TermninalPlayer

NON_ACTION_MOVE = 3

class HumanTerminalPlayer(TermninalPlayer):
    def __init__(self, name="", display_evaluation_message: bool = False):
        super().__init__()
        self.display_evaluation_message = display_evaluation_message
        if name:
            self.name = name

    def play(self, opponents: Sequence[Player]) -> Player:
        if len(opponents) > 1:
            opponent_string = ",".join([f'{i} for {opponent.name}' for i, opponent in enumerate(opponents)])
            opponent_player = int(input(f"{self.name}, please choose an opponent ({opponent_string}): "))
        else:
            opponent_player = 0
        opponent_player = opponents[opponent_player]
        my_possible_actions = self.possible_actions()
        action_string = ",".join([f'{i} for {self.actions[i]}' for i in my_possible_actions])
        my_hand_action = NON_ACTION_MOVE
        while my_hand_action not in my_possible_actions:
            my_hand_action = int(input(f"{self.name}, please choose which hand to play ({action_string}): "))
        opponent_possible_actions = opponent_player.possible_actions()
        if 2 in opponent_possible_actions:
            opponent_possible_actions.remove(2)
        action_string = ",".join([f'{i} for {opponent_player.actions[i]}' for i in opponent_possible_actions])
        opponent_hand = NON_ACTION_MOVE
        while opponent_hand not in opponent_possible_actions:
            opponent_hand = int(input(f"{self.name}, please choose which hand to tap ({action_string}): "))
        if self.display_evaluation_message:
            evaluation, message_str = self.evaluate_move_verbose(opponent_player, my_hand_action, opponent_hand, opponents)
            print(f"{self.name} evaluation is {evaluation}\n{message_str}")
        self.make_move(opponent_player, my_hand_action, opponent_hand)
        return opponent_player

    def exit_game(self, players_list: Sequence[Self], message="") -> None:
        if message:
            print(message)
        else:
            print(f"{self.name} has left the game!")
        if self in players_list:
            players_list.remove(self)



if __name__ == "__main__":
    game = TerminalChopStickGame([HumanTerminalPlayer("Sidhu"), HumanTerminalPlayer("Devan"), HumanTerminalPlayer("John")])
    game.play_game()