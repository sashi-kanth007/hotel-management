Hotel Management System

This is a Hotel Management System built using Python Flask as the back-end framework. The application allows administrators to add hotel details, manage admin details, search for hotels, add customer details, and book hotels. This system is designed to streamline the hotel booking process and efficiently manage hotel information.

Features

1. Admin Management:
   - Add, update, and delete admin details.
   - Secure admin login and authentication.

2. Hotel Management:
   - Add new hotel details including name, location, amenities, room types, and pricing.
   - Update and delete hotel information.
   - View a list of all hotels.

3. Customer Management:
   - Add and manage customer details.
   - View customer profiles and booking history.

4. Hotel Search:
   - Search for hotels based on location, price range, and amenities.
   - View detailed information about selected hotels.

5. Booking Management:
   - Book rooms in selected hotels.
   - Manage booking details including check-in and check-out dates.
   - View booking history and status.

Technologies Used

- Flask: A lightweight WSGI web application framework in Python.
- SQLite: A lightweight, disk-based database used to store hotel, admin, customer, and booking details.
- HTML/CSS: For the front-end to create responsive and user-friendly web pages.
- Bootstrap: For styling the application and creating responsive layouts.

Installation and Setup

1. Clone the Repository:
   git clone https://github.com/your-username/hotel-management-system.git
   cd hotel-management-system

2. Set Up Virtual Environment:
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies:
   pip install -r requirements.txt

4. Set Up the Database:
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

5. Run the Application:
   flask run

6. Access the Application:
   Open your web browser and navigate to http://127.0.0.1:5000.

Project Structure

- app: Contains the main application code.
  - static: Static files (CSS, JavaScript, images).
  - templates: HTML templates for rendering the web pages.
  - models.py: Database models for the application.
  - routes.py: Application routes and view functions.
  - forms.py: Forms for input validation and handling.
- migrations: Database migration files.
- config.py: Configuration settings for the application.
- run.py: Entry point to run the Flask application.

Contributing

Contributions are welcome! If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

---

This Hotel Management System provides a comprehensive solution for managing hotel bookings, customer details, and hotel information. It leverages the simplicity and power of Flask to create a robust back-end, making it easy to deploy and extend. Feel free to explore the code, use it in your projects, and contribute to its development!
