import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any, List
from utils.logger import logger

class VisionService:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    def analyze_image(self, image: Image.Image) -> Dict[str, Any]:
        try:
            img_np = np.array(image.convert('RGB'))
            img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            num_faces = len(faces)

            luminosity = float(np.mean(gray))
            sharpness = float(cv2.Laplacian(gray, cv2.CV_64F).var())
            top_colors = self._extract_dominant_colors(img_np, top_k=3)

            detected_objects: List[str] = []
            if num_faces > 0:
                detected_objects.append("rosto humano")

            description = f"Captura processada contendo {num_faces} rosto(s) identificado(s)."

            results = {
                "descricao": description,
                "objetos": detected_objects,
                "quantidade_pessoas": num_faces,
                "rostos": num_faces,
                "idade": "Não avaliado (Requer IA)",
                "emocao": "Não avaliado (Requer IA)",
                "cores": top_colors,
                "luminosidade": round(luminosity, 2),
                "nitidez": round(sharpness, 2),
                "json_resultado": {
                    "dimensions": {"width": image.width, "height": image.height},
                    "detected_faces_count": num_faces,
                    "metrics": {
                        "luminosity": round(luminosity, 2),
                        "sharpness": round(sharpness, 2)
                    }
                }
            }
            logger.info("Análise de Visão Computacional concluída com sucesso.")
            return results
        except Exception as e:
            logger.error(f"Erro durante o processamento da imagem: {str(e)}")
            raise e

    def _extract_dominant_colors(self, img_np: np.ndarray, top_k: int = 3) -> List[str]:
        pixels = img_np.reshape(-1, 3)
        pixels = np.float32(pixels)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        _, labels, centers = cv2.kmeans(pixels, top_k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)
        hex_colors = [f"#{c[0]:02x}{c[1]:02x}{c[2]:02x}" for c in centers]
        return hex_colors