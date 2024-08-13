# Maximus Ticket management system

A simple IT ticket managment tool  written with python django, and several javascripts
Website  design created with tailwind-css, free tailwind templates, and TW components

Reason of the application:  Study, practise django, python and tailwind css

Website functions:
Different dashboards with different, permission for admin,manager, and general users

Admin Dashboard with extended functions:
-update tickets
-create user, modify users, reset user passwords
-create workroles, departments, customer and update them

Management dashboard with extra fuctions:

-list tickets with different settings
-export data to csv file
-list workroles, list departments, view users in department and other departments
-list oncall users
-view ticket tables
-close tickets
-extended statisic charts

General User dashboard 
-create tickets 
-list own deparment tickets
-assign tickets to departments, and users, update tickets and possiblity to resolv them
-see own department user information
-own department statistic charts


Application installation:
about lack of space database not contain any data

1. clone the repository
2. need create virtual environment ( on linux: virtualenv  venv)
3. activate the vitual environment (source venv/bin/activate )
4. install python django and requirements :   ( pip3 install -r  requirements.txt)
5. need create empty database, and structure with :   python manage.py makemigrations &  python manage.py migrate
6. need create superuser : python manage.py createsuperuser
7. start application with : python manage.py runserver
9. login with superuser and password 
8. need to fill admin user profile,  create customers, workroles, departments for proper tesing 

