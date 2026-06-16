from app import db
from datetime import datetime

class TreatmentRecord(db.Model):
    """Treatment record model - stores restoration progress and results"""
    __tablename__ = 'treatment_record'
    
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image_record.id'), nullable=False, index=True)
    treatment_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Treatment methods applied
    treatment_methods = db.Column(db.Text, nullable=True)  # e.g., "super_resolution,denoise,face_restoration"
    treatment_plan = db.Column(db.Text, nullable=True)  # Detailed treatment plan from AI
    
    # Before and after scores
    before_score = db.Column(db.Float, nullable=False)  # Score before treatment
    after_score = db.Column(db.Float, nullable=False)  # Score after treatment
    improvement = db.Column(db.Float, nullable=False)  # Improvement percentage
    
    # Detailed metrics after treatment
    after_sharpness = db.Column(db.Float, nullable=True)
    after_contrast = db.Column(db.Float, nullable=True)
    after_brightness = db.Column(db.Float, nullable=True)
    after_noise = db.Column(db.Float, nullable=True)
    after_compression = db.Column(db.Float, nullable=True)
    
    # Status
    status = db.Column(db.String(50), default='pending', nullable=False)  # pending, processing, completed, failed
    treatment_duration = db.Column(db.Integer, nullable=True)  # seconds
    error_message = db.Column(db.Text, nullable=True)  # If failed, store error
    
    def __repr__(self):
        return f'<TreatmentRecord image_id={self.image_id} improvement={self.improvement}%>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_id': self.image_id,
            'treatment_time': self.treatment_time.isoformat(),
            'before_score': self.before_score,
            'after_score': self.after_score,
            'improvement': self.improvement,
            'status': self.status,
            'treatment_methods': self.treatment_methods
        }
