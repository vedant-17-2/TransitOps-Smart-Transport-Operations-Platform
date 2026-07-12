import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction

from accounts.models import UserProfile
from fleet.models import Vehicle
from drivers.models import Driver
from trips.models import Trip
from maintenance.models import MaintenanceRecord
from fuel.models import FuelLog, Expense

class Command(BaseCommand):
    help = 'Sets up demo data for TransitOps'

    def handle(self, *args, **kwargs):
        if Vehicle.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists. Skipping demo setup.'))
            return

        with transaction.atomic():
            self.setup_users()
            self.setup_vehicles()
            self.setup_drivers()
            self.setup_trips()
            self.setup_maintenance()
            self.setup_fuel_and_expenses()
            
            self.stdout.write(self.style.SUCCESS('Successfully populated database with demo data.'))

    def setup_users(self):
        # Admin
        User.objects.create_superuser('admin', 'admin@transitops.com', 'admin123', first_name='Admin', last_name='User')
        
        # Staff users
        users_data = [
            ('fleet_mgr', 'pass123', 'Fleet', 'Manager', UserProfile.Role.FLEET_MANAGER),
            ('dispatcher', 'pass123', 'Operations', 'Dispatcher', UserProfile.Role.DISPATCHER),
            ('safety_off', 'pass123', 'Safety', 'Officer', UserProfile.Role.SAFETY_OFFICER),
            ('finance', 'pass123', 'Financial', 'Analyst', UserProfile.Role.FINANCIAL_ANALYST),
        ]
        
        for username, password, first, last, role in users_data:
            user = User.objects.create_user(username=username, email=f"{username}@transitops.com", password=password, first_name=first, last_name=last)
            # Profile is auto-created by signal, just update role
            profile = user.profile
            profile.role = role
            profile.save()
            
        self.stdout.write(self.style.SUCCESS('Users created.'))

    def setup_vehicles(self):
        vehicles_data = [
            ('MH-12-AB-1234', 'Tata Prima', Vehicle.VehicleType.TRUCK, 15, 45000, 2500000, Vehicle.Status.AVAILABLE),
            ('MH-14-CD-5678', 'Ashok Leyland', Vehicle.VehicleType.TRUCK, 20, 78000, 3200000, Vehicle.Status.AVAILABLE),
            ('KA-01-EF-9012', 'Mahindra Bolero Pickup', Vehicle.VehicleType.PICKUP, 1.5, 32000, 850000, Vehicle.Status.AVAILABLE),
            ('DL-02-GH-3456', 'Force Traveller', Vehicle.VehicleType.BUS, 3, 56000, 1800000, Vehicle.Status.AVAILABLE),
            ('GJ-05-IJ-7890', 'Eicher Pro', Vehicle.VehicleType.TRUCK, 12, 91000, 2100000, Vehicle.Status.AVAILABLE),
            ('TN-07-KL-2345', 'Tata Ace', Vehicle.VehicleType.VAN, 1, 23000, 600000, Vehicle.Status.ON_TRIP),
            ('RJ-14-MN-6789', 'BharatBenz Truck', Vehicle.VehicleType.TRUCK, 25, 120000, 4500000, Vehicle.Status.ON_TRIP),
            ('MH-04-OP-1357', 'Mahindra Furio', Vehicle.VehicleType.TRUCK, 18, 67000, 2800000, Vehicle.Status.IN_SHOP),
            ('UP-32-QR-2468', 'Tata Signa', Vehicle.VehicleType.TRUCK, 22, 145000, 3800000, Vehicle.Status.IN_SHOP),
            ('PB-10-ST-1359', 'Swaraj Mazda', Vehicle.VehicleType.TRUCK, 10, 210000, 1200000, Vehicle.Status.RETIRED),
        ]
        for reg, name, v_type, cap, odo, cost, status in vehicles_data:
            Vehicle.objects.create(registration_number=reg, vehicle_name=name, vehicle_type=v_type, capacity=cap, current_odometer=odo, acquisition_cost=cost, status=status)
        self.stdout.write(self.style.SUCCESS('Vehicles created.'))

    def setup_drivers(self):
        now = timezone.now().date()
        drivers_data = [
            ('Rajesh Kumar', 'DL-0420231234', Driver.LicenseCategory.HMV, now + timedelta(days=500), '9876543210', 95, Driver.Status.AVAILABLE),
            ('Suresh Patil', 'MH-1220221567', Driver.LicenseCategory.HTV, now + timedelta(days=200), '9876543211', 88, Driver.Status.AVAILABLE),
            ('Amit Singh', 'DL-0920241890', Driver.LicenseCategory.HMV, now + timedelta(days=800), '9876543212', 92, Driver.Status.AVAILABLE),
            ('Vikram Sharma', 'KA-0120232345', Driver.LicenseCategory.HGMV, now + timedelta(days=450), '9876543213', 78, Driver.Status.AVAILABLE),
            ('Manoj Yadav', 'GJ-0520226789', Driver.LicenseCategory.HMV, now + timedelta(days=120), '9876543214', 85, Driver.Status.ON_TRIP),
            ('Deepak Verma', 'TN-0720231012', Driver.LicenseCategory.HTV, now + timedelta(days=600), '9876543215', 72, Driver.Status.ON_TRIP),
            ('Sanjay Gupta', 'RJ-1420223456', Driver.LicenseCategory.HMV, now - timedelta(days=100), '9876543216', 60, Driver.Status.ON_LEAVE),
            ('Ravi Tiwari', 'UP-3220237890', Driver.LicenseCategory.HGMV, now - timedelta(days=300), '9876543217', 45, Driver.Status.SUSPENDED),
        ]
        for name, lic, cat, exp, phone, score, status in drivers_data:
            Driver.objects.create(name=name, license_number=lic, license_category=cat, license_expiry=exp, phone=phone, safety_score=score, status=status)
        self.stdout.write(self.style.SUCCESS('Drivers created.'))

    def setup_trips(self):
        now = timezone.now()
        admin_user = User.objects.get(username='admin')
        
        # Available pool
        avail_vehicles = list(Vehicle.objects.filter(status=Vehicle.Status.AVAILABLE))
        avail_drivers = list(Driver.objects.filter(status=Driver.Status.AVAILABLE))
        
        # On Trip pool
        trip_vehicles = list(Vehicle.objects.filter(status=Vehicle.Status.ON_TRIP))
        trip_drivers = list(Driver.objects.filter(status=Driver.Status.ON_TRIP))
        
        routes = [
            ('Mumbai', 'Pune', 150),
            ('Delhi', 'Jaipur', 280),
            ('Bangalore', 'Chennai', 350),
            ('Hyderabad', 'Vijayawada', 275),
            ('Ahmedabad', 'Surat', 260),
            ('Kolkata', 'Bhubaneswar', 440)
        ]

        # Completed Trips (3)
        for i in range(3):
            route = random.choice(routes)
            v = random.choice(avail_vehicles)
            d = random.choice(avail_drivers)
            start = now - timedelta(days=random.randint(10, 30))
            end = start + timedelta(days=random.randint(1, 3))
            Trip.objects.create(vehicle=v, driver=d, source=route[0], destination=route[1], cargo_weight=float(v.capacity) * 0.8, distance=route[2], status=Trip.Status.COMPLETED, start_date=start, end_date=end, created_by=admin_user)

        # Dispatched (3) - use the On Trip vehicles/drivers
        for i in range(min(3, len(trip_vehicles))):
            route = random.choice(routes)
            Trip.objects.create(vehicle=trip_vehicles[i], driver=trip_drivers[i], source=route[0], destination=route[1], cargo_weight=float(trip_vehicles[i].capacity) * 0.9, distance=route[2], status=Trip.Status.DISPATCHED, start_date=now - timedelta(hours=2), created_by=admin_user)
            
        # In Progress (3) - reuse available (but would be on_trip logically)
        for i in range(3):
            if i < len(avail_vehicles) and i < len(avail_drivers):
                route = random.choice(routes)
                v = avail_vehicles[i]
                d = avail_drivers[i]
                # Logically we should change their status to ON_TRIP, but keeping simple for demo
                Trip.objects.create(vehicle=v, driver=d, source=route[0], destination=route[1], cargo_weight=float(v.capacity) * 0.7, distance=route[2], status=Trip.Status.IN_PROGRESS, start_date=now - timedelta(days=1), created_by=admin_user)

        # Pending (3)
        for i in range(3):
            route = random.choice(routes)
            Trip.objects.create(vehicle=random.choice(avail_vehicles), driver=random.choice(avail_drivers), source=route[0], destination=route[1], cargo_weight=1, distance=route[2], status=Trip.Status.PENDING, start_date=now + timedelta(days=2), created_by=admin_user)

        # Cancelled (2)
        for i in range(2):
            route = random.choice(routes)
            Trip.objects.create(vehicle=random.choice(avail_vehicles), driver=random.choice(avail_drivers), source=route[0], destination=route[1], cargo_weight=1, distance=route[2], status=Trip.Status.CANCELLED, start_date=now - timedelta(days=5), created_by=admin_user)

        self.stdout.write(self.style.SUCCESS('Trips created.'))

    def setup_maintenance(self):
        now = timezone.now().date()
        in_shop = list(Vehicle.objects.filter(status=Vehicle.Status.IN_SHOP))
        all_vehicles = list(Vehicle.objects.all())
        
        m_types = [c[0] for c in MaintenanceRecord.MaintenanceType.choices]
        
        # Open (2)
        for i in range(min(2, len(in_shop))):
            MaintenanceRecord.objects.create(vehicle=in_shop[i], maintenance_type=random.choice(m_types), description='Regular checkup', cost=5000, date=now - timedelta(days=random.randint(1, 5)), status=MaintenanceRecord.Status.OPEN)
            
        # Completed (3)
        for i in range(3):
            v = random.choice(all_vehicles)
            start = now - timedelta(days=random.randint(10, 60))
            MaintenanceRecord.objects.create(vehicle=v, maintenance_type=random.choice(m_types), description='Fixed issues', cost=random.randint(1000, 15000), date=start, status=MaintenanceRecord.Status.COMPLETED, completed_date=start + timedelta(days=2))

        self.stdout.write(self.style.SUCCESS('Maintenance records created.'))

    def setup_fuel_and_expenses(self):
        now = timezone.now().date()
        all_vehicles = list(Vehicle.objects.all())
        
        # Fuel Logs (20)
        for i in range(20):
            v = random.choice(all_vehicles)
            qty = random.randint(30, 200)
            cost = qty * 100 # Approx 100 Rs/L
            date = now - timedelta(days=random.randint(1, 90))
            FuelLog.objects.create(vehicle=v, fuel_quantity=qty, cost=cost, date=date)
            
        # Expenses (15)
        e_types = [c[0] for c in Expense.ExpenseType.choices]
        for i in range(15):
            v = random.choice(all_vehicles)
            e_type = random.choice(e_types)
            amount = random.randint(500, 50000)
            date = now - timedelta(days=random.randint(1, 90))
            Expense.objects.create(vehicle=v, expense_type=e_type, amount=amount, date=date, description=f'{e_type} expense')

        self.stdout.write(self.style.SUCCESS('Fuel logs and expenses created.'))
