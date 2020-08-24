# indian-food-app

# how to run app locally:
1) create and activate virtual enviroment then install the dependencies:
    pip install -r requirements.txt

2) create local instance of database:
    flask db init
    flask db migrate -m "my first migration"
    flask db upgrade

3) run app by comman:
    python run.py
