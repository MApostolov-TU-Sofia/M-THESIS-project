from application import app, db


class Project(db.Model):
    __tablename__ = 'at_projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('at_users.id'), nullable=True)
    updated_at = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, nullable=False)
    project_tables = db.relationship('ProjectTable')
    project_data_transformations = db.relationship('ProjectDataTransformation')
    project_privacy_models = db.relationship('ProjectPrivacyModel')

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
            'project_tables': self.project_tables,
            'project_data_transformations': self.project_data_transformations,
            'project_privacy_models': self.project_privacy_models
        }
