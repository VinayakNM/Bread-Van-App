from App.database import db
from datetime import datetime

class StopRequests(db.Model):
    requestId = db.Column(db.Integer, primary_key=True)
    requestTime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    residentId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    driverId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    stopLocation = db.Column(db.String(100), nullable=False)


    def __init__(self, location, time, residentId):
        self.location = location
        self.time = time
        self.residentId = residentId
        self.status = 'pending'