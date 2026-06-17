from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .image import ImageRecord
from .diagnosis import DiagnosisRecord
from .treatment import TreatmentRecord

__all__ = ['db', 'ImageRecord', 'DiagnosisRecord', 'TreatmentRecord']
