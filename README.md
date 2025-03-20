[
Postgres DB is used for this project:

-replace connection string in database.py

-replcae the sqlalchemy.url with your connection string in the alembic.ini file

To Setup Backend

run:

python -m venv venv

venv\Scripts\activate   	

pip install -r requirements.txt

pip install fastapi[all] "uvicorn[standard]"  

pip install langchain

pip install langchain_community

pip install openai

alembic revision --autogenerate -m "Create items, orders, and users tables" //This will create a model of the table  

alembic upgrade head // This will create the tables in your specified database

uvicorn backend.app.main:app --reload  //This must be executed from "your_system_path}/nikeapplication/" path. When you run this all the data needed to test the application will be seeded into your postgres database to test the application. 
]


[
Frontend Setup

run:

npm install

npm install @mui/material @emotion/react @emotion/styled   

npm install @mui/icons-material  

npm install react-router-dom   

npm start 

Note: you should be in the NIKEAPPLICATION\frontend\nike-react-app when running commands
]