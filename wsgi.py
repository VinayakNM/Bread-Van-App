import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User,route
from App.models.driver import Driver
from App.models.resident import Resident

from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
        # Add street names during initialization
    streetNames = ["Maple Street", "Oak Avenue", "Pine Lane", "Cedar Road", "Birch Boulevard", "Ash Drive"]
    
    try:
        # Add routes
        for name in streetNames:
            if not route.Route.query.filter_by(streetName=name).first():
                newRoute = route.Route(streetName=name)
                db.session.add(newRoute)
        
        # Populate the database with 5 drivers
        drivers = [
            {"username": "driver1", "password": "Johnpass123", "name": "John Smith", "location": "Downtown"},
            {"username": "driver2", "password": "Sarahpass123", "name": "Sarah Jones", "location": "Uptown"}, 
            {"username": "driver3", "password": "Mikepass123", "name": "Mike Johnson", "location": "Westside"},
            {"username": "driver4", "password": "Lisapass123", "name": "Lisa Brown", "location": "Eastside"},
            {"username": "driver5", "password": "Tompass123", "name": "Tom Wilson", "location": "Southside"}
        ]
        
        for driver_data in drivers:
            if not User.query.filter_by(username=driver_data["username"]).first():
                driver = Driver(
                    username=driver_data["username"],
                    password=driver_data["password"],
                    driver_name=driver_data["name"],
                    location=driver_data["location"]
                )
                db.session.add(driver)
        
        #Populate the database with 10 residents
        residents = [
            {"username": "resident1", "password": "Alicepass123", "name": "Alice Johnson", "address": "123 Maple Street"},
            {"username": "resident2", "password": "Bobpass123", "name": "Bob Davis", "address": "456 Oak Avenue"},
            {"username": "resident3", "password": "Carolpass123", "name": "Carol Miller", "address": "789 Pine Lane"},
            {"username": "resident4", "password": "Davidpass123", "name": "David Garcia", "address": "321 Cedar Road"},
            {"username": "resident5", "password": "Emmapass123", "name": "Emma Wilson", "address": "654 Birch Boulevard"},
            {"username": "resident6", "password": "Frankpass123", "name": "Frank Lee", "address": "987 Ash Drive"},
            {"username": "resident7", "password": "Gracepass123", "name": "Grace Chen", "address": "147 Maple Street"},
            {"username": "resident8", "password": "Henrypass123", "name": "Henry Taylor", "address": "258 Oak Avenue"},
            {"username": "resident9", "password": "Ivypass123", "name": "Ivy Rodriguez", "address": "369 Pine Lane"},
            {"username": "resident10", "password": "Jackpass123", "name": "Jack Martinez", "address": "741 Cedar Road"}
        ]
        
        for resident_data in residents:
            if not User.query.filter_by(username=resident_data["username"]).first():
                resident = Resident(
                    username=resident_data["username"],
                    password=resident_data["password"],
                    name=resident_data["name"],
                    address=resident_data["address"]
                )
                db.session.add(resident)
        
        db.session.commit()
        print('Database initialized with routes, 5 drivers, and 10 residents!')
        
    except Exception as e:
        print(f'Error initializing: {str(e)}')
        db.session.rollback()



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------





'''
User Commands
'''
user_cli = AppGroup('user', help='User object commands') 

@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    try:
        if format == 'string':
            drivers = Driver.query.all()
            residents = Resident.query.all()
            
            result = "--- ALL USERS ---\n"
            result += f"Drivers ({len(drivers)}):\n"
            for driver in drivers:
                result += f"  ID: {driver.driverId} | {driver.username} - {driver.driver_name} ({driver.location})\n"
            
            result += f"\nResidents ({len(residents)}):\n"
            for resident in residents:
                result += f"  ID: {resident.residentId} | {resident.username} - {resident.name} at {resident.address}\n"
            
            print(result)
        else:
            drivers = [driver.get_json() for driver in Driver.query.all()]
            residents = [resident.get_json() for resident in Resident.query.all()]
            
            import json
            result = {
                'drivers': drivers,
                'residents': residents,
                'total_drivers': len(drivers),
                'total_residents': len(residents)
            }
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f'Error listing users: {str(e)}')


app.cli.add_command(user_cli)




#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



'''
Route Commands
'''
route_cli = AppGroup('route', help='Route management commands')

