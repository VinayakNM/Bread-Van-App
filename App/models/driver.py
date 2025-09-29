from App.database import db
from App.models.user import User
from App.models.schedule import Schedule
from App.models.stopRequest import StopRequests


class Driver(User):
    __tablename__ = None  # Use parent table
    
    __mapper_args__ = {
        'polymorphic_identity': 'driver'
    }
    
    def __init__(self, username, password, driver_name=None, location=None):
        super().__init__(username, password)
        self.driver_name = driver_name or username  # Consistent naming
        self.location = location or 'Unknown'
        self.status = 'available'
        self.is_active = False
        self.route_id = None
        
        # Generate unique driverId
        last_driver = Driver.query.order_by(User.driverId.desc()).first()
        self.driverId = (last_driver.driverId + 1) if last_driver and last_driver.driverId else 1

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'driver_name': self.driver_name,
            'location': self.location,
            'status': self.status,
            'is_active': self.is_active,
            'route_id': self.route_id
        }


    

    def scheduleRoute(self, resident):
        schedule = Schedule(driverId=self.driverId, residentId=resident.residentId, street=resident.address)
        db.session.add(schedule)
        db.session.commit()
        print(f"Driver {self.username} scheduled route to {resident.address}")
        return schedule
    
    def acceptStopRequest(self, requestId):
        request = StopRequests.query.filter_by(id=requestId).first()
        if request and request.status == 'pending':
            request.status = 'accepted'
            db.session.commit()
            print(f"Driver {self.username} accepted stop request {requestId}")
            return True
        else:
            print(f"Driver {self.username} could not accept stop request {requestId}")
            return False
    
    def updateLocationandStatus(self, newLocation, newStatus):
        prevLocation = self.location
        prevStatus = self.status
        self.location = newLocation
        self.status = newStatus
        db.session.commit()
        print(f"Driver {self.username} updated location from {prevLocation} to {newLocation} and status from {prevStatus} to {newStatus}")
        return True