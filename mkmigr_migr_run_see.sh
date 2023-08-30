# add it to the .gitignore later
py manage.py makemigrations
py manage.py migrate
py -mwebbrowser http://127.0.0.1:8000/
py manage.py runserver
