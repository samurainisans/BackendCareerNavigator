from datetime import datetime
from app.extensions import db

class Job(db.Model):
    job_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('work_type.type_id'), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    employment_id = db.Column(db.Integer, db.ForeignKey('employment.employment_id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    salary = db.Column(db.Float, nullable=True)
    experience = db.Column(db.String(120), nullable=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)