from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# CHANGE TO NEW TABLES
# from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///CATalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/catalog')
def catalog():
    return "Display the different categories and the latest items"

@app.route('/catalog/<int:category_id>/items')
def catEdit(category_id):
    return "Display a list of items in the selected category"

@app.route('/catalog/new')
def catNew():
    return "Create a new category"

@app.route('/catalog/<int:category_id>/edit')
def catEdit(category_id):
    return "Edit a category"

@app.route('/catalog/<int:category_id>/delete')
def catDelete(cetegory_id):
    return "Delete a category"

@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def itemView(category_id, item_id):
    return "Display a specific item"

@app.route('/catalog/<int:category_id>/items/new')
def itemNew(category_id):
    return "Create a new item"

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit')
def itemEdit(category_id, item_id):
    return "Edit a specific item"

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete')
def itemDelete(category_id, item_id):
    return "Delete a specific item"   

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
