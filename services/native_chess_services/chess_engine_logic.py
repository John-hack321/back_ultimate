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

    
