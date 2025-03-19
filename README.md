To Setup Backend
run:

python -m venv venv

venv\Scripts\activate   	

pip install -r requirements.txt
pip install fastapi[all] "uvicorn[standard]"  

alembic revision --autogenerate -m "Create items, orders, and users tables"  

alembic upgrade head
 pip install langchain
 pip install langchain_community
 pip install openai

uvicorn backend.app.main:app --reload  


Frontend
run:

npm install @mui/material @emotion/react @emotion/styled   
npm install @mui/icons-material  
npm install react-router-dom   
npm start 
