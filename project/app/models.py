from sqlmodel import SQLModel, Field


class SongBase(SQLModel):
    name: str
    artist: str
    year: int | None = None


class Song(SongBase, table=True):
    id: int = Field(default=None, nullable=False, primary_key=True)


class SongCreate(SongBase):
    pass
