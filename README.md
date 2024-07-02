1. Clone the project from github

2. Create the virtual environment
    windows - python -m venv venv
    mac - python3 -m venv venv

3. Activate the virtual environment
    windows -  .\venv\Scripts\activate.bat
    mac -  source myvenv/bin/activate

4. Install requirements
    pip install -r requirements.txt
    After adding a new library/package update the requirements.txt file using pip freeze > requirements.txt

5. Create super user
    python manage.py createsuperuser

6. Run migrations
    python manage.py makemigrations
    python manage.py migrate

7. Run the project
    python manage.py runserver