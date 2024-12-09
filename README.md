# MakersBnB Project

This repository is an AirBnb clone which aims to replicate its core functunalities.

## Built with Python, Flask, PostgreSQL and Pytest.

## 🌟 Features

     * User Authentication: Users can create an account and log in. Passwords are encrypted in the database.
     * Design & Responsiveness: Leveraging Bootstrap for modern UI components and responsiveness.
     * Database Management: Utilizes PostgreSQL for robust, scalable, and reliable data storage.
     * Testing Suite: Implements pytest for unit and integration testing, ensuring high code quality and reliability.
     * Routing: Employs Flask's URL routing for intuitive navigation across pages.
     * Environment Configuration: Integrates configuration management with .env files for secure handling of sensitive information.
     * Error Handling: Provides comprehensive error handling for better debugging and user feedback

## 🔧 Prerequisites

Ensure you have Python and PostgreSQL installed.

## Setup for Windows

```shell
# Set up the virtual environment
; python -m venv makersbnb-venv

# Activate the virtual environment
; makersbnb-venv\Scripts\Activate

# Install dependencies
(makersbnb-venv); pip install -r requirements.txt

# Install the virtual browser we will use for testing
(makersbnb-venv); playwright install

# To run the tests (with extra logging)
(makersbnb-venv); pytest -sv

# To run the app
(makersbnb-venv); python app.py

# Now visit http://localhost:5001/index in your browser
```
