# user.py - CORRECTED VERSION
from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    
    # Single Table Inheritance discriminator
    type = db.Column(db.String(50))
    
    # Driver-specific columns (nullable for non-drivers)
    driverId = db.Column(db.Integer, unique=True, nullable=True)
    driver_name = db.Column(db.String(50), nullable=True)  # Changed from driverName
    status = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=False, nullable=True)  # Added
    route_id = db.Column(db.Integer, db.ForeignKey('route.routeId'), nullable=True)  # Added
    
    # Resident-specific columns (nullable for non-residents)
    residentId = db.Column(db.Integer, unique=True, nullable=True)
    name = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'type': self.type
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
