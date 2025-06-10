# Flight Management System

## What it does
Basic flight management system for my database coursework. Manages flights, pilots and destinations for airlines using SQLite database.

## How to run it
1. Make sure you have Python 3 installed
2. Navigate to the project folder
3. Run: `python main.py`
4. The database will be created automatically with sample data

## Files
- `main.py` - starts the program
- `database.py` - handles SQLite database stuff
- `*_service.py` - business logic for flights, pilots, destinations, reports
- `ui.py` - command line interface
- `models.py` - data classes and sample data
- `seed_database.py` - utility for resetting database

## Database Tables
The system has 5 main tables:

### Airlines
- airline_id (primary key)
- airline_name, airline_code, country, headquarters
- fleet_size, established_year

### Destinations  
- destination_id (primary key)
- destination_name, country, airport_code, timezone

### Pilots
- pilot_id (primary key) 
- first_name, last_name, license_number
- experience_years, hire_date, airline_id (foreign key)
- status (Active/Inactive/On Leave)

### Flights
- flight_id (primary key)
- flight_number, airline_id (foreign key)
- origin_id, destination_id (foreign keys to Destinations)
- departure_time, arrival_time, status
- aircraft_type, capacity

### Flight_assignments
- assignment_id (primary key)
- flight_id, pilot_id (foreign keys)
- role (Captain/First Officer/Relief Pilot)
- assignment_date, status

## Features
The menu lets you:
1. Add new flights
2. View flights (all or filtered by destination/status/date/pilot)
3. Update flight info (times, status)
4. Assign pilots to flights
5. View pilot schedules
6. Manage destinations (view/add/update)
7. Generate reports
8. Exit

## Sample Data
Comes with realistic test data:
- 10 airlines (BA, Air France, Lufthansa etc.)
- 30 airports worldwide 
- 25 pilots with different experience levels
- 50 flights with proper routes and schedules
- Crew assignments

## Key SQL Queries
The system uses various SQL operations:

**View all flights with details:**
```sql
SELECT f.flight_number, a.airline_name, o.destination_name as origin, 
       d.destination_name as destination, f.departure_time, f.status
FROM Flights f
JOIN Airlines a ON f.airline_id = a.airline_id
JOIN Destinations o ON f.origin_id = o.destination_id  
JOIN Destinations d ON f.destination_id = d.destination_id
```

**Pilot workload report:**
```sql
SELECT p.first_name || ' ' || p.last_name as pilot_name, 
       COUNT(fa.flight_id) as flight_count
FROM Pilots p
LEFT JOIN Flight_assignments fa ON p.pilot_id = fa.pilot_id
GROUP BY p.pilot_id
```

**Flight status summary:**
```sql
SELECT status, COUNT(*) as count
FROM Flights 
GROUP BY status
ORDER BY count DESC
```

## Database Management
Reset database: `python seed_database.py --reset`
View stats: `python seed_database.py --stats`

## Requirements
- Python 3.6+
- SQLite3 (comes with Python)
- No external dependencies needed

## Notes
This was built for the Database & Cloud computing module. The system demonstrates:
- Relational database design with proper normalisation
- Foreign key constraints and referential integrity
- Complex SQL queries with JOINs and aggregations
- Python database programming with sqlite3
- Command line interface design
- Modular code architecture

The sample data includes realistic airline routes like LHR-JFK, CDG-MAD etc. with proper IATA airport codes and flight durations.