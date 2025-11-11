"""
Base de datos y configuración de SQLAlchemy
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
from app.config.settings import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base class para modelos de SQLAlchemy"""
    pass


# Motor de base de datos asíncrono
engine = create_async_engine(
    settings.get_database_url().replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_database():
    """
    Dependency para obtener sesión de base de datos
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def test_connection():
    """
    Función para probar la conexión a la base de datos
    """
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            logger.info("✅ Conexión a la base de datos exitosa")
            return True
    except Exception as e:
        logger.error(f"❌ Error conectando a la base de datos: {e}")
        return False


async def close_database():
    """
    Cerrar conexiones de la base de datos
    """
    await engine.dispose()
    logger.info("🔒 Conexiones de base de datos cerradas")