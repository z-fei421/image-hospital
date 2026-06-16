from app import db
from datetime import datetime

class DiagnosisRecord(db.Model):
    """Diagnosis record model - stores IQA analysis results"""
    __tablename__ = 'diagnosis_record'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image_record.id'), nullable=False, index=True)
    diagnosis_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # IQA Metrics (0-100)
    health_score = db.Column(db.Float, nullable=False)  # Overall score
    sharpness = db.Column(db.Float, nullable=False)  # Clarity/Sharpness
    contrast = db.Column(db.Float, nullable=False)  # Contrast level
    brightness = db.Column(db.Float, nullable=False)  # Brightness level
    noise = db.Column(db.Float, nullable=False)  # Noise level
    compression = db.Column(db.Float, nullable=False)  # Compression artifacts
    
    # Health Grade (A/B/C/D)
    health_grade = db.Column(db.String(1), nullable=False)  # A: 85-100, B: 70-84, C: 50-69, D: 0-49
    
    # Diagnosis text from AI
    diagnosis_text = db.Column(db.Text, nullable=True)  # AI analysis output
    problems = db.Column(db.Text, nullable=True)  # Identified problems (JSON format)
    recommendations = db.Column(db.Text, nullable=True)  # Treatment recommendations (JSON format)
    risk_level = db.Column(db.String(50), nullable=True)  # low, medium, high
    
    def __repr__(self):
        return f'<DiagnosisRecord image_id={self.image_id} score={self.health_score}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_id': self.image_id,
            'diagnosis_time': self.diagnosis_time.isoformat(),
            'health_score': self.health_score,
            'sharpness': self.sharpness,
            'contrast': self.contrast,
            'brightness': self.brightness,
            'noise': self.noise,
            'compression': self.compression,
            'health_grade': self.health_grade,
            'risk_level': self.risk_level
        }
