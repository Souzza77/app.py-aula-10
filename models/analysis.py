from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from datetime import datetime, timezone
from database.connection import Base

class AnalysisModel(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    image_path = Column(String(500), nullable=False)
    descricao = Column(String(500), nullable=True)
    objetos = Column(JSON, nullable=True)
    quantidade_pessoas = Column(Integer, default=0, nullable=False)
    rostos = Column(Integer, default=0, nullable=False)
    idade = Column(String(50), nullable=True)
    emocao = Column(String(50), nullable=True)
    cores = Column(JSON, nullable=True)
    luminosidade = Column(Float, nullable=False)
    nitidez = Column(Float, nullable=False)
    json_resultado = Column(JSON, nullable=False)