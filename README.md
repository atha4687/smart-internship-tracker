# Smart Internship Tracker

## Project Overview
Smart Internship Tracker is a web-based application that helps students organize and manage internship and job applications in one place. The system allows users to register, log in, add applications, update statuses, search and filter records, and delete entries.

## Features
- User registration and login
- Add internship/job applications
- View applications in dashboard
- Update application status
- Delete applications
- Search and filter applications
- Track deadlines and notes

## Technologies Used
- Python
- Flask
- MySQL
- XAMPP
- HTML
- CSS

## Installation and Setup
1. Open the project folder in VS Code.
2. Start XAMPP and turn on MySQL.
3. Open phpMyAdmin and import `database/schema.sql`.
   - The app can also create this database automatically if the MySQL root user has permission.
4. Open a terminal in the project folder.
5. Install the project packages:
   pip3 install -r requirements.txt

## How to Run the Project
1. Make sure you are inside the project folder.
2. Start XAMPP MySQL if it is not already running.
3. Run:
   python3 app.py
4. Open your browser and go to:
   http://127.0.0.1:5000

## Database Notes
The default database connection is in `app.py`:

- host: `localhost`
- user: `root`
- password: blank
- database: `internship_tracker`

These settings match the default XAMPP MySQL setup.

The database structure is saved in `database/schema.sql` so the MySQL database can be recreated from GitHub.

## Project Structure
- app.py
- database/schema.sql
- templates/
- static/
- requirements.txt
- README.md

## Team Members 
- Alhaji Kargbo
- Langston Gwinn
- Ali-Andro Thaxter
- Renae Washington
- Quincy King
