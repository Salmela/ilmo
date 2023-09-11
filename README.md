# ILMO
![GHA badge](https://github.com/ILMOWEB/ilmo/workflows/CI/badge.svg)  

[Backlog](https://docs.google.com/spreadsheets/d/1zsXol2-I28QDLTTSvJKAZO7r786YN_nL7AbXE-i2GJM/edit?invite=CIPmtn8&pli=1#gid=1)

[Google Meets](https://meet.google.com/xwd-djmc-bmb)

[Definition of Done](https://github.com/ILMOWEB/ilmo/blob/main/documentation/DoD.md)

## Run tests
To run unit tests manually, go to app-directory and run ```./manage.py test ilmoweb``` 

## Get unit test coverage
Go to the directory containing the ```manage.py``` file.  

- Run ```coverage run --source='.' manage.py test ilmoweb/ ```  
  
- To produce a html-report of the coverage, run ```coverage html```
  
Now the report ```index.html``` is located in the htmlcov directory.
