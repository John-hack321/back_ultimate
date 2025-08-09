from fastapi import HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from sqlalchemy.orm import query

from db.db_setup import Base
from db.models.model_foreign_chess_user import ChessProfile
from pydantic_schemas.chess_player_schemas import CreateChessDbProfile , account_status_code
from api.utils.util_native_chess_players import get_native_profile_by_user_id

async def add_new_chess_player(db: AsyncSession, user_chess_data: dict, user_id: int):
    """
    Creates a new chess player profile from dictionary data returned by the chess service
    """
    # Convert dictionary data to the format expected by the database model
    new_chess_data = ChessProfile(
        user_id=user_id,
        player_id=user_chess_data.get('player_id'),
        username=user_chess_data.get('chess_username'),
        followers=user_chess_data.get('followers', 0),
        country=user_chess_data.get('country'),
        account_status=account_status_code.basic,  # Default to basic
        account_verification_status=user_chess_data.get('account_verification_status', False),
        league=user_chess_data.get('league', 'wood')
    )
    
    db.add(new_chess_data)
    
    # after crating the object in the database we will want to update nativechessprofile with the relevant foreingchess id
    await db.flush()

    db_native_profile = await get_native_profile_by_user_id(db , new_chess_data.user_id)
    if not db_native_profile:
        raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR , detail = f'falied to get native profile object for update')
    #update the foreign_chess_id
    db_native_profile.foreign_chess_id = new_chess_data.id


    await db.commit()
    await db.refresh(new_chess_data)
    await db.refresh(db_native_profile)
    return new_chess_data


async def get_user_by_chess_foreign_username(db: AsyncSession, username: str):
    query = select(ChessProfile).where(ChessProfile.username == username) 
    print('the database query was ran successful')
    result = await db.execute(query)
    print('result returned successfuly')
    result = result.scalars().first()
    print(f'object returned : {result}')
    return result

"""
but this is a chance to show them that i can do and be alot in the most powerful way to ever exist ama 
its my time to show what im capable of , and i kinda have like 2 years to do that.
okay hii kitu ya kamama ndio inanipea stress kidogo. but i need to find a way around it.
"""