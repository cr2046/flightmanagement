class DestinationService:
    """
    handles destination stuff - basically manages airports and destinations

    This class manages destination management like adding new airports,
    viewing them, updating info etc. Acts as the middleware between the UI and database.

    Attributes:
        db_manager: the database manager thing
        conn: database connection
        cur: cursor for queries
    """

    def __init__(self, db_manager):
        """
        Sets up the destination service

        Args:
            db_manager: Database manager for doing database operations
        """
        self.db_manager = db_manager
        self.conn, self.cur = db_manager.get_connection()

    def manage_destinations(self):
        """
        Main menu for destination management

        Shows a menu with options to view, add or update destinations.

        Side Effects:
            - shows menu
            - calls other methods based on choice
            - handles errors if user types wrong thing
        """
        try:
            print("\n=== Destination Management ===")
            print("1. View all destinations")
            print("2. Add new destination")
            print("3. Update destination")

            choice = int(input("Choose option: "))

            if choice == 1:
                self.view_all_destinations()
            elif choice == 2:
                self.add_destination()
            elif choice == 3:
                self.update_destination()

        except Exception as e:
            print(f"Error managing destinations: {e}")

    def view_all_destinations(self):
        """
        displays all destinations in a table

        Gets all destination records from database and shows them in a table
        with ID, name, country, airport code and timezone. Sorted alphabetically.

        """
        try:
            self.cur.execute(
                "SELECT * FROM Destinations ORDER BY destination_name")
            destinations = self.cur.fetchall()

            print(
                f"\n{'ID':<5} {'Name':<25} {'Country':<20} {'Code':<8} {'Timezone':<10}")
            print("-" * 75)
            for dest in destinations:
                print(
                    f"{dest[0]:<5} {dest[1]:<25} {dest[2]:<20} {dest[3]:<8} {dest[4]:<10}")

        except Exception as e:
            print(f"Error viewing destinations: {e}")

    def add_destination(self):
        """
        Add new destination to system

        Asks user for destination details and inserts it in the database.
        Airport code gets converted to uppercase automatically.

        User needs to enter:
            - destination name
            - country 
            - airport code (3 letters)
            - timezone

        """
        try:
            name = input("Enter destination name: ")
            country = input("Enter country: ")
            code = input("Enter airport code: ").upper()
            timezone = input("Enter timezone: ")

            self.cur.execute('''
                INSERT INTO Destinations (destination_name, country, airport_code, timezone)
                VALUES (?, ?, ?, ?)
            ''', (name, country, code, timezone))
            self.conn.commit()
            print("Destination added successfully!")

        except Exception as e:
            print(f"Error adding destination: {e}")

    def update_destination(self):
        """
        Update existing destination info

        lets user change destination details. They pick the destination by ID
        then choose what field to update.

        Can update:
            - name
            - country
            - code (gets uppercased)
            - timezone
        """
        try:
            self.cur.execute(
                "SELECT destination_id, destination_name FROM Destinations")
            destinations = self.cur.fetchall()
            print("\nDestinations:")
            for dest in destinations:
                print(f"{dest[0]}. {dest[1]}")

            dest_id = int(input("Enter destination ID to update: "))
            field = input(
                "Enter field to update (name/country/code/timezone): ").lower()
            new_value = input("Enter new value: ")

            if field == "name":
                self.cur.execute(
                    "UPDATE Destinations SET destination_name = ? WHERE destination_id = ?",
                    (new_value, dest_id))
            elif field == "country":
                self.cur.execute(
                    "UPDATE Destinations SET country = ? WHERE destination_id = ?",
                    (new_value, dest_id))
            elif field == "code":
                self.cur.execute(
                    "UPDATE Destinations SET airport_code = ? WHERE destination_id = ?",
                    (new_value.upper(), dest_id))
            elif field == "timezone":
                self.cur.execute(
                    "UPDATE Destinations SET timezone = ? WHERE destination_id = ?",
                    (new_value, dest_id))

            self.conn.commit()
            print("Destination updated successfully!")

        except Exception as e:
            print(f"Error updating destination: {e}")

    def get_all_destinations(self):
        """
        Gets all destinations for other parts of the system

        Returns basic destination info that other services need

        Returns:
            list of tuples with (destination_id, destination_name, airport_code)
        """
        try:
            self.cur.execute(
                "SELECT destination_id, destination_name, airport_code FROM Destinations")
            return self.cur.fetchall()
        except Exception as e:
            print(f"Error retrieving destinations: {e}")
            return []
