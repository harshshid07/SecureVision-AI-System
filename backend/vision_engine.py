"""
Vision Engine for SecureVision
Handles all face recognition, anti-spoofing, and validation logic using DeepFace
"""
from deepface import DeepFace
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import base64
import cv2
from io import BytesIO
from PIL import Image
from config import settings
import warnings

# Check if PyTorch is available for anti-spoofing
ANTI_SPOOFING_AVAILABLE = False
try:
    import torch
    ANTI_SPOOFING_AVAILABLE = True
except ImportError:
    warnings.warn(
        "PyTorch not installed. Anti-spoofing will be disabled. "
        "Install with: pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu"
    )


class VisionEngine:
    """
    Core facial recognition engine with multi-layer security:
    1. Single face enforcement
    2. Passive anti-spoofing (optional, requires PyTorch)
    3. Face matching with cosine similarity
    """
    
    def __init__(self):
        self.model_name = settings.DEEPFACE_MODEL  # "Facenet"
        self.detector_backend = settings.DEEPFACE_DETECTOR  # "retinaface"
        self.threshold = settings.FACE_MATCH_THRESHOLD  # 0.6
        
        # Log anti-spoofing status
        if ANTI_SPOOFING_AVAILABLE:
            print("✅ Anti-spoofing enabled (PyTorch available)")
        else:
            print("⚠️  Anti-spoofing disabled (PyTorch not available)")
            print("   Install PyTorch to enable: pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu")
    
    def _base64_to_image(self, base64_string: str) -> np.ndarray:
        """Convert base64 string to numpy array (OpenCV format)"""
        # Remove data URL prefix if present
        if "data:image" in base64_string:
            base64_string = base64_string.split(",")[1]
        
        # Decode base64
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to OpenCV format (RGB)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    def extract_single_face_embedding(self, image_base64: str) -> Dict[str, Any]:
        """
        Extract face embedding with strict validation:
        - Only 1 face allowed
        - Anti-spoofing check (if PyTorch available)
        Returns: {
            "success": bool,
            "embedding": List[float] or None,
            "error": str or None,
            "face_count": int,
            "is_real": bool or None
        }
        """
        try:
            # Convert base64 to image
            img = self._base64_to_image(image_base64)
            
            # Step 1: Extract faces with optional anti-spoofing
            # Only enable anti-spoofing if PyTorch is available
            use_anti_spoofing = ANTI_SPOOFING_AVAILABLE
            
            faces = DeepFace.extract_faces(
                img_path=img,
                detector_backend=self.detector_backend,
                enforce_detection=True,
                anti_spoofing=use_anti_spoofing  # Only enable if torch is available
            )
            
            # Step 2: Single face enforcement
            if len(faces) == 0:
                return {
                    "success": False,
                    "embedding": None,
                    "error": "No face detected. Please position your face in the camera.",
                    "face_count": 0,
                    "is_real": None
                }
            
            if len(faces) > 1:
                return {
                    "success": False,
                    "embedding": None,
                    "error": "Multiple faces detected. Only one person allowed.",
                    "face_count": len(faces),
                    "is_real": None
                }
            
            # Step 3: Anti-spoofing check (only if available)
            face_data = faces[0]
            is_real = face_data.get("is_real", True)  # Default to True if not available
            
            if use_anti_spoofing and not is_real:
                return {
                    "success": False,
                    "embedding": None,
                    "error": "Anti-spoofing failed. Live presence required.",
                    "face_count": 1,
                    "is_real": False
                }
            
            # Step 4: Generate embedding
            embedding_result = DeepFace.represent(
                img_path=img,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            
            # Extract the embedding vector
            embedding = embedding_result[0]["embedding"]
            
            return {
                "success": True,
                "embedding": embedding,  # 128-d vector for Facenet
                "error": None,
                "face_count": 1,
                "is_real": is_real if use_anti_spoofing else None  # None indicates anti-spoofing not available
            }
            
        except ValueError as e:
            return {
                "success": False,
                "embedding": None,
                "error": f"Face detection failed: {str(e)}",
                "face_count": 0,
                "is_real": None
            }
        except Exception as e:
            return {
                "success": False,
                "embedding": None,
                "error": f"Vision engine error: {str(e)}",
                "face_count": 0,
                "is_real": None
            }
    
    def verify_access(
        self,
        live_image_base64: str,
        stored_embedding: List[float]
    ) -> Dict[str, Any]:
        """
        Complete verification pipeline:
        1. Extract face from live image
        2. Check single face
        3. Check anti-spoofing
        4. Compare with stored embedding
        
        Returns: {
            "verified": bool,
            "similarity_score": float,
            "is_real": bool,
            "face_count": int,
            "error": str or None
        }
        """
        # Step 1: Extract live face embedding with all validations
        extraction_result = self.extract_single_face_embedding(live_image_base64)
        
        if not extraction_result["success"]:
            return {
                "verified": False,
                "similarity_score": 0.0,
                "is_real": extraction_result["is_real"],
                "face_count": extraction_result["face_count"],
                "error": extraction_result["error"]
            }
        
        live_embedding = extraction_result["embedding"]
        
        # Step 2: Calculate cosine similarity
        similarity = self._cosine_similarity(live_embedding, stored_embedding)
        
        # Step 3: Verify based on threshold
        verified = similarity >= self.threshold
        
        if not verified:
            return {
                "verified": False,
                "similarity_score": similarity,
                "is_real": True,
                "face_count": 1,
                "error": f"Face verification failed. Similarity: {similarity:.2f} (threshold: {self.threshold})"
            }
        
        return {
            "verified": True,
            "similarity_score": similarity,
            "is_real": True,
            "face_count": 1,
            "error": None
        }
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))


# Singleton instance
vision_engine = VisionEngine()
