# ILMO
![GHA badge](https://github.com/ILMOWEB/ilmo/workflows/CI/badge.svg)

[Backlog](https://docs.google.com/spreadsheets/d/1zsXol2-I28QDLTTSvJKAZO7r786YN_nL7AbXE-i2GJM/edit?invite=CIPmtn8&pli=1#gid=1)

[Google Meets](https://meet.google.com/xwd-djmc-bmb)

[Definition of Done](https://github.com/ILMOWEB/ilmo/blob/main/documentation/DoD.md)

[Documentation](https://github.com/ILMOWEB/ilmo/tree/main/documentation)

- [Testing instuctions](https://github.com/ILMOWEB/ilmo/blob/main/documentation/testing.md)

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
