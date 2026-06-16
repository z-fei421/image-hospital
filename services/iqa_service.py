import cv2
import numpy as np
from PIL import Image

class IQAService:
    """Image Quality Assessment service"""
    
    @staticmethod
    def calculate_metrics(image_path):
        """Calculate all IQA metrics"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError("Cannot read image")
            
            sharpness = IQAService._calculate_sharpness(img)
            contrast = IQAService._calculate_contrast(img)
            brightness = IQAService._calculate_brightness(img)
            noise = IQAService._calculate_noise(img)
            compression = IQAService._calculate_compression(img)
            
            # Calculate health score (weighted average)
            health_score = (
                0.35 * sharpness +
                0.25 * contrast +
                0.20 * brightness +
                0.20 * noise
            )
            
            return {
                'sharpness': round(sharpness, 2),
                'contrast': round(contrast, 2),
                'brightness': round(brightness, 2),
                'noise': round(noise, 2),
                'compression': round(compression, 2),
                'health_score': round(health_score, 2)
            }
        except Exception as e:
            raise Exception(f"IQA calculation failed: {str(e)}")
    
    @staticmethod
    def _calculate_sharpness(img):
        """Calculate sharpness using Laplacian variance"""
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        variance = np.var(laplacian)
        # Normalize to 0-100
        sharpness = min(100, variance / 50)  # Adjust divisor based on testing
        return sharpness
    
    @staticmethod
    def _calculate_contrast(img):
        """Calculate contrast using standard deviation"""
        std_dev = np.std(img)
        # Normalize to 0-100
        contrast = min(100, std_dev / 2.55)  # 255 / 100 = 2.55
        return contrast
    
    @staticmethod
    def _calculate_brightness(img):
        """Calculate brightness"""
        mean_brightness = np.mean(img)
        # Normalize to 0-100
        brightness = (mean_brightness / 255) * 100
        return brightness
    
    @staticmethod
    def _calculate_noise(img):
        """Calculate noise level"""
        # Use Laplacian to detect noise
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        # Local variance for noise estimation
        noise_level = np.mean(np.abs(laplacian))
        # Normalize to 0-100 (lower is better for noise)
        noise = 100 - min(100, noise_level / 2.55)
        return noise
    
    @staticmethod
    def _calculate_compression(img):
        """Estimate compression artifacts"""
        # Simple estimation based on block artifacts
        # In real implementation, use more sophisticated methods
        h, w = img.shape
        block_size = 8  # JPEG blocks are typically 8x8
        
        score = 85.0  # Default good score
        # This is simplified - real implementation would analyze block boundaries
        # For now, return a reasonable estimate
        return score
    
    @staticmethod
    def get_health_grade(score):
        """Get health grade based on score"""
        if score >= 85:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 50:
            return 'C'
        else:
            return 'D'
