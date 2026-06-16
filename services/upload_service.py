import os
from PIL import Image
from datetime import datetime
from app import db
from models.image import ImageRecord

class UploadService:
    """Service for handling file uploads"""
    
    @staticmethod
    def get_image_resolution(filepath):
        """Get image resolution"""
        try:
            img = Image.open(filepath)
            width, height = img.size
            return f"{width}x{height}"
        except Exception as e:
            return "Unknown"
    
    @staticmethod
    def generate_patient_id():
        """Generate unique patient ID (e.g., P202606220001)"""
        date_str = datetime.now().strftime('%Y%m%d')
        
        # Get the count of records for today
        today_count = ImageRecord.query.filter(
            ImageRecord.patient_id.like(f'P{date_str}%')
        ).count()
        
        sequence = str(today_count + 1).zfill(4)
        return f"P{date_str}{sequence}"
    
    @staticmethod
    def delete_file(filepath):
        """Delete file from disk"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            pass
        return False
