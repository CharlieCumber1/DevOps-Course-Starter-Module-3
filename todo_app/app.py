import os
from flask import Flask, render_template, redirect, url_for, request, abort
from functools import wraps
import requests
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient

from todo_app.data.mongodb import MongoDB
from todo_app.user import User
from todo_app.view_model import ViewModel

def writer_required(f):
    @login_required
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = User(current_user.id)
        if not user.is_writer():
            abort(401, "Permission Denied")
        return f(*args, **kwargs)
    return decorated_function

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED')
    database = MongoDB()

    ## Auth Service Setup
    login_manager = LoginManager()
    login_manager.init_app(app)

    client_id = os.getenv("AUTH_CLIENT_ID")
    client_secret = os.getenv("AUTH_CLIENT_SECRET")
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'

    auth_client = WebApplicationClient(client_id)
    auth_client.prepare_request_uri(authorization_base_url)

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(auth_client.prepare_request_uri(authorization_base_url))

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/login/')
    def login():
        code = request.args.get('code')
        token_request_url, token_request_headers, token_request_body = auth_client.prepare_token_request(token_url, authorization_response=request.url, client_secret=client_secret)
        token_request_response = requests.post(token_request_url, headers=token_request_headers, data=token_request_body)
        auth_client.parse_request_body_response(token_request_response.content.decode())
        user_request_url, user_request_headers, user_request_body = auth_client.add_token("https://api.github.com/user")
        user_request_response = requests.get(user_request_url, headers=user_request_headers, data=user_request_body)
        user_name = user_request_response.json()['login']
        user = User(user_name)
        login_user(user)
        return redirect(url_for('index'))

    @app.route('/')
    @login_required
    def index():
        user = User(current_user.id)
        items = database.get_items()
        view_model_items = ViewModel(items)
        return render_template('index.html', items = view_model_items, read_only = not user.is_writer())


    @app.route('/items/new', methods=['POST'])
    @writer_required
    def add_item():
        name = request.form['name']
        database.add_item(name)
        return redirect(url_for('index'))


    @app.route('/items/<id>/start')
    @writer_required
    def start_item(id):
        database.start_item(id)
        return redirect(url_for('index')) 


    @app.route('/items/<id>/complete')
    @writer_required
    def complete_item(id):
        database.complete_item(id)
        return redirect(url_for('index'))


    @app.route('/items/<id>/uncomplete')
    @writer_required
    def uncomplete_item(id):
        database.uncomplete_item(id)
        return redirect(url_for('index')) 


    @app.route('/items/<id>/delete')
    @writer_required
    def delete_item(id):
        database.delete_item(id)
        return redirect(url_for('index'))


    if __name__ == '__main__':
        app.run(host='0.0.0.0')
    
    return app
    