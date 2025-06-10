import sqlite3
from models import SampleData


class DatabaseManager:
    """
    manages the SQLite database for the flight system

    handles connection, creating tables, populating data etc.
    basically the main database interface
    """

    def __init__(self, db_name="FlightManagement.db"):
        """
        sets up database manager

        creates connection and tables, adds sample data if empty
        """
        self.db_name = db_name
        self.conn = None
        self.cur = None
        self.connect()
        self.create_tables()

    def connect(self):
        """
        connect to sqlite database

        creates connection and cursor for running queries
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
            print("Database connected successfully")
        except Exception as e:
            print(f"Database connection error: {e}")

    def get_connection(self):
        """
        returns database connection

        reconnects if needed. used by service classes
        """
        if self.conn is None:
            self.connect()
        return self.conn, self.cur

    def create_tables(self):
        """
        creates all the tables for the system

        makes 5 tables: airlines, destinations, pilots, flights, flight_assignments
        with proper foreign keys and constraints. populates with sample data if empty.
        """
        try:
            # airlines table
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Airlines (
                    airline_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    airline_name TEXT NOT NULL UNIQUE,
                    airline_code TEXT NOT NULL UNIQUE,
                    country TEXT NOT NULL,
                    headquarters TEXT,
                    fleet_size INTEGER DEFAULT 0,
                    established_year INTEGER,
                    created_date DATE DEFAULT CURRENT_DATE
                )
            ''')

            # destinations table
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Destinations (
                    destination_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    destination_name TEXT NOT NULL UNIQUE,
                    country TEXT NOT NULL,
                    airport_code TEXT NOT NULL UNIQUE,
                    timezone TEXT NOT NULL,
                    created_date DATE DEFAULT CURRENT_DATE
                )
            ''')

            # pilots table
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Pilots (
                    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    license_number TEXT NOT NULL UNIQUE,
                    experience_years INTEGER NOT NULL,
                    hire_date DATE NOT NULL,
                    airline_id INTEGER,
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'On Leave')),
                    FOREIGN KEY (airline_id) REFERENCES Airlines (airline_id)
                )
            ''')

            # flights table
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Flights (
                    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_number TEXT NOT NULL UNIQUE,
                    airline_id INTEGER NOT NULL,
                    origin_id INTEGER NOT NULL,
                    destination_id INTEGER NOT NULL,
                    departure_time DATETIME NOT NULL,
                    arrival_time DATETIME NOT NULL,
                    status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Delayed', 'Cancelled', 'Completed', 'In-Flight')),
                    aircraft_type TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    created_date DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (airline_id) REFERENCES Airlines (airline_id),
                    FOREIGN KEY (origin_id) REFERENCES Destinations (destination_id),
                    FOREIGN KEY (destination_id) REFERENCES Destinations (destination_id)
                )
            ''')

            # flight assignments table
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Flight_assignments (
                    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_id INTEGER NOT NULL,
                    pilot_id INTEGER NOT NULL,
                    assignment_date DATE DEFAULT CURRENT_DATE,
                    role TEXT DEFAULT 'Captain' CHECK(role IN ('Captain', 'First Officer', 'Relief Pilot')),
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Cancelled', 'Completed')),
                    notes TEXT,
                    FOREIGN KEY (flight_id) REFERENCES Flights (flight_id),
                    FOREIGN KEY (pilot_id) REFERENCES Pilots (pilot_id),
                    UNIQUE(flight_id, pilot_id, role)
                )
            ''')

            self.conn.commit()
            print("All 5 tables created successfully")

            # populate with sample data if empty
            self.cur.execute("SELECT COUNT(*) FROM Airlines")
            if self.cur.fetchone()[0] == 0:
                self.populate_sample_data()

        except Exception as e:
            print(f"Error creating tables: {e}")

    def populate_sample_data(self):
        """
        fills tables with sample data for testing

        inserts realistic data using the SampleData class.
        includes airlines, destinations, pilots, flights and crew assignments
        """
        try:
            sample_data = SampleData()

            # insert airlines first (needed for foreign keys)
            self.cur.executemany('''
                INSERT INTO Airlines (airline_name, airline_code, country, headquarters, fleet_size, established_year)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_data.get_airlines())

            # destinations
            self.cur.executemany('''
                INSERT INTO Destinations (destination_name, country, airport_code, timezone)
                VALUES (?, ?, ?, ?)
            ''', sample_data.get_destinations())

            # pilots with airline assignments
            self.cur.executemany('''
                INSERT INTO Pilots (first_name, last_name, license_number, experience_years, hire_date, airline_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_data.get_pilots())

            # flights
            self.cur.executemany('''
                INSERT INTO Flights (flight_number, airline_id, origin_id, destination_id, departure_time, arrival_time, status, aircraft_type, capacity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_data.get_flights())

            # flight assignments
            self.cur.executemany('''
                INSERT INTO Flight_assignments (flight_id, pilot_id, assignment_date, role, status, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', sample_data.get_flight_assignments())

            self.conn.commit()
            print("Sample data populated successfully")
            print("- 10 airlines")
            print("- 30 destinations")
            print("- 25 pilots")
            print("- 50 flights")
            print("- crew assignments")

        except Exception as e:
            print(f"Error populating sample data: {e}")

    def close_connection(self):
        """
        closes database connection

        should be called when shutting down
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed")
