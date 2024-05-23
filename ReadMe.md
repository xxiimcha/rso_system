# RSO Registration System

## Overview

The RSO Registration System is a Python application built using Tkinter for the GUI and MySQL for the database. The system allows users to manage organizations and their members.

## Features

- Add, edit, and delete organizations.
- Add, edit, and delete members associated with organizations.
- Upload and display organization logos.
- View and manage members of selected organizations.

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)
- Pillow (for image handling)
- MySQL
- mysql-connector-python

## Installation

### Step 1: Install Python Dependencies
Install the required Python packages using pip:

pip install pillow mysql-connector-python

### Step 2: Set Up the Database

## Using phpMyAdmin
- Open phpMyAdmin in your web browser.
- Create a new database named rso.
- Import the provided SQL file (rso.sql) to set up the database schema and initial data.
- Click on the rso database in the left sidebar.
- Go to the Import tab.
- Choose the rso.sql file from your local machine.
- Click Go to import the file.

## Using MySQL Command Line
Alternatively, you can use the MySQL command line to import the database:

mysql -u root -p
CREATE DATABASE rso;
USE rso;
SOURCE path/to/rso.sql;

### Step 3: Run the Application
Run the Python application using the following command:

python main.py

### Usage
- The main window displays the list of organizations and their members.
- Use the buttons at the top to add, edit, or delete organizations and members.
- When adding or editing an organization, you can upload an image to be used as the organization's logo.
- Selecting an organization displays its members in the right pane.
- Selecting a member enables the edit and delete options for that member.