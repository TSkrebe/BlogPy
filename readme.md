#  Simple flask website
Writen with python3

Instructions:

1. Clone this project
2. Open config.py file and change variables RECAPTCHA, SECRET_KEY, DATABASE, etc. 
2. Create virtual environment and install dependencies from *requirements.txt* file: `pip install -r requirements.txt`
  1. Depending on your DB you will need to install additional dependencies 
3. To create a database and tables you will need to run these command lines
  1. `python startup.py db init`
  2. `python startup.py db migrate`
  3. `python startup.py db upgrade`

4. Now you can start website by executing `python startup.py runserver -h 0.0.0.0`
5. If you want to access admin panel (which you probably want) you will need to create a row in "users" table. To do that simply write `python startup.py shell`
6. Write and `user = User(your_username, your_password)` followed by `user.save()`
8. repeat step 4 and go to www.ipaddress:port/login
9. Enjoy your website


## More info

Flask provided webserver should not be used in production applications. To have fully functioning website read about Gunicorn and nginx.

