# Lingua-dei-segni-web-trainer
## Prerequisites
 - Python
 - Pip
 - venv
 - Node
 - npm
 - MySQL
 - OpenSSL

## Environment Variables

For the environment variables, there are ".env.example" files in both the frontend and backend folders. Remove ".example" and provide values for each variable.

## Certificates

For use the application you need a certificate for HTTPS.

For generate a self-signed certificate you can use this command:

`openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes`

Leave all te values with blank and insert "localhost" on the Common Name parameter.

After that you should verifiy inside `./frontend/vite.config.js` and `./backend/app.py` the paths for the certificate and the key.

## Start aplication

For start the application you need to create the database that the application will use. Simply create an empty database; the app will handle setting up the structure.

To start the backend, you need to install the dependencies inside a virtual environment:

`python -m venv ./venv`

Then execute:

`./venv/Scripts/activate`

`pip install -r requirements.txt`

`python3 app.py`

To start the frontend, simply run the following commands inside the frontend folder:

`npm i`

`npm run dev`

The website will be accessible at "https://localhost:5173" and when you open it you have to accept the certificate.

Before you use the application you also need to go on "https://localhost:5000" to accept the certificate for the backend.