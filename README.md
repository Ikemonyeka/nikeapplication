[

Postgres DB is used for this project:

-replace connection string in database.py

-replcae the sqlalchemy.url variable with your connection string in the alembic.ini file
]

[

To Setup Backend

run:

Note: your location must be "your_system_path/NIKEAPPLICATION/"

First, you want remove the current venv file:

	Remove-Item -Recurse -Force venv

Second, create it again:

	python -m venv venv
Third, activate the env:

	.\venv\Scripts\Activate
 
Fourth, install all packages by running:

	pip install -r requirements.txt

Note: your location must be "your_system_path/NIKEAPPLICATION/backend"

Fifth, ensure no pending migrations:

	alembic stamp head
 
Sixth, create the migration for the models:

	alembic revision --autogenerate -m "create tables"
 
Seventh, create the tables in the database specified:

	alembic upgrade head

Note: your location must be "your_system_path/NIKEAPPLICATION/"

Eight, start the backend of the application:

	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
 
	the url should be: http://127.0.0.1:8000/docs
 
]

[

Frontend Setup

Note: you should be in the NIKEAPPLICATION\frontend\nike-react-app

npm install

npm install @mui/material @emotion/react @emotion/styled @mui/icons-material    

npm install react-router-dom   

npm start 

]
