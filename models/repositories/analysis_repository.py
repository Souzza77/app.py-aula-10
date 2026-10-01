from typing import List, Optional
from sqlalchemy.orm import Session
from models.analysis import AnalysisModel
from utils.logger import logger

class AnalysisRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create(self, data: dict) -> AnalysisModel:
        try:
            record = AnalysisModel(**data)
            self.db.add(record)
            self.db.commit()
            self.db.refresh(record)
            logger.info(f"Registro de análise salvo com ID: {record.id}")
            return record
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao salvar análise no repositório: {str(e)}")
            raise e

    def get_all(self) -> List[AnalysisModel]:
        return self.db.query(AnalysisModel).order_by(AnalysisModel.created_at.desc()).all()

    def get_by_id(self, analysis_id: int) -> Optional[AnalysisModel]:
        return self.db.query(AnalysisModel).filter(AnalysisModel.id == analysis_id).first()

    def delete(self, analysis_id: int) -> bool:
        try:
            record = self.get_by_id(analysis_id)
            if record:
                self.db.delete(record)
                self.db.commit()
                logger.info(f"Registro ID {analysis_id} removido com sucesso.")
                return True
            return False
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao deletar análise ID {analysis_id}: {str(e)}")
            raise e