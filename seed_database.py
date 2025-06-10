#!/usr/bin/env python3
"""
Database Seeding Script for Flight Management System

This script does data seeding including:
- Fresh database setup
- Additional data population  
- Data validation and stats
- Bulk operations

Usage:
    python seed_database.py [--reset] [--stats] [--additional]
"""

import sqlite3
import os
import argparse
from datetime import datetime, timedelta
import random
from models import SampleData


class DatabaseSeeder:
    """
    database seeding and management class

    handles database reset, data population, statistics etc.
    for testing and development
    """

    def __init__(self, db_name="FlightManagement.db"):
        """
        setup database seeder
        """
        self.db_name = db_name
        self.conn = None
        self.cur = None

    def connect(self):
        """
        connect to sqlite database
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
            print(f"Connected to database: {self.db_name}")
        except Exception as e:
            print(f"Database connection error: {e}")

    def reset_database(self):
        """
        reset database by dropping and recreating tables

        completely wipes database and recreates with fresh schema.
        useful for testing when you need clean slate
        """
        try:
            print("Resetting database...")

            # drop tables
            self.cur.execute("DROP TABLE IF EXISTS Flights")
            self.cur.execute("DROP TABLE IF EXISTS Pilots")
            self.cur.execute("DROP TABLE IF EXISTS Destinations")

            # recreate
            self.create_tables()
            print("Database reset completed")

        except Exception as e:
            print(f"Error resetting database: {e}")

    def create_tables(self):
        """
        create database tables with proper schema

        creates the 3 main tables with appropriate constraints and foreign keys
        """
        try:
            # destinations
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

            # pilots
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Pilots (
                    pilot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    license_number TEXT NOT NULL UNIQUE,
                    experience_years INTEGER NOT NULL,
                    hire_date DATE NOT NULL,
                    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'On Leave'))
                )
            ''')

            # flights
            self.cur.execute('''
                CREATE TABLE IF NOT EXISTS Flights (
                    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_number TEXT NOT NULL UNIQUE,
                    origin_id INTEGER NOT NULL,
                    destination_id INTEGER NOT NULL,
                    pilot_id INTEGER,
                    departure_time DATETIME NOT NULL,
                    arrival_time DATETIME NOT NULL,
                    status TEXT DEFAULT 'Scheduled' CHECK(status IN ('Scheduled', 'Delayed', 'Cancelled', 'Completed', 'In-Flight')),
                    aircraft_type TEXT NOT NULL,
                    capacity INTEGER NOT NULL,
                    created_date DATE DEFAULT CURRENT_DATE,
                    FOREIGN KEY (origin_id) REFERENCES Destinations (destination_id),
                    FOREIGN KEY (destination_id) REFERENCES Destinations (destination_id),
                    FOREIGN KEY (pilot_id) REFERENCES Pilots (pilot_id)
                )
            ''')

            self.conn.commit()
            print("Tables created successfully")

        except Exception as e:
            print(f"Error creating tables: {e}")

    def seed_comprehensive_data(self):
        """
        seed database with sample data using SampleData class

        populates all tables with realistic data including destinations,
        pilots and flights. maintains referential integrity
        """
        try:
            sample_data = SampleData()

            print("Seeding comprehensive data...")

            # destinations
            destinations = sample_data.get_destinations()
            self.cur.executemany('''
                INSERT INTO Destinations (destination_name, country, airport_code, timezone)
                VALUES (?, ?, ?, ?)
            ''', destinations)
            print(f"✓ Inserted {len(destinations)} destinations")

            # pilots
            pilots = sample_data.get_pilots()
            self.cur.executemany('''
                INSERT INTO Pilots (first_name, last_name, license_number, experience_years, hire_date)
                VALUES (?, ?, ?, ?, ?)
            ''', pilots)
            print(f"✓ Inserted {len(pilots)} pilots")

            # flights
            flights = sample_data.get_flights()
            self.cur.executemany('''
                INSERT INTO Flights (flight_number, origin_id, destination_id, pilot_id, departure_time, arrival_time, status, aircraft_type, capacity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', flights)
            print(f"✓ Inserted {len(flights)} flights")

            self.conn.commit()
            print("Data seeding completed successfully!")

        except Exception as e:
            print(f"Error seeding data: {e}")

    def display_statistics(self):
        """
        display database statistics

        shows detailed stats about database contents including
        record counts, averages, distributions etc
        """
        try:
            print("\n" + "="*60)
            print("           DATABASE STATISTICS")
            print("="*60)

            # destinations stats
            self.cur.execute("SELECT COUNT(*) FROM Destinations")
            dest_count = self.cur.fetchone()[0]

            self.cur.execute(
                "SELECT COUNT(DISTINCT country) FROM Destinations")
            country_count = self.cur.fetchone()[0]

            print(
                f"Destinations: {dest_count} airports across {country_count} countries")

            # pilots stats
            self.cur.execute("SELECT COUNT(*) FROM Pilots")
            pilot_count = self.cur.fetchone()[0]

            self.cur.execute("SELECT AVG(experience_years) FROM Pilots")
            avg_experience = self.cur.fetchone()[0]

            print(
                f"Pilots: {pilot_count} pilots (avg. {avg_experience:.1f} years experience)")

            # flights stats
            self.cur.execute("SELECT COUNT(*) FROM Flights")
            flight_count = self.cur.fetchone()[0]

            self.cur.execute('''
                SELECT status, COUNT(*) as count 
                FROM Flights 
                GROUP BY status 
                ORDER BY count DESC
            ''')
            status_stats = self.cur.fetchall()

            print(f"Flights: {flight_count} total flights")
            print("Flight status distribution:")
            for status, count in status_stats:
                percentage = (count / flight_count) * 100
                print(f"  {status}: {count} ({percentage:.1f}%)")

            print("="*60)

        except Exception as e:
            print(f"Error displaying statistics: {e}")

    def close(self):
        """
        close database connection
        """
        if self.conn:
            self.conn.close()


def main():
    """
    main function with command line interface

    provides command line options for database operations:
    - --reset: reset database and seed fresh data
    - --stats: show database statistics
    - default: create tables and seed if empty
    """
    parser = argparse.ArgumentParser(
        description='Flight Management Database Seeder')
    parser.add_argument('--reset', action='store_true',
                        help='Reset database before seeding')
    parser.add_argument('--stats', action='store_true',
                        help='Display database statistics')

    args = parser.parse_args()

    seeder = DatabaseSeeder()
    seeder.connect()

    try:
        if args.reset:
            seeder.reset_database()
            seeder.seed_comprehensive_data()
        elif not args.stats:
            # default - seed if empty
            seeder.cur.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            if seeder.cur.fetchone()[0] == 0:
                seeder.create_tables()
                seeder.seed_comprehensive_data()
            else:
                print("Database already exists. Use --reset to recreate.")

        if args.stats:
            seeder.display_statistics()

    finally:
        seeder.close()


if __name__ == "__main__":
    main()
