# add log files for gunicorn
sudo mkdir -pv /var/{log,run}/gunicorn/

sleep 1

sudo chown -cR root:root /var/{log,run}/gunicorn/