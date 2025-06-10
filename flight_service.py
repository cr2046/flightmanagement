class FlightService:
    """
    handles flight operations

    manages adding flights, viewing them, updating info etc.
    the main flight management process.
    """

    def __init__(self, db_manager):
        """
        setup flight service
        """
        self.db_manager = db_manager
        self.conn, self.cur = db_manager.get_connection()

    def add_flight(self):
        """
        add new flight to system

        asks user for flight details and puts it in database.
        checks origin != destination before inserting
        """
        try:
            print("\n=== Add New Flight ===")
            flight_number = input("Enter flight number: ").upper()

            # show airlines
            self.cur.execute(
                "SELECT airline_id, airline_name, airline_code FROM Airlines")
            airlines = self.cur.fetchall()
            print("\nAvailable Airlines:")
            for airline in airlines:
                print(f"{airline[0]}. {airline[1]} ({airline[2]})")

            airline_id = int(input("\nEnter airline ID: "))

            # show destinations
            self.cur.execute(
                "SELECT destination_id, destination_name, airport_code FROM Destinations")
            destinations = self.cur.fetchall()
            print("\nAvailable Destinations:")
            for dest in destinations:
                print(f"{dest[0]}. {dest[1]} ({dest[2]})")

            origin_id = int(input("\nEnter origin destination ID: "))
            destination_id = int(input("Enter destination ID: "))

            if origin_id == destination_id:
                print("Origin and destination cannot be the same!")
                return

            departure_time = input("Enter departure time (YYYY-MM-DD HH:MM): ")
            arrival_time = input("Enter arrival time (YYYY-MM-DD HH:MM): ")
            aircraft_type = input("Enter aircraft type: ")
            capacity = int(input("Enter capacity: "))

            self.cur.execute('''
                INSERT INTO Flights (flight_number, airline_id, origin_id, destination_id, departure_time, arrival_time, aircraft_type, capacity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (flight_number, airline_id, origin_id, destination_id, departure_time, arrival_time, aircraft_type, capacity))

            self.conn.commit()
            print("Flight added successfully!")

        except Exception as e:
            print(f"Error adding flight: {e}")

    def view_flights_by_criteria(self):
        """
        view flights with different filters

        multiple options for filtering - all flights, by destination,
        status, date range or pilot. uses JOINs to show proper info
        """
        try:
            print("\n=== View Flights ===")
            print("1. All flights")
            print("2. By destination")
            print("3. By status")
            print("4. By date range")
            print("5. By pilot")

            choice = int(input("Choose filter option: "))

            if choice == 1:
                query = '''
                    SELECT f.flight_number, a.airline_name, o.destination_name as origin, d.destination_name as destination,
                           GROUP_CONCAT(p.first_name || ' ' || p.last_name || ' (' || fa.role || ')') as crew,
                           f.departure_time, f.arrival_time, f.status
                    FROM Flights f
                    JOIN Airlines a ON f.airline_id = a.airline_id
                    JOIN Destinations o ON f.origin_id = o.destination_id
                    JOIN Destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN Flight_assignments fa ON f.flight_id = fa.flight_id AND fa.status = 'Active'
                    LEFT JOIN Pilots p ON fa.pilot_id = p.pilot_id
                    GROUP BY f.flight_id, f.flight_number, a.airline_name, o.destination_name, d.destination_name, f.departure_time, f.arrival_time, f.status
                    ORDER BY f.departure_time
                '''
                self.cur.execute(query)

            elif choice == 2:
                self.cur.execute(
                    "SELECT destination_id, destination_name FROM Destinations")
                destinations = self.cur.fetchall()
                print("\nDestinations:")
                for dest in destinations:
                    print(f"{dest[0]}. {dest[1]}")

                dest_id = int(input("Enter destination ID: "))
                query = '''
                    SELECT f.flight_number, a.airline_name, o.destination_name as origin, d.destination_name as destination,
                           GROUP_CONCAT(p.first_name || ' ' || p.last_name || ' (' || fa.role || ')') as crew,
                           f.departure_time, f.arrival_time, f.status
                    FROM Flights f
                    JOIN Airlines a ON f.airline_id = a.airline_id
                    JOIN Destinations o ON f.origin_id = o.destination_id
                    JOIN Destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN Flight_assignments fa ON f.flight_id = fa.flight_id AND fa.status = 'Active'
                    LEFT JOIN Pilots p ON fa.pilot_id = p.pilot_id
                    WHERE f.destination_id = ?
                    GROUP BY f.flight_id, f.flight_number, a.airline_name, o.destination_name, d.destination_name, f.departure_time, f.arrival_time, f.status
                    ORDER BY f.departure_time
                '''
                self.cur.execute(query, (dest_id,))

            elif choice == 3:
                status = input(
                    "Enter status (Scheduled/Delayed/Cancelled/Completed/In-Flight): ")
                query = '''
                    SELECT f.flight_number, a.airline_name, o.destination_name as origin, d.destination_name as destination,
                           GROUP_CONCAT(p.first_name || ' ' || p.last_name || ' (' || fa.role || ')') as crew,
                           f.departure_time, f.arrival_time, f.status
                    FROM Flights f
                    JOIN Airlines a ON f.airline_id = a.airline_id
                    JOIN Destinations o ON f.origin_id = o.destination_id
                    JOIN Destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN Flight_assignments fa ON f.flight_id = fa.flight_id AND fa.status = 'Active'
                    LEFT JOIN Pilots p ON fa.pilot_id = p.pilot_id
                    WHERE f.status = ?
                    GROUP BY f.flight_id, f.flight_number, a.airline_name, o.destination_name, d.destination_name, f.departure_time, f.arrival_time, f.status
                    ORDER BY f.departure_time
                '''
                self.cur.execute(query, (status,))

            elif choice == 4:
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                query = '''
                    SELECT f.flight_number, a.airline_name, o.destination_name as origin, d.destination_name as destination,
                           GROUP_CONCAT(p.first_name || ' ' || p.last_name || ' (' || fa.role || ')') as crew,
                           f.departure_time, f.arrival_time, f.status
                    FROM Flights f
                    JOIN Airlines a ON f.airline_id = a.airline_id
                    JOIN Destinations o ON f.origin_id = o.destination_id
                    JOIN Destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN Flight_assignments fa ON f.flight_id = fa.flight_id AND fa.status = 'Active'
                    LEFT JOIN Pilots p ON fa.pilot_id = p.pilot_id
                    WHERE DATE(f.departure_time) BETWEEN ? AND ?
                    GROUP BY f.flight_id, f.flight_number, a.airline_name, o.destination_name, d.destination_name, f.departure_time, f.arrival_time, f.status
                    ORDER BY f.departure_time
                '''
                self.cur.execute(query, (start_date, end_date))

            elif choice == 5:
                self.cur.execute(
                    "SELECT pilot_id, first_name, last_name FROM Pilots")
                pilots = self.cur.fetchall()
                print("\nPilots:")
                for pilot in pilots:
                    print(f"{pilot[0]}. {pilot[1]} {pilot[2]}")

                pilot_id = int(input("Enter pilot ID: "))
                query = '''
                    SELECT f.flight_number, a.airline_name, o.destination_name as origin, d.destination_name as destination,
                           GROUP_CONCAT(p.first_name || ' ' || p.last_name || ' (' || fa.role || ')') as crew,
                           f.departure_time, f.arrival_time, f.status
                    FROM Flights f
                    JOIN Airlines a ON f.airline_id = a.airline_id
                    JOIN Destinations o ON f.origin_id = o.destination_id
                    JOIN Destinations d ON f.destination_id = d.destination_id
                    LEFT JOIN Flight_assignments fa ON f.flight_id = fa.flight_id AND fa.status = 'Active'
                    LEFT JOIN Pilots p ON fa.pilot_id = p.pilot_id
                    WHERE fa.pilot_id = ?
                    GROUP BY f.flight_id, f.flight_number, a.airline_name, o.destination_name, d.destination_name, f.departure_time, f.arrival_time, f.status
                    ORDER BY f.departure_time
                '''
                self.cur.execute(query, (pilot_id,))

            results = self.cur.fetchall()
            self._display_flight_results(results)

        except Exception as e:
            print(f"Error viewing flights: {e}")

    def update_flight(self):
        """
        update flight details

        can change departure time, arrival time or status.
        user picks flight by number then what to update
        """
        try:
            print("\n=== Update Flight ===")
            flight_number = input("Enter flight number to update: ").upper()

            # check flight exists
            self.cur.execute(
                "SELECT * FROM Flights WHERE flight_number = ?", (flight_number,))
            flight = self.cur.fetchone()

            if not flight:
                print("Flight not found!")
                return

            print("\nWhat would you like to update?")
            print("1. Departure time")
            print("2. Arrival time")
            print("3. Status")

            choice = int(input("Choose option: "))

            if choice == 1:
                new_time = input(
                    "Enter new departure time (YYYY-MM-DD HH:MM): ")
                self.cur.execute(
                    "UPDATE Flights SET departure_time = ? WHERE flight_number = ?", (new_time, flight_number))
            elif choice == 2:
                new_time = input("Enter new arrival time (YYYY-MM-DD HH:MM): ")
                self.cur.execute(
                    "UPDATE Flights SET arrival_time = ? WHERE flight_number = ?", (new_time, flight_number))
            elif choice == 3:
                new_status = input(
                    "Enter new status (Scheduled/Delayed/Cancelled/Completed/In-Flight): ")
                self.cur.execute(
                    "UPDATE Flights SET status = ? WHERE flight_number = ?", (new_status, flight_number))

            self.conn.commit()
            print("Flight updated successfully!")

        except Exception as e:
            print(f"Error updating flight: {e}")

    def _display_flight_results(self, results):
        """
        shows flight results in table format

        displays flight info in columns. handles empty results
        """
        if results:
            print(f"\n{'Flight':<10} {'Airline':<15} {'Origin':<15} {'Destination':<15} {'Crew':<30} {'Departure':<20} {'Arrival':<20} {'Status':<12}")
            print("-" * 140)
            for row in results:
                crew = row[4] if row[4] else "No crew assigned"
                print(
                    f"{row[0]:<10} {row[1]:<15} {row[2]:<15} {row[3]:<15} {crew:<30} {row[5]:<20} {row[6]:<20} {row[7]:<12}")
        else:
            print("No flights found matching the criteria.")
