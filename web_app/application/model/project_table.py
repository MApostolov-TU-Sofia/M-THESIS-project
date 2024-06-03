from flask_sqlalchemy import SQLAlchemy
from application import app, db


class ProjectTable(db.Model):
    __tablename__ = 'at_project_tables'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('at_projects.id'), nullable=True)
    row_index = db.Column(db.Integer, nullable=False)
    column_type = db.Column(db.String(32), nullable=False)
    column_name = db.Column(db.String(256), nullable=False)
    column_value = db.Column(db.String(256), nullable=True)
    updated_at = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'column_type': self.column_type,
            'column_name': self.column_name,
            'column_value': self.column_value,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }
