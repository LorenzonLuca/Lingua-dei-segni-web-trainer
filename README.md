# Lingua-dei-segni-web-trainer
## Goal
The goal of this project is to create a product that allows users to train in sign language. To achieve this goal, I created a website where users can select an image or capture in real time from a webcam. The website will use a Machine Learning model to recognize a hand within the image and show the user the words related to the sign they made. On the website, it will be possible to train the user's knowledge by showing an image of the hand and asking the user to replicate the sign. The application will determine if the hand is positioned correctly. Users will also be able to log in to the website to save their learning progress history. 

## Deploy
### Prerequisites
 - Python
 - Pip
 - venv
 - Node
 - npm
 - MySQL
 - OpenSSL

### Environment Variables

For the environment variables, there are ".env.example" files in both the frontend and backend folders. Remove ".example" and provide values for each variable.

### Certificates

For use the application you need a certificate for HTTPS.

For generate a self-signed certificate you can use this command:

`openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes`

Leave all te values with blank and insert "localhost" on the Common Name parameter.

After that you should verifiy inside `./frontend/vite.config.js` and `./backend/app.py` the paths for the certificate and the key.

### Start application

For start the application you need to create a MySQL database that the application will use. Simply create an empty database and the app will handle setting up the structure.

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
