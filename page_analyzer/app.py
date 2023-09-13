import os

from flask import Flask, render_template
from dotenv import load_dotenv

from page_analyzer.db import initialize_db
from page_analyzer.url_repository import URLRepository
from page_analyzer.url_service import URLService

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

min_connections = os.environ.get('DB_MIN_CONNECTIONS', 1)
max_connections = os.environ.get('DB_MAX_CONNECTIONS', 10)
db_uri = os.environ.get('DB_URI')

db_pool = initialize_db(db_uri, min_connections, max_connections)
url_repository = URLRepository(db_pool)
url_service = URLService(url_repository)


@app.route("/")
def index():
    return render_template('index.html')
