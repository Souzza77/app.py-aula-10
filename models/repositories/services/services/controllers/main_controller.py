from PIL import Image
from database.connection import SessionLocal
from repositories.analysis_repository import AnalysisRepository
from services.vision_service import VisionService
from services.storage_service import StorageService
from utils.logger import logger

class MainController:
    def __init__(self):
        self.vision_service = VisionService()

    def process_capture(self, image: Image.Image) -> dict:
        db = SessionLocal()
        try:
            repo = AnalysisRepository(db)
            analysis_data = self.vision_service.analyze_image(image)
            filepath = StorageService.save_image(image)
            analysis_data["image_path"] = filepath

            record = repo.create(analysis_data)
            return {
                "id": record.id,
                "created_at": record.created_at,
                "image_path": record.image_path,
                **analysis_data
            }
        except Exception as e:
            logger.error(f"Falha no fluxo do controlador: {str(e)}")
            raise e
        finally:
            db.close()

    def fetch_all_analyses(self):
        db = SessionLocal()
        try:
            repo = AnalysisRepository(db)
            return repo.get_all()
        finally:
            db.close()

    def delete_analysis(self, analysis_id: int) -> bool:
        db = SessionLocal()
        try:
            repo = AnalysisRepository(db)
            return repo.delete(analysis_id)
        finally:
            db.close()