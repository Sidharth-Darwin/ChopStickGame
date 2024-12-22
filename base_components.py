from collections.abc import Sequence
from typing import Self, Optional, Tuple

class Player:
    player_count = 1

    def __init__(self, name: str = player_count, verbose: bool = True):
        Player.player_count += 1
        self.name = name
        self.verbose = verbose
        self.left_hand = 1
        self.right_hand = 1
        self.actions = ["left", "right", "split"]

    def __repr__(self) -> str:
        return f"|{self.name:^20}|{self.left_hand:^11}|{self.right_hand:^12}|"
    
    def tap(self, self_hand: int, opponent_hand: int) -> int:
        opponent_hand += self_hand
        if opponent_hand == 5:
            return 0
        return opponent_hand % 5
    
    def make_move(self, opponent: Self, my_hand_action: int, opponent_hand: int) -> None:
        if my_hand_action == 2:
            self.split()
            my_hand_action = 0
        if my_hand_action == 0:
            if opponent_hand == 0:
                opponent.left_hand = self.tap(self.left_hand, opponent.left_hand)
            else:
                opponent.right_hand = self.tap(self.left_hand, opponent.right_hand)
        elif my_hand_action == 1:
            if opponent_hand == 0:
                opponent.left_hand = self.tap(self.right_hand, opponent.left_hand)
            else:
                opponent.right_hand = self.tap(self.right_hand, opponent.right_hand)
    
    def is_split_possible(self) -> bool:
        if self.left_hand == 0:
            if self.right_hand == 2 or self.right_hand == 4:
                return True
        elif self.right_hand == 0:
            if self.left_hand == 2 or self.left_hand == 4:
                return True
        return False
    
    def possible_actions(self) -> list[str]:
        actions = []
        if self.left_hand != 0:
            actions.append(0)
        if self.right_hand != 0:
            actions.append(1)
        if self.is_split_possible():
            actions.append(2)
        return actions
    
    def split(self) -> None:
        val = (self.left_hand + self.right_hand) // 2
        self.left_hand = val
        self.right_hand = val

    def evaluate_move(self, opponent: Self, my_hand_action: int, opponent_hand: int, opponents: Sequence[Self]) -> int:
        opp_after_move = Player()
        opp_after_move.left_hand = opponent.left_hand
        opp_after_move.right_hand = opponent.right_hand
        self.make_move(opp_after_move, my_hand_action, opponent_hand)
        if opp_after_move.am_i_defeated():
            return 10
        opponent_index = opponents.index(opponent)
        new_opponents = [opp_after_move] + opponents[:opponent_index] + opponents[opponent_index+1:]
        for any_opponent in new_opponents:
            for opponent_possible_hand, my_possible_hand in any_opponent.get_all_possible_moves(self):
                future_self = Player()
                future_self.left_hand = self.left_hand
                future_self.right_hand = self.right_hand
                any_opponent.make_move(future_self, opponent_possible_hand, my_possible_hand)
                if future_self.am_i_defeated():
                    return -10
        return 0
    
    def evaluate_move_verbose(self, opponent: Self, my_hand_action: int, opponent_hand: int, opponents: Sequence[Self]) -> Tuple[int, str]:
        opp_after_move = Player()
        opp_after_move.name = opponent.name
        opp_after_move.left_hand = opponent.left_hand
        opp_after_move.right_hand = opponent.right_hand
        self.make_move(opp_after_move, my_hand_action, opponent_hand)
        if opp_after_move.am_i_defeated():
            return 10, f"\t--> I ({self.name}) have defeated {opponent.name}, return 10 score\n"
        opponent_index = opponents.index(opponent)
        new_opponents = [opp_after_move] + opponents[:opponent_index] + opponents[opponent_index+1:]
        for any_opponent in new_opponents:
            for opponent_possible_hand, my_possible_hand in any_opponent.get_all_possible_moves(self):
                future_self = Player()
                future_self.left_hand = self.left_hand
                future_self.right_hand = self.right_hand
                any_opponent.make_move(future_self, opponent_possible_hand, my_possible_hand)
                if future_self.am_i_defeated():
                    return -10, f"\t--> I ({self.name}) was defeated by {any_opponent.name}, return -10 score\n"
        return 0, ""
    
    def get_all_possible_moves_for_all_opponents(self, opponents: Sequence[Self]) -> Sequence[Sequence[Self, int, int]]:
        all_possible_moves = []
        for opponent in opponents:
            all_possible_moves.extend((opponent, my_hand_action, opponent_hand) for my_hand_action, opponent_hand in self.get_all_possible_moves(opponent))
        return all_possible_moves
    
    def get_all_possible_moves(self, opponent: Self) -> Sequence[Tuple[int, int]]:
        all_possible_moves = []
        for my_hand_action in self.possible_actions():
            for opponent_hand in opponent.possible_actions():
                if opponent_hand == 2:
                    continue
                all_possible_moves.append((my_hand_action, opponent_hand))
        return all_possible_moves

    def am_i_defeated(self) -> bool:
        return self.left_hand == 0 and self.right_hand == 0
    
    def play(self, opponents: Sequence[Self]) -> Self:
        raise NotImplementedError("Child classes must implement this method.")
    
    def exit_game(self) -> None:
        raise NotImplementedError("Child classes must implement this method.")

class ChopStickGame:
    def __init__(self, players: Sequence[Player]):
        unique_players = []
        for player in players:
            if player not in unique_players:
                unique_players.append(player)
        self.players = unique_players
        self.winner = None

    def play_game(self) -> None:
        current_player_idx = 0
        while len(self.players) > 1:
            current_player = self.players[current_player_idx]
            opponent_player = current_player.play(self.players[:current_player_idx] + self.players[current_player_idx + 1:])
            if opponent_player.am_i_defeated():
                opponent_player.exit_game(self.players,f"{opponent_player.name} was defeated by {current_player.name}!")
            self.display_game(current_player, opponent_player)
            current_player_idx = (current_player_idx + 1) % len(self.players)
        if len(self.players) == 1:
            self.set_result(self.players[0])
            self.players[0].exit_game(self.players,f"Game over!\n{self.players[0].name} has won the game!")

    def display_game(self, current_player: Optional[Player] = None, opponent_player: Optional[Player] = None) -> None:
        raise NotImplementedError("Child classes must implement this method.")
    
    def set_result(self, player: Player) -> None:
        self.winner = player

    def get_result(self) -> str:
        return self.winner.name if self.winner else ""

    