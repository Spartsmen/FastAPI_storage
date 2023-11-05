from fastapi import FastAPI, Depends, HTTPException
from fastapi_users import FastAPIUsers

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError

from typing import List, Dict

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
        for id in set(entered_ids):
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
    stmt = delete(referrals).where(referrals.c.source_id == document_id)
    await session.execute(stmt)

    await session.commit()
    return {"status": "success", "deleted id": document_id}


@app.get("/search", tags=["Docs"])
async def search(
    document_name: str,
    depth: int = 3,
    limit: int = 10,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(document.c.name, document.c.id).where(document.c.name == document_name).limit(1)
    result = await session.execute(query)
    matching_documents = [dict(r._mapping) for r in result]

    if not matching_documents:
        raise HTTPException(status_code=404, detail="Document not found")

    document_ids = [doc['id'] for doc in matching_documents]
    references = []
    lenf = 0
    for _ in range(depth):
        query = select(document.c.name, document.c.id, referrals.c.target_id).join(referrals, document.c.id ==
            referrals.c.source_id).where(referrals.c.source_id.in_(document_ids))
        result = await session.execute(query)
        matching_references = [dict(r._mapping) for r in result][:limit-lenf]
        references.extend(matching_references)
        lenf += len(matching_documents) + len(references)
        document_ids = [ref['target_id'] for ref in matching_references]

        if not document_ids or lenf >= limit:
            break

    references = [dict(t) for t in {tuple(d.items()) for d in references}]
    return {"matching_documents": matching_documents, "references": references}


@app.get("/get_ids1", tags=["Docs"])
async def get_ids1(
    document_name: str,
    depth_start: int = 3,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(document.c.name, document.c.id).where(document.c.name == document_name).limit(10)
    result = await session.execute(query)
    matching_documents = [dict(r._mapping) for r in result]
    for doc in matching_documents:
        doc['referrals'] = await get_references([doc['id']], session, depth_start)
    return {"matching_documents": matching_documents}


async def get_references(document_ids: List[int], session: AsyncSession, depth_start: int, depth: int=0) -> List[Dict]:
    if depth >= depth_start:
        return []
    query = select(referrals).where(referrals.c.source_id.in_(document_ids))
    result = await session.execute(query)
    matching_references = [dict(r._mapping) for r in result]
    referenced_document_ids = [ref['target_id'] for ref in matching_references]
    query = select(document.c.name, document.c.id).where(document.c.id.in_(referenced_document_ids))
    result = await session.execute(query)
    referenced_documents = [dict(r._mapping) for r in result]
    for doc in referenced_documents:
        doc['references'] = await get_references([doc['id']], session,depth_start, depth + 1)
    return referenced_documents

# docker build -t myapp .
# docker run -p 8000:8000 myapp
