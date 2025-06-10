from datetime import datetime, timedelta
import random


class SampleData:
    """
    Generates sample data for the flight management system

    Creates realistic test data for airlines, destinations, pilots and flights.
    Includes proper relationships between tables.
    """

    def get_airlines(self):
        """
        Returns list of airline data

        10 major airlines with codes, countries, fleet sizes etc.
        """
        return [
            ('British Airways', 'BA', 'United Kingdom', 'London', 280, 1974),
            ('Air France', 'AF', 'France', 'Paris', 220, 1933),
            ('Lufthansa', 'LH', 'Germany', 'Frankfurt', 300, 1953),
            ('American Airlines', 'AA', 'United States', 'Dallas', 950, 1930),
            ('Emirates', 'EK', 'UAE', 'Dubai', 270, 1985),
            ('Singapore Airlines', 'SQ', 'Singapore', 'Singapore', 130, 1947),
            ('Japan Airlines', 'JL', 'Japan', 'Tokyo', 170, 1951),
            ('KLM', 'KL', 'Netherlands', 'Amsterdam', 110, 1919),
            ('Swiss International', 'LX', 'Switzerland', 'Zurich', 90, 2002),
            ('Turkish Airlines', 'TK', 'Turkey', 'Istanbul', 380, 1933)
        ]

    def get_destinations(self):
        """
        Sample destinations data

        30 major international airports with IATA codes and timezones
        """
        return [
            # Major International Hubs
            ('London Heathrow', 'United Kingdom', 'LHR', 'GMT'),
            ('New York JFK', 'United States', 'JFK', 'EST'),
            ('Paris Charles de Gaulle', 'France', 'CDG', 'CET'),
            ('Tokyo Haneda', 'Japan', 'HND', 'JST'),
            ('Dubai International', 'UAE', 'DXB', 'GST'),
            ('Los Angeles International', 'United States', 'LAX', 'PST'),
            ('Frankfurt am Main', 'Germany', 'FRA', 'CET'),
            ('Singapore Changi', 'Singapore', 'SIN', 'SGT'),
            ('Sydney Kingsford Smith', 'Australia', 'SYD', 'AEST'),
            ('Amsterdam Schiphol', 'Netherlands', 'AMS', 'CET'),

            # Additional Major Airports
            ('Hong Kong International', 'Hong Kong', 'HKG', 'HKT'),
            ('Madrid Barajas', 'Spain', 'MAD', 'CET'),
            ('Rome Fiumicino', 'Italy', 'FCO', 'CET'),
            ('Mumbai Chhatrapati Shivaji', 'India', 'BOM', 'IST'),
            ('Toronto Pearson', 'Canada', 'YYZ', 'EST'),
            ('Seoul Incheon', 'South Korea', 'ICN', 'KST'),
            ('Bangkok Suvarnabhumi', 'Thailand', 'BKK', 'ICT'),
            ('Istanbul Airport', 'Turkey', 'IST', 'TRT'),
            ('Moscow Sheremetyevo', 'Russia', 'SVO', 'MSK'),
            ('São Paulo Guarulhos', 'Brazil', 'GRU', 'BRT'),

            # Regional airports
            ('Berlin Brandenburg', 'Germany', 'BER', 'CET'),
            ('Vienna International', 'Austria', 'VIE', 'CET'),
            ('Zurich Airport', 'Switzerland', 'ZUR', 'CET'),
            ('Copenhagen Airport', 'Denmark', 'CPH', 'CET'),
            ('Stockholm Arlanda', 'Sweden', 'ARN', 'CET'),
            ('Oslo Gardermoen', 'Norway', 'OSL', 'CET'),
            ('Dublin Airport', 'Ireland', 'DUB', 'GMT'),
            ('Brussels Airport', 'Belgium', 'BRU', 'CET'),
            ('Barcelona El Prat', 'Spain', 'BCN', 'CET'),
            ('Milan Malpensa', 'Italy', 'MXP', 'CET')
        ]

    def get_pilots(self):
        """
        pilot data with different experience levels

        25 pilots from new hires to senior captains, assigned to different airlines
        """
        return [
            # Senior Captains (15+ years)
            ('John', 'Smith', 'PIL001', 20, '2003-03-15', 1),
            ('Sarah', 'Johnson', 'PIL002', 18, '2005-07-22', 1),
            ('David', 'Wilson', 'PIL003', 22, '2001-11-30', 2),
            ('Michelle', 'White', 'PIL004', 16, '2007-10-08', 2),
            ('Daniel', 'Lewis', 'PIL005', 25, '1998-01-12', 3),
            ('Robert', 'Taylor', 'PIL006', 19, '2004-06-12', 3),
            ('Jennifer', 'Martinez', 'PIL007', 17, '2006-08-25', 4),

            # Experienced pilots (8-14 years)
            ('Michael', 'Brown', 'PIL008', 12, '2011-01-10', 4),
            ('Emily', 'Davis', 'PIL009', 14, '2009-09-05', 5),
            ('William', 'Garcia', 'PIL010', 11, '2012-02-14', 5),
            ('James', 'Lee', 'PIL011', 13, '2010-05-20', 6),
            ('Lisa', 'Anderson', 'PIL012', 10, '2013-04-18', 6),
            ('Christopher', 'Thompson', 'PIL013', 9, '2014-12-01', 7),
            ('Angela', 'Moore', 'PIL014', 8, '2015-03-22', 7),

            # Junior pilots
            ('Amanda', 'Rodriguez', 'PIL015', 6, '2017-12-03', 8),
            ('Christopher', 'Harris', 'PIL016', 5, '2018-09-15', 8),
            ('Jessica', 'Clark', 'PIL017', 4, '2019-03-27', 9),
            ('Kevin', 'Young', 'PIL018', 7, '2016-08-14', 9),
            ('Rachel', 'Scott', 'PIL019', 3, '2020-05-30', 10),
            ('Mark', 'Turner', 'PIL020', 4, '2019-11-18', 10),

            # New pilots
            ('Sophie', 'Adams', 'PIL021', 2, '2021-09-10', 1),
            ('Ryan', 'Cooper', 'PIL022', 1, '2022-04-05', 2),
            ('Emma', 'Parker', 'PIL023', 2, '2021-07-20', 3),
            ('Nathan', 'Brooks', 'PIL024', 1, '2022-01-15', 4),
            ('Olivia', 'Bennett', 'PIL025', 2, '2021-03-08', 5)
        ]

    def get_flights(self):
        """
        generates realistic flight data

        Creates 50 flights with proper routes, times, aircraft etc.
        includes transatlantic, european and asian routes with realistic durations
        """
        # realistic flight routes with durations
        popular_routes = [
            # Transatlantic Routes
            (1, 2, 8, 1),   # LHR -> JFK (8 hours) - BA
            (2, 1, 7, 1),   # JFK -> LHR (7 hours) - BA
            (3, 2, 8, 2),   # CDG -> JFK (8 hours) - Air France
            (6, 1, 11, 1),  # LAX -> LHR (11 hours) - BA
            (1, 6, 11, 1),  # LHR -> LAX (11 hours) - BA

            # European Routes
            (1, 3, 1, 1),   # LHR -> CDG (1 hour) - BA
            (3, 1, 1, 2),   # CDG -> LHR (1 hour) - Air France
            (1, 7, 1, 3),   # LHR -> FRA (1 hour) - Lufthansa
            (7, 1, 1, 3),   # FRA -> LHR (1 hour) - Lufthansa
            (3, 12, 2, 2),  # CDG -> MAD (2 hours) - Air France
            (12, 13, 2, 2),  # MAD -> FCO (2 hours) - Air France
            (10, 7, 1, 8),  # AMS -> FRA (1 hour) - KLM

            # Asian Routes
            (4, 8, 7, 7),   # HND -> SIN (7 hours) - JAL
            (8, 4, 7, 6),   # SIN -> HND (7 hours) - Singapore Airlines
            (4, 11, 3, 7),  # HND -> HKG (3 hours) - JAL
            (11, 4, 4, 6),  # HKG -> HND (4 hours) - Singapore Airlines
            (8, 5, 7, 5),   # SIN -> DXB (7 hours) - Emirates
            (5, 8, 7, 5),   # DXB -> SIN (7 hours) - Emirates

            # Long-haul routes
            (1, 9, 22, 1),  # LHR -> SYD (22 hours)
            (9, 1, 21, 1),  # SYD -> LHR (21 hours)
            (5, 14, 3, 5),  # DXB -> BOM (3 hours)
            (14, 5, 3, 5),  # BOM -> DXB (3 hours)
            (2, 15, 1, 4),  # JFK -> YYZ (1 hour)
            (15, 2, 1, 4),  # YYZ -> JFK (1 hour)

            # regional routes
            (7, 10, 1, 3),  # FRA -> AMS (1 hour)
            (10, 21, 1, 8),  # AMS -> BER (1 hour)
            (21, 22, 1, 3),  # BER -> VIE (1 hour)
            (22, 23, 1, 3),  # VIE -> ZUR (1 hour)
            (3, 29, 1, 2),  # CDG -> BCN (1 hour)
            (29, 30, 1, 2)  # BCN -> MXP (1 hour)
        ]

        aircraft_types = [
            'Boeing 737-800', 'Boeing 737 MAX 8', 'Airbus A320', 'Airbus A321',
            'Boeing 777-300ER', 'Boeing 787-9', 'Airbus A350-900', 'Airbus A380',
            'Boeing 747-8F', 'Embraer E190'
        ]

        # capacity for each aircraft type
        aircraft_capacity = {
            'Boeing 737-800': 189, 'Boeing 737 MAX 8': 210, 'Airbus A320': 180,
            'Airbus A321': 220, 'Boeing 777-300ER': 396, 'Boeing 787-9': 290,
            'Airbus A350-900': 325, 'Airbus A380': 525, 'Boeing 747-8F': 467,
            'Embraer E190': 114
        }

        statuses = ['Scheduled', 'Delayed',
                    'Completed', 'In-Flight', 'Cancelled']
        status_weights = [0.5, 0.2, 0.25, 0.03, 0.02]  # realistic distribution

        flights = []
        base_time = datetime.now()

        # Generate 50 flights with realistic scheduling
        for i in range(50):
            flight_num = f"BA{2000 + i}" if i < 10 else f"AF{3000 + (i-10)}" if i < 20 else f"LH{4000 + (i-20)}" if i < 30 else f"AA{5000 + (i-30)}" if i < 40 else f"EK{6000 + (i-40)}"

            # pick route
            if i < len(popular_routes):
                origin_id, dest_id, duration, airline_id = popular_routes[i]
            else:
                # random route for remaining flights
                origin_id = random.randint(1, 30)
                dest_id = random.randint(1, 30)
                while dest_id == origin_id:
                    dest_id = random.randint(1, 30)
                duration = random.randint(1, 15)
                airline_id = random.randint(1, 10)

            # assign pilot
            pilot_id = random.randint(1, 25)

            # realistic departure times
            days_offset = random.randint(-7, 30)  # past week to next month
            hour = random.choice([6, 8, 10, 12, 14, 16, 18, 20, 22])
            minute = random.choice([0, 15, 30, 45])

            departure = base_time.replace(
                hour=hour, minute=minute, second=0, microsecond=0) + timedelta(days=days_offset)
            arrival = departure + \
                timedelta(hours=duration, minutes=random.randint(0, 45))

            # select aircraft
            aircraft = random.choice(aircraft_types)
            capacity = aircraft_capacity[aircraft]

            # status based on timing
            if departure < base_time - timedelta(hours=2):
                status = 'Completed'
            elif departure < base_time + timedelta(hours=2) and departure > base_time - timedelta(hours=2):
                status = random.choice(['In-Flight', 'Delayed'])
            else:
                status = random.choices(statuses, weights=status_weights)[0]

            flights.append((flight_num, airline_id, origin_id, dest_id,
                           departure.strftime('%Y-%m-%d %H:%M:%S'),
                           arrival.strftime('%Y-%m-%d %H:%M:%S'),
                           status, aircraft, capacity))

        return flights

    def get_flight_assignments(self):
        """
        crew assignments for flights

        each flight gets a captain, most also get first officers
        """
        assignments = []
        base_date = datetime.now().date()

        # assignments for flights 1-30
        for flight_id in range(1, 31):
            # each flight gets a captain
            captain_id = random.randint(1, 25)
            assignments.append(
                (flight_id, captain_id, base_date, 'Captain', 'Active', None))

            # 70% chance of first officer
            if random.random() < 0.7:
                first_officer_id = random.randint(1, 25)
                while first_officer_id == captain_id:  # different pilot
                    first_officer_id = random.randint(1, 25)
                assignments.append(
                    (flight_id, first_officer_id, base_date, 'First Officer', 'Active', None))

        return assignments

    def get_additional_sample_data(self):
        """
        additional data for testing

        Returns dict with all the sample data
        """
        return {
            'destinations': self.get_destinations(),
            'pilots': self.get_pilots(),
            'flights': self.get_flights()
        }


