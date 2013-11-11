This is pre-alfa. :D

Make sure you have the packets:
youtube-dl
rabbitmq-server
python-virtualenv

You need this in /etc/rabbitmq/rabbitmq-env.conf:
NODE_IP_ADDRESS='127.0.0.1'
NODENAME='guest@localhost'

Make a virtualenv in the root of the project:
virtualenv --no-site-packages .

Activate the virtual env:
source bin/activate

Install the deps:
python setup.py install

Run the dev server:
pserve production.ini

Run the MQ server:
rabbitmq-server -detached

Run the worker:
mkdir yodl/media
celery -A yodl.tasks worker --loglevel=INFO &

