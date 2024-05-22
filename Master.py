from app import db

class Master(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    location_id = db.Column(db.Integer, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)

    def __repr__(self):
        return '<Master %r>' % self.id