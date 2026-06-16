from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from models.image import ImageRecord
from services.upload_service import UploadService
import os
from datetime import datetime

upload_bp = Blueprint('upload', __name__, url_prefix='/api')
upload_service = UploadService()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload image file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get file info
        file_size = os.path.getsize(filepath)
        resolution = upload_service.get_image_resolution(filepath)
        
        # Generate Patient ID (P + date + sequence number)
        patient_id = upload_service.generate_patient_id()
        
        # Create image record
        image_record = ImageRecord(
            patient_id=patient_id,
            image_name=file.filename,
            original_path=filepath,
            status='uploaded',
            file_size=file_size,
            resolution=resolution
        )
        
        db.session.add(image_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'patient_id': patient_id,
            'image_id': image_record.id,
            'image_name': image_record.image_name,
            'resolution': resolution,
            'file_size': file_size
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
