"""
Some example strategies for people who want to create a custom, homemade bot.
"""

from __future__ import annotations

import logging

import chess
from chess.engine import PlayResult
import random
from engine_wrapper import MinimalEngine
from typing import Any

from src import main

logger = logging.getLogger(__name__)


class ExampleEngine(MinimalEngine):
    pass


# Strategy names and ideas from tom7's excellent eloWorld video

class RandomMove(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        return PlayResult(random.choice(list(board.legal_moves)), None)


class Alphabetical(ExampleEngine):
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        moves.sort(key=board.san)
        return PlayResult(moves[0], None)


class FirstMove(ExampleEngine):
    """Gets the first move when sorted by uci representation"""
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        moves = list(board.legal_moves)
        moves.sort(key=str)
        return PlayResult(moves[0], None)


class Habits1(ExampleEngine):
    """Calls an AWS lambda to get the recommended move"""
    def search(self, board: chess.Board, *args: Any) -> PlayResult:
        move_str = main.invoke_function(board.fen())
        logger.info(f"Move returned from lambda function: {move_str}")
        move = chess.Move.from_uci(move_str)
        return PlayResult(move, None)
