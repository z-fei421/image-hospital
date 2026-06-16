from flask import Blueprint, request, jsonify
from app import db
from models.image import ImageRecord
from models.diagnosis import DiagnosisRecord
from services.iqa_service import IQAService
from services.deepseek_service import DeepSeekService

diagnosis_bp = Blueprint('diagnosis', __name__, url_prefix='/api')
iqa_service = IQAService()
deepseek_service = DeepSeekService()

@diagnosis_bp.route('/check/<int:image_id>', methods=['POST'])
def check_image(image_id):
    """Perform IQA health check on image"""
    try:
        image_record = ImageRecord.query.get(image_id)
        if not image_record:
            return jsonify({'success': False, 'error': 'Image not found'}), 404
        
        # Calculate IQA metrics
        metrics = iqa_service.calculate_metrics(image_record.original_path)
        
        # Calculate health grade
        health_grade = iqa_service.get_health_grade(metrics['health_score'])
        
        # Create diagnosis record
        diagnosis = DiagnosisRecord(
            image_id=image_id,
            health_score=metrics['health_score'],
            sharpness=metrics['sharpness'],
            contrast=metrics['contrast'],
            brightness=metrics['brightness'],
            noise=metrics['noise'],
            compression=metrics['compression'],
            health_grade=health_grade
        )
        
        db.session.add(diagnosis)
        image_record.status = 'checked'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Health check completed',
            'diagnosis_id': diagnosis.id,
            'metrics': diagnosis.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@diagnosis_bp.route('/ai-diagnosis/<int:diagnosis_id>', methods=['POST'])
def ai_diagnosis(diagnosis_id):
    """Get AI diagnosis from DeepSeek"""
    try:
        diagnosis = DiagnosisRecord.query.get(diagnosis_id)
        if not diagnosis:
            return jsonify({'success': False, 'error': 'Diagnosis not found'}), 404
        
        # Get AI diagnosis (requires DeepSeek API)
        ai_result = deepseek_service.diagnose(diagnosis.to_dict())
        
        diagnosis.diagnosis_text = ai_result.get('diagnosis_text')
        diagnosis.problems = ai_result.get('problems')
        diagnosis.recommendations = ai_result.get('recommendations')
        diagnosis.risk_level = ai_result.get('risk_level')
        
        diagnosis.image.status = 'diagnosed'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'AI diagnosis completed',
            'diagnosis': diagnosis.to_dict(),
            'ai_result': ai_result
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
