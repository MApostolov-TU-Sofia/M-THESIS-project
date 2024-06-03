from flask_sqlalchemy import SQLAlchemy
from application import app, db


class ProjectPrivacyModel(db.Model):
    __tablename__ = 'at_project_privacy_models'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('at_projects.id'), nullable=True)
    column_name = db.Column(db.String(256), nullable=False)
    column_type = db.Column(db.String(32), nullable=False)
    privacy_model = db.Column(db.String(32), nullable=False)
    column_value = db.Column(db.String(32), nullable=False)
    updated_at = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'column_name': self.column_name,
            'column_type': self.column_type,
            'privacy_model': self.privacy_model,
            'column_value': self.column_value,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }
