from App.database import db
from datetime import datetime


class Schedule(db.Model):
    scheduleId = db.Column(db.Integer, primary_key=True)
    driverId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    routeId = db.Column(db.Integer, db.ForeignKey('route.routeId'), nullable=True)
    schedudledTieme = db.Column(db.DateTime, nullable=True)

    def __init__(self, driverId, routeId=None, scheduledTime=None):
        self.driverId = driverId
        self.routeId = routeId
        self.scheduledTime = scheduledTime if scheduledTime else datetime.utcnow()