@route_cli.command("list", help="View all available routes")    #list all available routes that a driver can take
def list_routes_command():
    """Display all routes in the database"""
    try:
        routes = route.Route.query.all()
        if routes:
            print(f"\n--- AVAILABLE ROUTES ({len(routes)} total) ---")
            print("-" * 40)
            for r in routes:
                print(f"ID: {r.routeId} - {r.streetName}")
            print("-" * 40)
        else:
            print("No routes found in the database.")
    except Exception as e:
        print(f'Error listing routes: {str(e)}')

app.cli.add_command(route_cli)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



'''
Driver Commands
'''
driver_cli = AppGroup('driver', help='Driver management commands')

@driver_cli.command("select-route", help="Allow a driver to select their route")    #gives the driver a choice of routes to take to schedule a drive to a street
@click.argument("driver_id", type=int)
def select_route_command(driver_id):
    """Allow a driver to select from available routes using driver ID"""
    try:
        driver = Driver.query.filter_by(driverId=driver_id).first()
        if not driver:
            print(f"Driver with ID '{driver_id}' not found!")
            return
        
        routes = route.Route.query.all()
        if not routes:
            print("No routes available in the database.")
            return
        
        print(f"\nHello {driver.driver_name} (ID: {driver.driverId})!")
        print("Please choose your route:")
        print("-" * 40)
        
        for i, r in enumerate(routes, 1):
            print(f"{i}. {r.streetName} (ID: {r.routeId})")
        
        print("-" * 40)
        
        while True:
            try:
                choice = input(f"Enter your choice (1-{len(routes)}): ")
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(routes):
                    selected_route = routes[choice_num - 1]
                    
                    driver.route_id = selected_route.routeId
                    driver.is_active = True
                    db.session.commit()
                    
                    print(f"\nRoute assigned successfully!")
                    print(f"Driver: {driver.driver_name} (ID: {driver.driverId})")
                    print(f"Route: {selected_route.streetName}")
                    print(f"Status: Active")
                    print("\nResidents on this street can now see you in their inbox!")
                    break
                else:
                    print(f"Please enter a number between 1 and {len(routes)}")
                    
            except ValueError:
                print("Please enter a valid number")
            except KeyboardInterrupt:
                print("\nRoute selection cancelled.")
                return
                
    except Exception as e:
        print(f'Error selecting route: {str(e)}')
        db.session.rollback()

@driver_cli.command("status", help="Toggle driver active/inactive status")      #allows the driver to update their status to active or inactive
@click.argument("driver_id", type=int)
def toggle_status_command(driver_id):
    """Toggle driver's active status using driver ID"""
    try:
        driver = Driver.query.filter_by(driverId=driver_id).first()
        if not driver:
            print(f"Driver with ID '{driver_id}' not found!")
            return
        
        driver.is_active = not driver.is_active
        db.session.commit()
        
        status = "Active" if driver.is_active else "Inactive"
        print(f"\nDriver {driver.driver_name} (ID: {driver.driverId}) is now {status}")
        
        if driver.is_active and driver.route_id:
            assigned_route = route.Route.query.get(driver.route_id)
            if assigned_route:
                print(f"Route: {assigned_route.streetName}")
        
    except Exception as e:
        print(f'Error updating status: {str(e)}')
        db.session.rollback()       


app.cli.add_command(driver_cli)



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




'''
Resident Commands
'''
resident_cli = AppGroup('resident', help='Resident management commands')

@resident_cli.command("inbox", help="View scheduled delivery drivers for resident's street")    #shows residents the drivers scheduled for thier street only
@click.argument("resident_id", type=int)
def view_inbox_command(resident_id):
    """Show scheduled drivers for the resident's street using resident ID"""
    try:
        resident = Resident.query.filter_by(residentId=resident_id).first()
        if not resident:
            print(f"Resident with ID '{resident_id}' not found!")
            return
        
        address_parts = resident.address.split()
        street_name = " ".join(address_parts[1:])
        
        street_route = route.Route.query.filter_by(streetName=street_name).first()
        if not street_route:
            print(f"No route found for street: {street_name}")
            return
        
        assigned_drivers = Driver.query.filter_by(route_id=street_route.routeId).all()
        
        print(f"\nINBOX for {resident.name} (ID: {resident.residentId}) at {resident.address}")
        print("=" * 70)
        print(f"Street Route: {street_route.streetName}")
        print("-" * 70)
        
        if assigned_drivers:
            print("SCHEDULED DELIVERY DRIVERS:")
            for i, driver in enumerate(assigned_drivers, 1):
                print(f"{i}. Driver: {driver.driver_name} (ID: {driver.driverId})")
                print(f"   Status: {'Active' if driver.is_active else 'Inactive'}")
                print(f"   Current Location: {driver.location}")
                print("-" * 40)
        else:
            print("No drivers currently scheduled for your street.")
            
    except Exception as e:
        print(f'Error viewing inbox: {str(e)}')

