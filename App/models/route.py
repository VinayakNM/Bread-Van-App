from App.database import db

class Route(db.Model):
    routeId = db.Column(db.Integer, primary_key=True)
    streetName = db.Column(db.String(100), nullable=False)

    def __init__(self, streetName):
        self.streetName = streetName

    
