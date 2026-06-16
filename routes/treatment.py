from flask import Blueprint, request, jsonify, current_app
from app import db
from models.image import ImageRecord
from models.treatment import TreatmentRecord
from models.diagnosis import DiagnosisRecord
from services.replicate_service import ReplicateService
from services.iqa_service import IQAService
import time

treatment_bp = Blueprint('treatment', __name__, url_prefix='/api')
replicate_service = ReplicateService()
iqa_service = IQAService()

@treatment_bp.route('/treatment/start/<int:image_id>', methods=['POST'])
def start_treatment(image_id):
    """Start image restoration treatment"""
    try:
        image_record = ImageRecord.query.get(image_id)
        if not image_record:
            return jsonify({'success': False, 'error': 'Image not found'}), 404
        
        diagnosis = DiagnosisRecord.query.filter_by(image_id=image_id).first()
        if not diagnosis:
            return jsonify({'success': False, 'error': 'Diagnosis not found, please check image first'}), 400
        
        # Get treatment methods from request or use default
        treatment_methods = request.json.get('methods', 'super_resolution,denoise')
        
        # Create treatment record
        treatment = TreatmentRecord(
            image_id=image_id,
            treatment_methods=treatment_methods,
            before_score=diagnosis.health_score,
            after_score=0,  # Will be updated
            improvement=0,  # Will be updated
            status='processing'
        )
        
        db.session.add(treatment)
        db.session.commit()
        
        image_record.status = 'treating'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Treatment started',
            'treatment_id': treatment.id,
            'status': 'processing'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@treatment_bp.route('/treatment/status/<int:treatment_id>', methods=['GET'])
def treatment_status(treatment_id):
    """Get treatment status"""
    try:
        treatment = TreatmentRecord.query.get(treatment_id)
        if not treatment:
            return jsonify({'success': False, 'error': 'Treatment not found'}), 404
        
        return jsonify({
            'success': True,
            'treatment': treatment.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
