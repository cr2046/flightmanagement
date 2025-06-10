class ReportService:
    """
    generates reports and analytics

    does various reports like flight stats, pilot workloads,
    destination traffic etc. basic business intelligence stuff
    """

    def __init__(self, db_manager):
        """
        setup report service
        """
        self.db_manager = db_manager
        self.conn, self.cur = db_manager.get_connection()

    def generate_reports(self):
        """
        main report menu

        shows different report options and routes to the right one
        """
        try:
            print("\n=== Reports ===")
            print("1. Flights per destination")
            print("2. Flights per pilot")
            print("3. Flight status summary")
            print("4. Busiest routes")

            choice = int(input("Choose report: "))

            if choice == 1:
                self.flights_per_destination_report()
            elif choice == 2:
                self.flights_per_pilot_report()
            elif choice == 3:
                self.flight_status_summary_report()
            elif choice == 4:
                self.busiest_routes_report()

        except Exception as e:
            print(f"Error generating reports: {e}")

    def flights_per_destination_report(self):
        """
        shows how many flights go to each destination

        uses LEFT JOIN to include destinations with zero flights.
        sorted by flight count highest first
        """
        try:
            self.cur.execute('''
                SELECT d.destination_name, COUNT(f.flight_id) as flight_count
                FROM Destinations d
                LEFT JOIN Flights f ON d.destination_id = f.destination_id
                GROUP BY d.destination_id, d.destination_name
                ORDER BY flight_count DESC
            ''')
            results = self.cur.fetchall()

            print(f"\n{'Destination':<25} {'Flight Count':<12}")
            print("-" * 40)
            for row in results:
                print(f"{row[0]:<25} {row[1]:<12}")

        except Exception as e:
            print(f"Error generating destination report: {e}")

    def flights_per_pilot_report(self):
        """
        pilot workload report

        shows how many flights each pilot is assigned to.
        includes pilots with zero assignments
        """
        try:
            self.cur.execute('''
                SELECT p.first_name || ' ' || p.last_name as pilot_name, COUNT(fa.flight_id) as flight_count
                FROM Pilots p
                LEFT JOIN Flight_assignments fa ON p.pilot_id = fa.pilot_id AND fa.status = 'Active'
                GROUP BY p.pilot_id, pilot_name
                ORDER BY flight_count DESC
            ''')
            results = self.cur.fetchall()

            print(f"\n{'Pilot':<25} {'Flight Count':<12}")
            print("-" * 40)
            for row in results:
                print(f"{row[0]:<25} {row[1]:<12}")

        except Exception as e:
            print(f"Error generating pilot report: {e}")

    def flight_status_summary_report(self):
        """
        flight status breakdown

        shows count of flights in each status (scheduled, delayed etc)
        """
        try:
            self.cur.execute('''
                SELECT status, COUNT(*) as count
                FROM Flights
                GROUP BY status
                ORDER BY count DESC
            ''')
            results = self.cur.fetchall()

            print(f"\n{'Status':<15} {'Count':<8}")
            print("-" * 25)
            for row in results:
                print(f"{row[0]:<15} {row[1]:<8}")

        except Exception as e:
            print(f"Error generating status report: {e}")

    def busiest_routes_report(self):
        """
        busiest routes analysis

        finds most popular routes by counting flight frequency.
        shows top 10 routes only
        """
        try:
            self.cur.execute('''
                SELECT o.destination_name || ' → ' || d.destination_name as route, COUNT(*) as count
                FROM Flights f
                JOIN Destinations o ON f.origin_id = o.destination_id
                JOIN Destinations d ON f.destination_id = d.destination_id
                GROUP BY route
                ORDER BY count DESC
                LIMIT 10
            ''')
            results = self.cur.fetchall()

            print(f"\n{'Route':<40} {'Flight Count':<12}")
            print("-" * 55)
            for row in results:
                print(f"{row[0]:<40} {row[1]:<12}")

        except Exception as e:
            print(f"Error generating routes report: {e}")
