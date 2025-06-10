class UserInterface:
    """
    Main UI class for the flight management system

    handles the command line interface and menus. coordinates between
    all the different service classes
    """

    def __init__(self, flight_service, pilot_service, destination_service, report_service):
        """
        setup UI with all the services
        """
        self.flight_service = flight_service
        self.pilot_service = pilot_service
        self.destination_service = destination_service
        self.report_service = report_service

    def display_main_menu(self):
        """
        shows the main menu

        prints out all the available options for the flight management system
        """
        print("\n" + "="*50)
        print("        FLIGHT MANAGEMENT SYSTEM")
        print("="*50)
        print("1.  Add New Flight")
        print("2.  View Flights by Criteria")
        print("3.  Update Flight Information")
        print("4.  Assign Pilot to Flight")
        print("5.  View Pilot Schedule")
        print("6.  Manage Destinations")
        print("7.  Generate Reports")
        print("8.  Exit")
        print("="*50)

    def handle_menu_choice(self, choice):
        """
        Handle what the user picked from menu

        calls the right service method based on what user chose.
        has error handling for wrong choices.

        Args:
            choice: the number the user entered

        Returns:
            True to keep going, False to exit
        """
        try:
            if choice == 1:
                self.flight_service.add_flight()
            elif choice == 2:
                self.flight_service.view_flights_by_criteria()
            elif choice == 3:
                self.flight_service.update_flight()
            elif choice == 4:
                self.pilot_service.assign_pilot_to_flight()
            elif choice == 5:
                self.pilot_service.view_pilot_schedule()
            elif choice == 6:
                self.destination_service.manage_destinations()
            elif choice == 7:
                self.report_service.generate_reports()
            elif choice == 8:
                return False  # Exit
            else:
                print("Invalid choice! Please enter a number between 1-8.")

            return True  # Continue

        except ValueError:
            print("Invalid input! Please enter a valid number.")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return True

    def run(self):
        """
        main application loop

        keeps showing menu and processing choices until user exits.
        handles input errors and keeps going.
        """
        while True:
            self.display_main_menu()

            try:
                choice = int(input("Enter your choice (1-8): "))

                if not self.handle_menu_choice(choice):
                    print("Thank you for using Flight Management System!")
                    break

            except ValueError:
                print("Invalid input! Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {e}")

            input("\nPress Enter to continue...")

    def get_user_input(self, prompt, input_type=str, validation_func=None):
        """
        helper for getting user input with validation

        keeps asking until user enters something valid. can convert to int/float
        and apply custom validation.

        Args:
            prompt: what to ask the user
            input_type: str, int or float
            validation_func: function to check if input is valid

        Returns:
            the validated input
        """
        while True:
            try:
                user_input = input(prompt)

                # convert to right type
                if input_type == int:
                    user_input = int(user_input)
                elif input_type == float:
                    user_input = float(user_input)

                # check validation if provided
                if validation_func and not validation_func(user_input):
                    print("Invalid input. Please try again.")
                    continue

                return user_input

            except ValueError:
                print(f"Invalid input type. Expected {input_type.__name__}.")
            except Exception as e:
                print(f"Error: {e}")

    def confirm_action(self, message):
        """
        get yes/no confirmation from user

        asks user to confirm an action. accepts y/yes or n/no (case insensitive)

        Args:
            message: what to ask the user

        Returns:
            True if yes, False if no
        """
        while True:
            response = input(f"{message} (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'.")
