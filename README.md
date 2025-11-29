# BarberBuddy

## 1. Description of the App
BarberBuddy is a virtual assistant and appointment-management system designed specifically for small barbershops. The goal of the app is to help barbers reduce missed calls, avoid repetitive questions, and automate booking so they can focus entirely on their clients.

This product combines two important components: 

## A-  Customer-facing chatbot:

Customers can:

- Log in with their phone number

- Book appointments automatically

- Check prices and available services

- Receive instant confirmations

- Avoid having to call or wait for replies

This solves the common problems barbers face: interruptions during work, missed calls, and constant repetitive messages about prices or availability.

## B- Barber-facing dashboard
Barbers can:

- View and manage their weekly schedule

- Track earnings

- See client histories and no-show behavior

- Manage services and pricing

This dashboard provides organization and visibility into the business, helping barbers save time and increase efficiency.
## 2. Features
BarberBuddy includes two main feature groups: Customer Features (via chatbot) and Barber Features (via dashboard). Together, they create a complete booking and management solution for small barbershops.

## Customer Features
**Phone Number Login:**

- Customers identify themselves using their phone number, making the process simple and fast.

**Automated Appointment Booking:**

- The chatbot guides the customer through selecting a service, choosing a barber, and booking an available time slot.

**Real-Time Availability:**

- The chatbot displays available time slots based on the barber’s schedule.

**Service & Price Consultation:**

- Customers can request the list of available services with updated prices.

**Booking Confirmation Message:**

- After a booking is made, the system sends a confirmation message summarizing the service, barber, date, and time.

Easy and Instant Interaction:
No need for calls, waiting times, or manual responses.
##  Barber Features

**Weekly Calendar View:**

- Barbers can see all their appointments for the week at a glance.

**Different Time Ranges:**

- Switch between daily, weekly, monthly, quarterly, or yearly views for better planning.

**Appointment Details:**

- Clicking a booking reveals client information, service type, and time.

**Earnings Overview:**

- A dedicated earnings section displays total earnings for selected time periods.

**Barber Comparison:**

- Managers can compare earnings between different barbers.

**Client History Tracking:**

- Barbers can see past visits, preferences, and no-show behavior.

**Service Management:**

- The dashboard allows updating prices and managing available services.

## 3. File Structure and Explanations

### /src
- **chatbot.py** → Handles the interaction flow for customers (booking, price queries, greetings, etc.).
Represents how the chatbot would function in a real system.


- **appointments.py** → Contains functions related to appointment creation, conflict checking, and schedule handling.


- **algorithm_next_slot.py** → Includes the required algorithm for the project.
This algorithm finds the next available time slot for a barber, based on existing appointments


- **database.py** → Represents the logic for loading, saving, and updating client, service, and appointment data.
In the prototype, it works with sample JSON files


- **dashboard.py** → Simulates how the barber dashboard would process data for the calendar and earnings views


- **utils.py** → Contains helper functions (validation, formatting, date utilities,...) used across the project.

### /resources
- **sample_clients.json** → Contains example client records (name, phone number, no-show count, ...)


- **sample_appointments.json** → Contains fake appointments used to simulate calendar and booking logic


- **sample_services.json** → Contains the list of available services and their prices

### Root Files
- **README.md** → Project documentation, includes descriptions, features and installation steps. 
- **run_app.py** → File to execute the prototype. It simulates the execution of the app
- **requirements.txt** → List of installed libraries

## 4. Prerequisites & Environment
To run the BarberBuddy prototype, the user only needs a basic Python environment.

- Python version 3.10+
- Operating Systems: Windows / MacOS / Linux
  - Libraries: 
  
    - json: to load an store sample client and appointment data ,
    
    - datetime: to manage appointment dates and times
    - tkinter (optional): placeholder for dashboard/GUI representation

## 5. Installation
Step 1 — Download the ZIP  
Step 2 — Extract the ZIP  
Step 3 — Double-click run_app.py  
Step 4 — The app prototype opens

## 6. Execution
Once the user double-clicks run_app.py, the prototype starts running automatically.

The file performs the following actions:

1- Displays a welcome message

2- Simulates the initialization of the system
- Even though the full app is not implemented, this file represents the entry point where: 
    
    - Data would be loaded from the /resources folder
    - The dashboard or chatbot interface would normally open
    - Future integrations (GUI, chatbot, scheduling algorithm) would be triggered

## 7. Further Improvements
The current prototype demonstrates the core logic of appointment booking, data handling, and basic interaction flows. Future improvements may include:

- Graphical User Interface (GUI): Replace the text-based simulation with a full visual interface for barbers and clients


- Integrated Chat Platform: Connect the chatbot to WhatsApp, Telegram, or a website widget for real-world abuse. 


- Advanced Scheduling Algorithm: Improve time slot detection to support overlapping services, like multiple barbers working at the same time. 


- User Authentication: Add password-based logins for barbers and enhanced verification for clients


- Notification systems: Implement email/SMS reminders for upcoming appointments.


- Online Payments (optional): Allow customers to pay online


## 8. Bibliography / Webgraphy
Here is what we used for the creation of the project and code: 

Python Official Documentation — https://docs.python.org/

JSON File Format Specification — https://www.json.org/

Python datetime Library — https://docs.python.org/3/library/datetime.html

Python Best Practices for Project Structure — https://realpython.com/python-application-layouts/

Tkinter Documentation — https://docs.python.org/3/library/tkinter.html
## 9. Credits
Telmo Bernedo, Manuel Abello, Alvaro Franco, Quique Lopez, Ivan Hermosilla, Tomas Cañizales