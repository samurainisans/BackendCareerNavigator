from datetime import datetime
from app.extensions import db


class JobApplication(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.job_id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.resume_id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(120), nullable=False)
