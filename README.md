# ILMO
![GHA badge](https://github.com/ILMOWEB/ilmo/workflows/CI/badge.svg)

[Backlog](https://docs.google.com/spreadsheets/d/1zsXol2-I28QDLTTSvJKAZO7r786YN_nL7AbXE-i2GJM/edit?invite=CIPmtn8&pli=1#gid=1)

[Google Meets](https://meet.google.com/xwd-djmc-bmb)

[Definition of Done](https://github.com/ILMOWEB/ilmo/blob/main/documentation/DoD.md)

[Documentation](https://github.com/ILMOWEB/ilmo/tree/main/documentation)

## Run tests
To run unit tests manually, go to app-directory and run ```poetry run invoke unittest```

## Run playwright tests
Poetry doesn't install playwright automatically since playwright installs its own browser configurations. <br/>
The first time you pull playwright to your local repository you need to run ```playwright install ``` in poetry shell.

Open the server in a terminal by going to app-directory and running ```poetry run invoke start```

Open another terminal and run ```poetry run invoke e2e```

## Get unit test coverage
- Go to app/

- Run ```poetry run invoke coverage```

HTML-report is produced automatically.

The report ```index.html``` is located in the htmlcov directory.

## Connect to a test database
For this step, you need a Postgres database locally.
You can use instructions from the University of Helsinki webpage: [Local database](https://github.com/hy-tsoha/local-pg)  
- Start the local database.
- Go to the app/config and create ```.env``` -file


```.env``` should include to following information:

NAME= ```database_name```  
USER= ```database_user``` or NONE  
PASSWORD= ```database_password``` or NONE  
HOST= ```database_host``` usually ```localhost``` or ```path/to/socket```  
PORT= ```database_port``` usually 5432
LOCAL= ```True```
UNI_LOGIN= ```False```
EMAIL_HOST_PASSWORD= ```email_host_password```

- Run ```poetry run invoke migrate```
- Start the application  

Now the application should be connected to your database.

## Populate the test database
- Go to app/

- Run ```poetry run invoke populate ```

## Create a superuser
- Go to app/
- Run ```python manage.py createsuperuser ``` and follow the instructions.
