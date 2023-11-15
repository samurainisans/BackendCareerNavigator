from app import db


class Resume(db.Model):
    title = db.Column(db.Text)
    resume_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    description = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    contact_info = db.Column(db.Text)