# Testing instructions
Pytest unit tests and Playwright browser tests are used in this project. To run tests locally use these instructions. For both unit tests and Playwright tests, you need to be in poetry shell and in the app/ directory
## Unit tests
- Use the command ```invoke unittest```
- The data from unit tests is stored in a test database that is destroyed after completion

Example:

![image](https://github.com/ILMOWEB/ilmo/assets/101889891/6166d134-844c-48f0-9b3a-fda1275535d7)


## Playwright browser tests
- In one terminal, start the application with ```invoke start```
- In another terminal use command ```invoke e2e``` to run headed tests
- For headless test use command ```pytest ilmoweb/tests/playwright/ --base-url http://127.0.0.1:8000/```
- For Playright tests, the database must be populated with populate.py and have no local changes

Example:

![image](https://github.com/ILMOWEB/ilmo/assets/101889891/49fd5be9-a1ee-4eb7-a9b8-b00ddb975e2f)

## Coverage
To get test coverage run ```invoke coverage```
Then access index.html file in the htmlcov folder /ilmo/app/htmlcov/

Currert coverage:

![image](https://github.com/ILMOWEB/ilmo/assets/101889891/cbc3fb40-aa18-4f86-badf-e35daf72c92c)

Coverage only accounts for unit tests and displays the test coverage for Django database models, app logic, and webpage requests.

