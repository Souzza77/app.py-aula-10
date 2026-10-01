import os
import uuid
from PIL import Image
from config.settings import Settings
from utils.logger import logger

class StorageService:
    @staticmethod
    def save_image(image: Image.Image) -> str:
        try:
            filename = f"capture_{uuid.uuid4().hex}.jpg"
            filepath = os.path.join(Settings.UPLOAD_FOLDER, filename)
            image.save(filepath, format="JPEG", quality=90)
            logger.info(f"Imagem salva no caminho: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo de imagem: {str(e)}")
            raise e