from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.model_native_chess_user import NativeChessProfile

async def get_native_profile_by_user_id(db : AsyncSession , user_id : int):
    query = select(NativeChessProfile).where(NativeChessProfile.user_id == user_id)
    result = await db.execute(query)
    return result.scalars().first()