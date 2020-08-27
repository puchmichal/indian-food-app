# indian-food-app

# how to run app locally:
1) Install heroku CLI appropriately for yout opertain system, instructions can be found:
    https://devcenter.heroku.com/articles/getting-started-with-python#set-up

2) create and activate virtual enviroment then install the dependencies:\
    pip install -r requirements.txt

3) install developer dependecies:\
    pip install -r requirements.dev.txt

4\) create local instance of database:\
    flask db init\
    flask db migrate\
    flask db upgrade

    or:

    python manage.py db init\
    python manage.py db migrate\
    python manage.py db upgrade

5) run app by command:\
    heroku local web \
    or:\

    flask run
