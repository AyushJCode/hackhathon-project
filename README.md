# Hackathon Project

A Flask + SQLite backend built for the Odoo x VIT Pune Hackathon.

## Team
- Ayush (Database + Git + Backend)
- Tejas (Backend + Flask)
- Member 3 (Frontend)
- Member 4 (Frontend)

## Setup

### Requirements
- Python 3.x
- Flask

### Install dependencies
pip install flask

### Run the app
python app.py

Server runs at http://127.0.0.1:5000

## API Routes

### Add User
- Method: POST
- URL: /add-user
- Body:
{
    "name": "Ayush",
    "email": "ayush@gmail.com"
}

### Add Entry
- Method: POST
- URL: /add-data
- Body:
{
    "user_id": 1,
    "data": "your data here"
}

### Get All Entries
- Method: GET
- URL: /get-data

### Get History by User
- Method: GET
- URL: /history?user_id=1

### Reset All Entries
- Method: DELETE
- URL: /reset

## Branch Structure
- main → stable code only
- dev → team integration branch
- ayush → Ayush's workspace
- tejas → Tejas's workspace

## Rules
- Never push directly to main
- Always pull from dev before starting work
- Use clear commit messages