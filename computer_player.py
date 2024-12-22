from collections.abc import Sequence
from typing import Tuple
import random
from base_components import Player


    
class ComputerPlayer(Player):
    computer_count = 0

    def __init__(self, difficulty_rate: int = 1, abp_depth: int = 5, *args, **kwargs):
        """Difficulty rate: 
        Can take values between -1 and 1 (inclusive).
        -1 means very easy -> random move
        0 means easy -> short sighted move
        1 means hard -> long sighted move (Not yet implemented: defaults to short sighted move)
        Decimal values in between are allowed. They indicate a probability between the floor and the ceiling values.        
        """
        super().__init__(*args, **kwargs)
        ComputerPlayer.computer_count += 1
        self.name = f"Computer {ComputerPlayer.computer_count}" if kwargs.get("name") is None else kwargs.get("name")
        self.abp_depth = abp_depth
        self.difficulty_rate = difficulty_rate
    
    def get_next_move(self, opponents: Sequence[Player]) -> Sequence[Player, int, int]:
        if self.difficulty_rate == 1:
            return self.long_sighted_move(opponents)
        elif self.difficulty_rate == 0:
            return self.short_sighted_move(opponents)
        elif self.difficulty_rate == -1:
            return self.random_move(opponents)
        elif self.difficulty_rate < 0 and self.difficulty_rate > -1:
            prob_value = -self.difficulty_rate
            if random.random() <= prob_value:
                return self.random_move(opponents)
            else:
                return self.short_sighted_move(opponents)
        elif self.difficulty_rate > 0 and self.difficulty_rate < 1:
            prob_value = self.difficulty_rate
            if random.random() <= prob_value:
                return self.long_sighted_move(opponents)
            else:
                return self.short_sighted_move(opponents)
        else:
            return self.random_move(opponents)
        
    def random_move(self, opponents: Sequence[Player]) -> Sequence[Player, int, int]:
        all_possible_moves = self.get_all_possible_moves_for_all_opponents(opponents)
        return random.choice(all_possible_moves)
    
    def short_sighted_move(self, opponents: Sequence[Player]) -> Sequence[Player, int, int]:
        all_possible_moves = self.get_all_possible_moves_for_all_opponents(opponents)
        all_possible_moves.sort(key=lambda move: self.evaluate_move(*move, opponents))
        return all_possible_moves[-1]
    
    def long_sighted_move(self, opponents: Sequence[Player]) -> Sequence[Player, int, int]:
        return self.short_sighted_move(opponents)
    


        


    
    