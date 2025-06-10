class PilotService:
    """
    handles pilot processing and data

    manages pilot assignments to flights, viewing schedules etc.

    """

    def __init__(self, db_manager):
        """
        setup pilot service with database manager
        """
        self.db_manager = db_manager
        self.conn, self.cur = db_manager.get_connection()

    def assign_pilot_to_flight(self):
        """
        assign pilot to a flight

        shows available flights and pilots, lets user assign them.
        creates entry in flight_assignments table.
        """
        try:
            print("\n=== Assign Pilot to Flight ===")

            # show flights
            self.cur.execute('''
                SELECT f.flight_id, f.flight_number, a.airline_name, o.destination_name, d.destination_name, f.departure_time
                FROM Flights f
                JOIN Airlines a ON f.airline_id = a.airline_id
                JOIN Destinations o ON f.origin_id = o.destination_id
                JOIN Destinations d ON f.destination_id = d.destination_id
                ORDER BY f.departure_time
            ''')
            flights = self.cur.fetchall()

            print("\nAvailable Flights:")
            for flight in flights:
                print(
                    f"{flight[0]}. {flight[1]} ({flight[2]}) - {flight[3]} to {flight[4]} ({flight[5]})")

            flight_id = int(input("\nEnter flight ID: "))

            # show pilots
            self.cur.execute(
                "SELECT pilot_id, first_name, last_name, experience_years FROM Pilots WHERE status = 'Active'")
            pilots = self.cur.fetchall()
            print("\nAvailable Pilots:")
            for pilot in pilots:
                print(
                    f"{pilot[0]}. {pilot[1]} {pilot[2]} ({pilot[3]} years experience)")

            pilot_id = int(input("\nEnter pilot ID: "))

            # pick role
            print("\nAvailable Roles:")
            print("1. Captain")
            print("2. First Officer")
            print("3. Relief Pilot")
            role_choice = int(input("Choose role (1-3): "))

            roles = {1: 'Captain', 2: 'First Officer', 3: 'Relief Pilot'}
            role = roles.get(role_choice, 'Captain')

            # check if pilot already assigned
            self.cur.execute(
                "SELECT COUNT(*) FROM Flight_assignments WHERE flight_id = ? AND pilot_id = ? AND role = ? AND status = 'Active'",
                (flight_id, pilot_id, role))

            if self.cur.fetchone()[0] > 0:
                print("This pilot is already assigned to this flight with this role!")
                return

            # insert assignment
            self.cur.execute('''
                INSERT INTO Flight_assignments (flight_id, pilot_id, role, status)
                VALUES (?, ?, ?, 'Active')
            ''', (flight_id, pilot_id, role))

            self.conn.commit()
            print(f"Pilot assigned successfully as {role}!")

        except Exception as e:
            print(f"Error assigning pilot: {e}")

    def view_pilot_schedule(self):
        """
        view schedule for a pilot

        shows all flights assigned to selected pilot with route info,
        times, status and their role
        """
        try:
            print("\n=== Pilot Schedule ===")

            # show pilots
            self.cur.execute(
                "SELECT pilot_id, first_name, last_name FROM Pilots")
            pilots = self.cur.fetchall()
            print("\nPilots:")
            for pilot in pilots:
                print(f"{pilot[0]}. {pilot[1]} {pilot[2]}")

            pilot_id = int(input("\nEnter pilot ID: "))

            # get pilot's flights
            self.cur.execute('''
                SELECT f.flight_number, a.airline_name, o.destination_name as origin, d.destination_name as destination,
                       f.departure_time, f.arrival_time, f.status, fa.role, fa.status as assignment_status
                FROM Flight_assignments fa
                JOIN Flights f ON fa.flight_id = f.flight_id
                JOIN Airlines a ON f.airline_id = a.airline_id
                JOIN Destinations o ON f.origin_id = o.destination_id
                JOIN Destinations d ON f.destination_id = d.destination_id
                WHERE fa.pilot_id = ? AND fa.status = 'Active'
                ORDER BY f.departure_time
            ''', (pilot_id,))

            flights = self.cur.fetchall()

            if flights:
                print(
                    f"\n{'Flight':<10} {'Airline':<15} {'Route':<30} {'Departure':<20} {'Arrival':<20} {'Status':<12} {'Role':<15}")
                print("-" * 125)
                for flight in flights:
                    route = f"{flight[2]} → {flight[3]}"
                    print(
                        f"{flight[0]:<10} {flight[1]:<15} {route:<30} {flight[4]:<20} {flight[5]:<20} {flight[6]:<12} {flight[7]:<15}")
            else:
                print("No flights assigned to this pilot.")

        except Exception as e:
            print(f"Error viewing pilot schedule: {e}")

    def get_all_pilots(self):
        """
        get list of all pilots

        returns all pilot records for other parts of system to use
        """
        try:
            self.cur.execute(
                "SELECT pilot_id, first_name, last_name, license_number, experience_years, hire_date, status FROM Pilots")
            return self.cur.fetchall()
        except Exception as e:
            print(f"Error retrieving pilots: {e}")
            return []

    def get_active_pilots(self):
        """
        gets only active pilots

        Returns pilots with Active status for flight assignments
        """
        try:
            self.cur.execute(
                "SELECT pilot_id, first_name, last_name, experience_years FROM Pilots WHERE status = 'Active'")
            return self.cur.fetchall()
        except Exception as e:
            print(f"Error retrieving active pilots: {e}")
            return []
