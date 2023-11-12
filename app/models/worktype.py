from app.extensions import db

class WorkType(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
