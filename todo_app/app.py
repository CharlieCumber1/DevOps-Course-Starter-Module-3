from flask import Flask, render_template, redirect, url_for, request

from todo_app.data.mongodb import MongoDB
from todo_app.view_model import ViewModel

def create_app():
    app = Flask(__name__)
    database = MongoDB()


    @app.route('/')
    def index():
        items = database.get_items()
        view_model_items = ViewModel(items)
        return render_template('index.html', items = view_model_items)


    @app.route('/items/new', methods=['POST'])
    def add_item():
        name = request.form['name']
        database.add_item(name)
        return redirect(url_for('index'))


    @app.route('/items/<id>/start')
    def start_item(id):
        database.start_item(id)
        return redirect(url_for('index')) 


    @app.route('/items/<id>/complete')
    def complete_item(id):
        database.complete_item(id)
        return redirect(url_for('index'))


    @app.route('/items/<id>/uncomplete')
    def uncomplete_item(id):
        database.uncomplete_item(id)
        return redirect(url_for('index')) 


    @app.route('/items/<id>/delete')
    def delete_item(id):
        database.delete_item(id)
        return redirect(url_for('index'))


    if __name__ == '__main__':
        app.run(host='0.0.0.0')
    
    return app
    