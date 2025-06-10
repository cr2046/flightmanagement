#!/usr/bin/env python3
"""
Flight Management System - Main Entry Point

basic flight management system with command line interface
for managing flights, pilots and destinations for airlines

simple layered architecture:
- UI layer: UserInterface 
- Business logic: Service classes
- Data layer: DatabaseManager
- Models: data classes

Author: Student
Version: 2.0
"""

from database import DatabaseManager
from flight_service import FlightService
from pilot_service import PilotService
from destination_service import DestinationService
from report_service import ReportService
from ui import UserInterface


def main():
    """
    main function - starts the flight management system

    sets up all the components and starts the UI.
    handles errors during startup
    """
    try:
        # setup database
        print("Initialising Flight Management System...")
        db_manager = DatabaseManager()

        # setup services
        flight_service = FlightService(db_manager)
        pilot_service = PilotService(db_manager)
        destination_service = DestinationService(db_manager)
        report_service = ReportService(db_manager)

        # setup UI
        ui = UserInterface(flight_service, pilot_service,
                           destination_service, report_service)

        # start app
        print("System initialised successfully!")
        ui.run()

    except Exception as e:
        print(f"Fatal error: {e}")
        print("Application could not start. Please check your configuration.")

    finally:
        # cleanup
        try:
            db_manager.close_connection()
        except:
            pass


if __name__ == "__main__":
    main()
