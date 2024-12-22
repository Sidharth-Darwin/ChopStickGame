from collections.abc import Sequence
from typing import Tuple
import random
from base_components import Player
from terminal_components import TermninalPlayer
from computer_player import ComputerPlayer


class ComputerTerminalPlayer(TermninalPlayer, ComputerPlayer):
    def __init__(self, difficulty_rate: int = 1, abp_depth: int = 5, *args, **kwargs):
        super(ComputerTerminalPlayer, self).__init__(difficulty_rate=difficulty_rate, abp_depth=abp_depth, *args, **kwargs)

    def play(self, opponents: Sequence[Player]) -> Player:
        opponent_player, my_hand_action, opponent_hand = self.get_next_move(opponents)
        self.display_evaluation(opponent_player, my_hand_action, opponent_hand, opponents)
        if my_hand_action == 2 and self.verbose:
            print(f"{self.name} did a split!")
        self.make_move(opponent_player, my_hand_action, opponent_hand)
        if self.verbose:
            print(f"{self.name} tapped {opponent_player.name}'s {opponent_player.actions[opponent_hand]} hand with its {self.actions[my_hand_action]} hand!")
        return opponent_player
    
    def get_next_move(self, opponents: Sequence[Player]) -> Sequence[Player, int, int]:
        if not self.verbose:
            return super().get_next_move(opponents)
        if self.difficulty_rate == 1:
            print(f"Long sighted move by {self.name}")
            return self.long_sighted_move(opponents)
        elif self.difficulty_rate == 0:
            print(f"Short sighted move by {self.name}")
            return self.short_sighted_move(opponents)
        elif self.difficulty_rate == -1:
            print(f"Random move by {self.name}")
            return self.random_move(opponents)
        elif self.difficulty_rate < 0 and self.difficulty_rate > -1:
            prob_value = -self.difficulty_rate
            if random.random() <= prob_value:
                print(f"Random move by {self.name} with probability {prob_value}")
                return self.random_move(opponents)
            else:
                print(f"Short sighted move by {self.name} with probability {1 - prob_value}")
                return self.short_sighted_move(opponents)
        elif self.difficulty_rate > 0 and self.difficulty_rate < 1:
            prob_value = self.difficulty_rate
            if random.random() <= prob_value:
                print(f"Long sighted move by {self.name} with probability {prob_value}")
                return self.long_sighted_move(opponents)
            else:
                print(f"Short sighted move by {self.name} with probability {1 - prob_value}")
                return self.short_sighted_move(opponents)
        else:
            print(f"Random move by {self.name} by default")
            return self.random_move(opponents)

    