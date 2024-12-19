from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
import uvicorn
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session, init_db,clear_db
from app.models import Song, SongCreate

app = FastAPI()


@asynccontextmanager
async def lifespan():
    await init_db()
    yield
    await clear_db()


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.get("/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]


@app.post("/songs")
async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    await session.commit()
    await session.refresh(song)
    return song


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8008)
