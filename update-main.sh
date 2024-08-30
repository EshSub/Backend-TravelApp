git pull git@github.com:EshSub/Backend-TravelApp

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate

pkill gunicorn

sleep 2

gunicorn -c config/gunicorn/prod.py

sleep 5

ps aux | grep gunicorn