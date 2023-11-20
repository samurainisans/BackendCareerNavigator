from app.extensions import db


class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.industry_id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.String(255), nullable=True)
    hr_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
