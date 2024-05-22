from app import db

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    master_id = db.Column(db.Integer, nullable = False)
    booked_by = db.Column(db.Integer)