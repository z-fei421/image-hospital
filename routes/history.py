from flask import Blueprint, jsonify
from app import db
from models.image import ImageRecord
from models.diagnosis import DiagnosisRecord
from models.treatment import TreatmentRecord

history_bp = Blueprint('history', __name__, url_prefix='/api')

@history_bp.route('/history', methods=['GET'])
def get_history():
    """Get all image history records"""
    try:
        images = ImageRecord.query.order_by(ImageRecord.upload_time.desc()).all()
        
        history_data = []
        for image in images:
            diagnosis = DiagnosisRecord.query.filter_by(image_id=image.id).first()
            treatment = TreatmentRecord.query.filter_by(image_id=image.id).first()
            
            history_data.append({
                'image': image.to_dict(),
                'diagnosis': diagnosis.to_dict() if diagnosis else None,
                'treatment': treatment.to_dict() if treatment else None
            })
        
        return jsonify({
            'success': True,
            'total': len(history_data),
            'history': history_data
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@history_bp.route('/history/<int:image_id>', methods=['GET'])
def get_image_detail(image_id):
    """Get detailed information for a specific image"""
    try:
        image = ImageRecord.query.get(image_id)
        if not image:
            return jsonify({'success': False, 'error': 'Image not found'}), 404
        
        diagnosis = DiagnosisRecord.query.filter_by(image_id=image_id).first()
        treatment = TreatmentRecord.query.filter_by(image_id=image_id).first()
        
        return jsonify({
            'success': True,
            'image': image.to_dict(),
            'diagnosis': diagnosis.to_dict() if diagnosis else None,
            'treatment': treatment.to_dict() if treatment else None
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
