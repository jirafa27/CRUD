from flask import Flask
from flask_bootstrap import Bootstrap
import redis

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
redisCache = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
from app import views
