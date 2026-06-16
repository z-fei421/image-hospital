from flask import Blueprint, send_file, jsonify
from app import db
from models.image import ImageRecord
from models.diagnosis import DiagnosisRecord
from models.treatment import TreatmentRecord
from services.pdf_service import PDFService
import os

report_bp = Blueprint('report', __name__, url_prefix='/api')
pdf_service = PDFService()

@report_bp.route('/report/<int:image_id>', methods=['GET'])
def generate_report(image_id):
    """Generate PDF report for an image"""
    try:
        image_record = ImageRecord.query.get(image_id)
        if not image_record:
            return jsonify({'success': False, 'error': 'Image not found'}), 404
        
        diagnosis = DiagnosisRecord.query.filter_by(image_id=image_id).first()
        treatment = TreatmentRecord.query.filter_by(image_id=image_id).first()
        
        # Generate PDF
        pdf_path = pdf_service.generate_report(
            image_record,
            diagnosis,
            treatment
        )
        
        return send_file(pdf_path, as_attachment=True, download_name=f"report_{image_record.patient_id}.pdf")
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
