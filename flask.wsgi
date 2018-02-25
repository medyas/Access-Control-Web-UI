import sys


dir = "/var/www/flask/accessControl"
sys.path.insert(0, dir)

from rfid import app as application

