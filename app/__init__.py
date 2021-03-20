from flask import Flask #ambil library flask framework
from flask_cors import CORS #ambil library cors untuk pemangglan request GET POST PUT dsb
from flask_sqlalchemy import SQLAlchemy #ambil library flask_sqlalchemy untuk menyimpan data ke database sementara SQLAlchemy
from flask_migrate import Migrate #ambil library flask_migrate untuk meng-update perubahan database
import os #ambil library os untuk memanggil folder didalam framework flask

project_dir = os.path.dirname(os.path.abspath(__file__)) #mengarahkan folder mana yang akan menyimpan file database
database_file = "sqlite:///{}".format(os.path.join(project_dir, "db/database.db")) # penyimpanan database

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.controller.AppController import *