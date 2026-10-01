from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.settings import Settings
from utils.logger import logger

class Base(DeclarativeBase):
    pass

engine = create_engine(
    Settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tabelas inicializadas com sucesso no Neon.tech PostgreSQL.")
    except Exception as e:
        logger.error(f"Erro ao inicializar tabelas do banco de dados: {str(e)}")
        raise e