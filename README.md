# ILMO
![GHA badge](https://github.com/ILMOWEB/ilmo/workflows/CI/badge.svg)  

[Backlog](https://docs.google.com/spreadsheets/d/1zsXol2-I28QDLTTSvJKAZO7r786YN_nL7AbXE-i2GJM/edit?invite=CIPmtn8&pli=1#gid=1)

[Google Meets](https://meet.google.com/xwd-djmc-bmb)

[Definition of Done](https://github.com/ILMOWEB/ilmo/blob/main/documentation/DoD.md)

[Documentation](https://github.com/ILMOWEB/ilmo/tree/main/documentation)

## Run tests
To run unit tests manually, go to app-directory and run ```./manage.py test ilmoweb``` 

## Get unit test coverage
Go to the directory containing the ```manage.py``` file.  

- Run ```coverage run --source='.' manage.py test ilmoweb/ ```  
  
- To produce a html-report of the coverage, run ```coverage html```
  
Now the report ```index.html``` is located in the htmlcov directory.

## Connect to a test database
- Go to the app/config and create ```.env``` -file


```.env``` should include to following information:

NAME=[database_name] <br/>
USER=[database_user] or NONE <br/>
PASSWORD=[database_password] or NONE <br/>
HOST=[database_host] usually [localhost] or [path/to/socket] <br/>
PORT=[database_port] usually 5432

- Run ```python manage.py makemigrations ```
  
- Run ```python manage.py migrate ```

- Run ```python manage.py createsuperuser ``` and follow the instructions.

Now the application should be connected to your database. 

- Open the application and go to .../admin.
- Log in as the superuser you just created. If it works, the connection is stable.

## Populate the test database
- Go to app/

- Run ```python config/populate.py ```

- Open the application and go to .../database_test

if the site shows you the database information, populating was successful.

