# Lingua-dei-segni-web-trainer
## Prerequisites
 - Python
 - Pip
 - venv
 - Node
 - npm
 - MySQL

## Environment Variables

For the environment variables, there are ".env.example" files in both the frontend and backend folders. Remove ".example" and provide values for each variable.

## Start aplication

First, you need to create the database that the application will use. Simply create an empty database; the app will handle setting up the structure.

To start the backend, you need to install the dependencies inside a virtual environment:

`python -m venv ./venv`

Then execute:

`./venv/Scripts/activate`

`pip install -r requirements.txt`

`python3 app.py`

To start the frontend, simply run the following commands inside the frontend folder:

`npm i`

`npm run dev`

The website will be accessible at "https://localhost:5173"
