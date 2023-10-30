from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError

from src.auth.manager import get_user_manager
from src.auth.base_config import auth_backend
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate
from src.database import get_async_session
from src.docs.models import document, referrals
from src.docs.schemas import DocsCreate


app = FastAPI(
    title="test"
)
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["Auth"],
)


current_user = fastapi_users.current_user()


@app.post("/add_docs", tags=["Docs"])
async def add_docs(
    new_docs: DocsCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
   ):
    entered_ids = [int(id) for id in new_docs.referrals.split(",")] if new_docs.referrals else []
    try:
        stmt = insert(document).values(name=new_docs.name, content=new_docs.content, owner_id=user.id).returning(
            document.c.id)
        result = await session.execute(stmt)
        inserted_id = result.scalar_one()
        for id in entered_ids:
            query = select(document).where((document.c.id == id))
            result = await session.execute(query)
            existing_document = result.scalar_one_or_none()

            if existing_document:
                stmt = insert(referrals).values(source_id=inserted_id, target_id=id)
                await session.execute(stmt)
            else:
                await session.rollback()
                raise HTTPException(status_code=404, detail=f"Referenced document with ID {id} not found")
        await session.commit()

        return {"status": "success", "document id": inserted_id}

    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="An error occurred during document creation")


@app.get("/get_docs", tags=["Docs"])
async def get_docs(
        document_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)):
    query = select(document).where((document.c.id == document_id) & (document.c.owner_id == user.id))
    result = await session.execute(query)
    return [dict(r._mapping) for r in result]


@app.delete("/del_docs", tags=["Docs"])
async def delete_docs(
    document_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    stmt = delete(document).where((document.c.id == document_id) & (document.c.owner_id == user.id))
    result = await session.execute(stmt)
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Document not found or you do not have permission to delete it")
    await session.commit()
    return {"status": "success", "deleted id": document_id}



