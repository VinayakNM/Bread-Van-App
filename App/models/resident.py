from App.database import db
from App.models.user import User
from App.models.stopRequest import StopRequests
from App.models.driver import Driver

# resident.py - CORRECTED VERSION
from App.database import db
from App.models.user import User

class Resident(User):
    __tablename__ = None  # Use parent table
    
    __mapper_args__ = {
        'polymorphic_identity': 'resident'
    }
    
    def __init__(self, username, password, name=None, address=None):
        super().__init__(username, password)
        self.name = name or username
        self.address = address or 'No address provided'
        
        # Generate unique residentId
        last_resident = Resident.query.order_by(User.residentId.desc()).first()
        self.residentId = (last_resident.residentId + 1) if last_resident and last_resident.residentId else 1

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'address': self.address
        }

    def requestStop(self, time):
        newRequest = StopRequests(location=self.address, time=time, residentId=self.id)
        db.session.add(newRequest)
        db.session.commit()
        return newRequest
  
    def cancelStopRequest(self, requestId):
        request = StopRequests.query.filter_by(id=requestId, residentId=self.id).first()
        if request:
            db.session.delete(request)
            db.session.commit()
            return True
        return False
    
    def trackDriverLocationandStatus(self, driverId):
        driver = Driver.query.get(driverId)
        if driver:
            return {"location": driver.currentLocation, "status": driver.status}
        return None