Team 2 Code Execution:
1. Ensure system python version is greater than or equal to 3.6.0: `python -V`
2. Setup python virtual environment and activate it: `https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/`
3. Go to the root directory of the project: `cd mtech-portal`
4. Install all library requirements: `pip install -r requirements.txt` 
5. SQLite migrations check: `python manage.py makemigrations`     
6. Perform SQLite migrations: `python manage.py migrate`
7. Run the server: `python manage.py runserver`