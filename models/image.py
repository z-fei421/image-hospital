from app import db
from datetime import datetime
import uuid

class ImageRecord(db.Model):
    """Image record model - stores basic image information"""
    __tablename__ = 'image_record'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    image_name = db.Column(db.String(255), nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    original_path = db.Column(db.String(500), nullable=False)
    restored_path = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(50), default='uploaded', nullable=False)  # uploaded, checked, diagnosed, treating, completed
    file_size = db.Column(db.Integer, nullable=True)  # bytes
    resolution = db.Column(db.String(50), nullable=True)  # e.g., "1920x1080"
    
    # Relationships
    diagnosis_records = db.relationship('DiagnosisRecord', backref='image', lazy=True, cascade='all, delete-orphan')
    treatment_records = db.relationship('TreatmentRecord', backref='image', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ImageRecord {self.patient_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'image_name': self.image_name,
            'upload_time': self.upload_time.isoformat(),
            'status': self.status,
            'file_size': self.file_size,
            'resolution': self.resolution
        }
