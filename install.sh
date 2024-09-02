# install python3-pip
sudo apt-get install python3-pip -y

# install venv
sudo apt-get install python3-venv -y

# create venv
python3 -m venv venv

# activate venv
source venv/bin/activate

# install requirements
pip install -r requirements.txt

# install gunicorn
pip install gunicorn

# add log files for gunicorn
sudo mkdir -pv /var/{log,run}/gunicorn/

sleep 1

sudo chown -cR root:root /var/{log,run}/gunicorn/