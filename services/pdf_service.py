from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from flask import current_app
from datetime import datetime

class PDFService:
    """Service for generating PDF reports"""
    
    @staticmethod
    def generate_report(image_record, diagnosis, treatment):
        """
        Generate PDF report for image records
        
        Args:
            image_record: ImageRecord model instance
            diagnosis: DiagnosisRecord model instance
            treatment: TreatmentRecord model instance
        
        Returns:
            Path to generated PDF
        """
        # Create PDF filename
        pdf_filename = f"report_{image_record.patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(current_app.config['REPORTS_FOLDER'], pdf_filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=1  # Center
        )
        elements.append(Paragraph("AI 图像医院 - 诊疗报告", title_style))
        elements.append(Spacer(1, 20))
        
        # Patient Info
        elements.append(Paragraph("<b>患者信息</b>", styles['Heading2']))
        patient_data = [
            ['患者ID', image_record.patient_id],
            ['图像名称', image_record.image_name],
            ['上传时间', image_record.upload_time.strftime('%Y-%m-%d %H:%M:%S')],
            ['分辨率', image_record.resolution or 'Unknown'],
            ['文件大小', f"{image_record.file_size / 1024:.2f} KB"],
        ]
        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(patient_table)
        elements.append(Spacer(1, 20))
        
        # Diagnosis Info
        if diagnosis:
            elements.append(Paragraph("<b>诊断结果</b>", styles['Heading2']))
            diagnosis_data = [
                ['健康评分', f"{diagnosis.health_score:.1f}/100"],
                ['健康等级', diagnosis.health_grade],
                ['清晰度', f"{diagnosis.sharpness:.1f}"],
                ['对比度', f"{diagnosis.contrast:.1f}"],
                ['亮度', f"{diagnosis.brightness:.1f}"],
                ['噪声', f"{diagnosis.noise:.1f}"],
                ['压缩损伤', f"{diagnosis.compression:.1f}"],
                ['风险等级', diagnosis.risk_level or 'N/A'],
            ]
            diagnosis_table = Table(diagnosis_data, colWidths=[2*inch, 4*inch])
            diagnosis_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(diagnosis_table)
            
            if diagnosis.diagnosis_text:
                elements.append(Spacer(1, 10))
                elements.append(Paragraph("<b>诊断说明：</b>", styles['Normal']))
                elements.append(Paragraph(diagnosis.diagnosis_text, styles['Normal']))
            
            elements.append(Spacer(1, 20))
        
        # Treatment Info
        if treatment:
            elements.append(Paragraph("<b>治疗结果</b>", styles['Heading2']))
            treatment_data = [
                ['治疗前评分', f"{treatment.before_score:.1f}/100"],
                ['治疗后评分', f"{treatment.after_score:.1f}/100"],
                ['提升幅度', f"{treatment.improvement:.1f}%"],
                ['治疗方法', treatment.treatment_methods or 'N/A'],
                ['治疗状态', treatment.status],
            ]
            treatment_table = Table(treatment_data, colWidths=[2*inch, 4*inch])
            treatment_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(treatment_table)
            elements.append(Spacer(1, 20))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=1
        )
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | AI 图像医院",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        return pdf_path
