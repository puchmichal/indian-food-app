# indian-food-app

## how to run app locally:
1. Install heroku CLI appropriately for your operating system, instructions can be found:
    https://devcenter.heroku.com/articles/getting-started-with-python#set-up

1. create and activate virtual environment then install the dependencies:\
    `pip install -r requirements.txt`

1. install developer dependencies:\
    `pip install -r requirements.dev.txt`
    

1. create local instance of database:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

    or:
    
   ```bash
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```
    
1. run app by command:\
    `python run.py` or `heroku local web` or `flask run`