@resident_cli.command("request-stop", help="Request a stop from a specific driver")     #allows to the resident to request a stop in advance from a driver assigned to their street
@click.argument("resident_id", type=int)
@click.argument("driver_id", type=int)
def request_stop_command(resident_id, driver_id):
    """Allow resident to request a delivery stop from a driver using IDs"""
    try:
        resident = Resident.query.filter_by(residentId=resident_id).first()
        if not resident:
            print(f"Resident with ID '{resident_id}' not found!")
            return
        
        driver = Driver.query.filter_by(driverId=driver_id).first()
        if not driver:
            print(f"Driver with ID '{driver_id}' not found!")
            return
        
        address_parts = resident.address.split()
        street_name = " ".join(address_parts[1:])
        street_route = route.Route.query.filter_by(streetName=street_name).first()
        
        if street_route and driver.route_id != street_route.routeId:
            print(f"Driver {driver.driver_name} (ID: {driver.driverId}) is not assigned to your street ({street_name})")
            return
        
        print(f"\nDELIVERY REQUEST")
        print(f"From: {resident.name} (ID: {resident.residentId}) at {resident.address}")
        print(f"To Driver: {driver.driver_name} (ID: {driver.driverId})")
        print("-" * 50)
        
        items_requested = input("What items would you like to request? : ")
        special_instructions = input("Any special delivery instructions? (optional): ")
        
        print(f"\nSTOP REQUEST SUBMITTED")
        print("=" * 50)
        print(f"Resident: {resident.name} (ID: {resident.residentId})")
        print(f"Address: {resident.address}")
        print(f"Driver: {driver.driver_name} (ID: {driver.driverId})")
        print(f"Items: {items_requested}")
        if special_instructions:
            print(f"Instructions: {special_instructions}")
        print(f"Status: Pending")
        print("=" * 50)
        print(f"Your request has been sent to {driver.driver_name}!")
        
    except Exception as e:
        print(f'Error requesting stop: {str(e)}')

@resident_cli.command("track-driver", help="View driver status and location")
@click.argument("resident_id", type=int)
@click.argument("driver_id", type=int, required=False)
def track_driver_command(resident_id, driver_id=None):
    """Track driver status and location for resident's street using IDs"""
    try:
        resident = Resident.query.filter_by(residentId=resident_id).first()
        if not resident:
            print(f"Resident with ID '{resident_id}' not found!")
            return
        
        address_parts = resident.address.split()
        street_name = " ".join(address_parts[1:])
        street_route = route.Route.query.filter_by(streetName=street_name).first()
        
        print(f"\nDRIVER TRACKING for {resident.name} (ID: {resident.residentId})")
        print(f"Your Location: {resident.address}")
        print("=" * 60)
        
        if driver_id:
            driver = Driver.query.filter_by(driverId=driver_id).first()
            if not driver:
                print(f"Driver with ID '{driver_id}' not found!")
                return
                
            print(f"TRACKING: {driver.driver_name} (ID: {driver.driverId})")
            print("-" * 40)
            print(f"Status: {'Active' if driver.is_active else 'Inactive'}")
            print(f"Current Location: {driver.location}")
            print(f"Route: {street_route.streetName if street_route and driver.route_id == street_route.routeId else 'Not on your street'}")
            
        else:
            if not street_route:
                print(f"No route found for {street_name}")
                return
                
            drivers_on_street = Driver.query.filter_by(route_id=street_route.routeId).all()
            
            if drivers_on_street:
                print(f"ALL DRIVERS ON {street_route.streetName}:")
                print("-" * 50)
                for driver in drivers_on_street:
                    status_icon = "Active" if driver.is_active else "Inactive"
                    print(f"ID: {driver.driverId} | {driver.driver_name} - {status_icon}")
                    print(f"   Location: {driver.location}")
                    print(f"   Username: {driver.username}")
                    print("-" * 25)
            else:
                print(f"No drivers currently assigned to {street_name}")
        
        print("\nTip: Use 'flask resident request-stop <resident_id> <driver_id>' to request a delivery!")
        
    except Exception as e:
        print(f'Error tracking driver: {str(e)}')


app.cli.add_command(resident_cli)



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




'''
Test Commands
'''
test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)