from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{0}:{1}@{2}/{3}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_NAME')
    )

db = SQLAlchemy(app)

