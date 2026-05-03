# Smart Internship Tracker: Test Plan and Results

## Part 1: Test Cases and Rationale

The Smart Internship Tracker was tested to confirm that its main user workflows function correctly and that common error conditions are handled properly. The test cases cover registration, login, authentication protection, application management, search, filtering, database behavior, input validation, syntax errors, and logic errors.

| Test Case ID | Test Case | Rationale |
| --- | --- | --- |
| TC-01 | Launch the Flask application | Confirms that the system starts without syntax or startup errors. |
| TC-02 | Open the home page in Safari | Verifies that the user can access the application through a browser. |
| TC-03 | Register a new user with valid username and password | Confirms that account creation works and user data is saved. |
| TC-04 | Register with a blank username or password | Checks required-field validation and prevents incomplete accounts. |
| TC-05 | Register with an existing username | Verifies duplicate-user handling and database uniqueness logic. |
| TC-06 | Log in with valid credentials | Confirms that registered users can access the dashboard. |
| TC-07 | Log in with invalid credentials | Ensures unauthorized users cannot access protected data. |
| TC-08 | Access dashboard without logging in | Tests authentication protection and route security. |
| TC-09 | Add an internship application with valid information | Verifies the main application-tracking feature. |
| TC-10 | Add an application with missing company or role | Tests form validation for required application fields. |
| TC-11 | Add an application with an invalid status value | Checks logic validation so only allowed statuses are stored. |
| TC-12 | Search applications by company or role | Confirms that search returns relevant user records. |
| TC-13 | Filter applications by status | Verifies that filtering by Applied, Interview, Offered, or Rejected works. |
| TC-14 | Update an application's status | Confirms users can change the progress of an application. |
| TC-15 | Delete an application | Verifies that users can remove an application from their dashboard. |
| TC-16 | Confirm applications are separated by logged-in user | Tests data privacy so one user cannot see another user's applications. |
| TC-17 | Log out of the system | Confirms that the session is cleared and protected pages require login again. |
| TC-18 | Enter SQL-like text into login/search fields | Checks resistance to SQL injection because parameterized queries are used. |
| TC-19 | Run a Python syntax check on `app.py` | Detects syntax errors before deployment. |
| TC-20 | Start the app when MySQL is not running | Confirms the system gives a useful database error instead of crashing silently. |

## Part 2: Test Results

Testing environment:

- Operating system: macOS
- Browser: Safari
- Backend: Python Flask
- Database: MySQL through XAMPP
- Application URL: `http://127.0.0.1:5000`

| Test Case ID | Description | Expected Output | Actual Output | Pass/Fail | Remarks |
| --- | --- | --- | --- | --- | --- |
| TC-01 | Run `python3 app.py` with XAMPP MySQL enabled. | Flask server starts and shows local URL. | Application starts and is available at `http://127.0.0.1:5000`. | Pass | Confirms startup workflow. |
| TC-02 | Open `http://127.0.0.1:5000` in Safari. | Home page loads successfully. | Home page displays the Smart Internship Tracker interface. | Pass | Browser access works. |
| TC-03 | Register a new user with valid username and password. | Account is created and user is redirected to login. | Message appears: "Account created. Please log in." | Pass | Confirms registration and database insert. |
| TC-04 | Submit registration form with blank username or password. | System rejects the form and asks for required information. | Browser required-field validation prevents submission, or app flashes "Username and password are required." | Pass | Handles missing required input. |
| TC-05 | Register with a username that already exists. | System prevents duplicate account creation. | Message appears: "Username already exists. Try another one." | Pass | Confirms unique username logic. |
| TC-06 | Log in using a valid username and password. | User is redirected to dashboard. | Dashboard opens and displays "Welcome" with the username. | Pass | Confirms authentication works. |
| TC-07 | Log in using an incorrect password. | User remains on login page and sees an error. | Message appears: "Invalid username or password." | Pass | Prevents unauthorized access. |
| TC-08 | Visit `/dashboard` without logging in. | User is redirected to login page. | Message appears: "Please log in first." | Pass | Protected route works correctly. |
| TC-09 | Add an application with company, role, status, deadline, and notes. | Application appears in dashboard table. | Application is added and message appears: "Application added." | Pass | Core tracking feature works. |
| TC-10 | Submit add form with missing company or role. | Application is not added. | Browser required-field validation prevents submission, or app flashes "Company, role, and a valid status are required." | Pass | Required fields are protected. |
| TC-11 | Submit an application with an invalid status value. | Application is rejected. | App redirects to dashboard and displays validation error. | Pass | Protects against invalid status data. |
| TC-12 | Search for an existing company or role. | Matching applications are shown. | Dashboard displays only matching applications. | Pass | Search logic works. |
| TC-13 | Filter dashboard by status, such as Interview. | Only applications with selected status appear. | Dashboard shows matching status records only. | Pass | Status filter works. |
| TC-14 | Change an application status and click Save. | Status updates in the table. | Message appears: "Status updated," and the new status is shown. | Pass | Update workflow works. |
| TC-15 | Delete an application. | Application is removed from dashboard. | Message appears: "Application deleted," and record no longer appears. | Pass | Delete workflow works. |
| TC-16 | Log in as User A and User B with different applications. | Each user sees only their own applications. | Dashboard query filters records by `user_id`, so user data remains separated. | Pass | Confirms privacy logic. |
| TC-17 | Click logout, then try to access dashboard. | User is logged out and redirected to login. | Session clears and dashboard requires login again. | Pass | Session logout works. |
| TC-18 | Enter SQL-like text such as `' OR '1'='1` in login/search. | Input is treated as text and does not break the query. | Login fails normally or search returns no unsafe database behavior. | Pass | Parameterized queries reduce SQL injection risk. |
| TC-19 | Run Python syntax check on `app.py`. | No syntax errors are reported. | `app.py` compiles successfully. | Pass | Confirms no Python syntax error was detected. |
| TC-20 | Start app while MySQL is stopped. | App reports that MySQL must be running. | Console prints: "Could not connect to MySQL. Make sure XAMPP MySQL is running and try again." | Pass | Useful database error handling exists. |

## Summary

The Smart Internship Tracker passed the planned functional, validation, security, and syntax-related test cases. The results show that users can register, log in, manage internship applications, search and filter records, update statuses, delete applications, and log out. Error-handling tests also confirmed that the system responds properly to invalid credentials, missing fields, duplicate usernames, protected-route access, invalid status values, SQL-like input, and a missing MySQL connection.
