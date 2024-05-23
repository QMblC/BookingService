from app import db

class Slot(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    master_id = db.Column(db.Integer, nullable = False)
    booked_by = db.Column(db.Integer)
    slot_type = db.Column(db.String(20), nullable = False)
    time = db.Column(db.DateTime, nullable = False)

    def __repr__(self):
        return '<Slot %r>' % self.id