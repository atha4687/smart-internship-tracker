# Smart Internship Tracker

 Project Overview
 
Smart Internship Tracker is a web-based application that helps students organize and manage internship and job applications in one place. Many students apply to multiple opportunities and struggle to keep track of deadlines, application statuses, and important notes. This system allows users to register, log in, add applications, update statuses, search and filter records, and delete entries — all from one centralized dashboard.

Features

User registration and login with secure encrypted passwords
Add internship and job applications with company name, role, location, deadline, and notes
View all applications in a clean dashboard table
Update application status (Applied, Interview, Offered, Rejected)
Delete applications you no longer need
Search and filter applications by company name or status
Track deadlines with visual highlights for upcoming dates
Add and expand notes for interview preparation
Charts and statistics to visualize your application progress


 Technologies Used

Python
Flask
MySQL
XAMPP
HTML
CSS
Bootstrap
JavaScript (optional interactivity)


 Installation and Setup

Clone or download the project and open the folder in VS Code.
Start XAMPP and turn on MySQL.
Open phpMyAdmin and create a database called internship_tracker, then import database/schema.sql.

The app can also create the database automatically if the MySQL root user has the required permissions.


Open a terminal inside the project folder.
Install the required packages: pip3 install -r requirements.txt


 How to Run the Project

Make sure you are inside the project folder.
Start XAMPP and confirm MySQL is running.
Run the application:

python3 app.py

 Open your browser and go to:

http://127.0.0.1:5000

 Database Notes
The default database connection is set in app.py:

host: localhost
user: root
password: (leave blank)
database: internship_tracker

These settings match the default XAMPP MySQL setup. If your setup is different, update the connection settings in app.py before running the app.
The full database structure is saved in database/schema.sql so the database can be recreated at any time directly from the repository.

Project Structure
internship-tracker/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   └── schema.sql
│
├── templates/
│
└── static/

 Team Members and Roles

Alhaji Kargbo — Project Manager
Responsible for coordinating the team, managing timelines, and ensuring project completion.

Renae Washington — Software Architect
Responsible for system design, database structure, and overall architecture decisions.

Langston Gwinn — Backend Developer
Responsible for implementing server-side logic, database integration, and application functionality.

Quincy King — Frontend Developer
Responsible for designing the user interface and ensuring a responsive and user-friendly experience.

Ali-Andro Thaxter — Software Tester
Responsible for testing the system, identifying bugs, and ensuring software quality.
