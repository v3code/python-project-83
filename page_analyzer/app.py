import logging
import os

from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, request, flash
from returns.result import Success, Failure

from page_analyzer.db import DatabaseHandler
from page_analyzer.errors import ValidationError, URLExistsError, URLNotExistsError
from page_analyzer.url_repository import URLRepository
from page_analyzer.url_service import URLService

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

min_connections = os.environ.get('DB_MIN_CONNECTIONS', 1)
max_connections = os.environ.get('DB_MAX_CONNECTIONS', 10)
db_uri = os.environ.get('DATABASE_URI')

db = DatabaseHandler(db_uri, min_connections, max_connections)
url_repository = URLRepository(db)
url_service = URLService(url_repository)


@app.get("/")
def index():
    return render_template('index.html')


@app.get("/urls")
def show_urls():
    urls = url_service.get_all_urls()
    return render_template('urls/urls_list.html', urls=urls)


@app.post("/urls")
def add_url():
    url_name = request.form['url']
    result = url_service.add_url(url_name)
    match result:
        case Success(url):
            return redirect(url_for('show_url_by_id', url_id=url.id))
        case Failure(ValidationError()) as result:
            flash(result.failure().get_message(), 'danger')
            return render_template('index.html', url_name=url_name)
        case Failure(URLExistsError()) as result:
            failure = result.failure()
            flash(failure.get_message(), 'info')
            url = failure.get_url()
            return redirect(url_for('show_url_by_id', url_id=url.id))


@app.get('/urls/<int:url_id>')
def show_url_by_id(url_id: int):
    result = url_service.get_url_by_id(url_id)
    match result:
        case Success(url):
            return render_template('urls/url_info.html', url=url)
        case Failure(URLNotExistsError()) as result:
            failure = result.failure()
            flash(failure.get_message(), 'danger')
            return redirect(url_for('show_urls'))