class Flight:
    """
    represents a flight

    basic flight entity with route info, timing, status etc
    """

    def __init__(self, flight_id=None, flight_number=None, origin_id=None,
                 destination_id=None, pilot_id=None, departure_time=None,
                 arrival_time=None, status='Scheduled', aircraft_type=None, capacity=None):
        """
        create flight object
        """
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.pilot_id = pilot_id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.status = status
        self.aircraft_type = aircraft_type
        self.capacity = capacity


class Pilot:
    """
    pilot class

    stores pilot info like name, licence, experience etc
    """

    def __init__(self, pilot_id=None, first_name=None, last_name=None,
                 license_number=None, experience_years=None, hire_date=None, status='Active'):
        """init pilot"""
        self.pilot_id = pilot_id
        self.first_name = first_name
        self.last_name = last_name
        self.license_number = license_number
        self.experience_years = experience_years
        self.hire_date = hire_date
        self.status = status


class Destination:
    """
    airport/destination class

    has airport info like name, country, IATA code etc
    """

    def __init__(self, destination_id=None, destination_name=None, country=None,
                 airport_code=None, timezone=None):
        """
        setup destination object
        """
        self.destination_id = destination_id
        self.destination_name = destination_name
        self.country = country
        self.airport_code = airport_code
        self.timezone = timezone
