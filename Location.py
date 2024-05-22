from app import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    address = db.Column(db.String(100), nullable = False)

    def __repr__(self) -> str:
        return '<Location %r>' % self.id