import fastapi
from fastapi import status , HTTPException

import chess
import chess.engine

import asyncio
from dotenv import load_dotenv
import logging
import os

load_dotenv()
logger = logging.getLogger(__name__)

class NativeChessEngine:

    engine_binary_url = os.getenv('NATIVE_CHESS_BINARY_PATH')

    def __init__ (self):
        native_engine_url = self.engine_binary_url

    async def get_best_moves(self ,fen : str , time_limit : fload = 2.0) -> str :
        """
        create a chessboard from the fen from the frontend
        initialize the engine
        get best move from engine
        return the moves in UCI format
        """
        board = chess.Board(fen) # use the fen string from the frontend to create a representational object of the chessboard
        
        # initilaize the engine 

        transport. engine = await chess.engine.popen_uci(self.engine_binary_url)

        try :
            # get best move

            result = await engine.play(
                board,
                chess.engine.Limit(time = time_limit)
            )
            return result.move.uci() # returns moves in uci format
        except Exception as e:
            logger.error(f"an error occured , detail : {str(e)}")
            raise RuntimeError(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR , detail = f"there was an error getting the result")
        finally :
            await engine.quit()


    
