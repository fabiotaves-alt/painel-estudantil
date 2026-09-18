from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import settings


class Database:
    """Gerenciamento de conexão com banco de dados."""

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_maker: async_sessionmaker[AsyncSession] | None = None

    def init(self) -> None:
        """Inicializa o engine e session maker."""
        self._engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            future=True,
        )
        self._session_maker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise RuntimeError("Database não inicializado. Chame init() primeiro.")
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        if self._session_maker is None:
            raise RuntimeError("Database não inicializado. Chame init() primeiro.")
        return self._session_maker

    async def create_tables(self) -> None:
        """Cria todas as tabelas no banco de dados."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Gera sessões do banco de dados."""
        async with self.session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def dispose(self) -> None:
        """Fecha todas as conexões do engine."""
        if self._engine:
            await self._engine.dispose()
            self._engine = None
            self._session_maker = None


database = Database()
