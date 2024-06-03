from flask_sqlalchemy import SQLAlchemy
from application import app, db


class ProjectDataTransformation(db.Model):
    __tablename__ = 'at_project_data_transformations'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('at_projects.id'), nullable=True)
    column_name = db.Column(db.String(256), nullable=False)
    column_type = db.Column(db.String(32), nullable=False)
    transformation_type = db.Column(db.String(32), nullable=False)
    hierarchy_type = db.Column(db.String(32), nullable=False)
    hierarchy_symbols = db.Column(db.String(128), nullable=False)
    updated_at = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'column_name': self.column_name,
            'column_type': self.column_type,
            'transformation_type': self.transformation_type,
            'hierarchy_type': self.hierarchy_type,
            'hierarchy_symbols': self.hierarchy_symbols,
            'updated_at': self.updated_at,
            'created_at': self.created_at
        }
