from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

app = Flask(__name__)

engine = create_engine('sqlite:///CATalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# For debugging
#Fake Categories
category = {'name': 'Wet Food', 'id': '1'}
categories = [{'name': 'Wet Food', 'id': '1'}, {'name':'Dry Food', 'id':'2'},{'name':'Toys', 'id':'3'}]

#Fake Category Items
category_items = [ {'name':'Almo Salmon', 'description':'Real chunks of salmon','id':'1'}, {'name':'Adult Cat Kibble','description':'For cats ages 1-10', 'id':'2'},{'name':'Lil Mouse', 'description':'Mouse with catnip inside','id':'3'},{'name':'Iced Tea', 'description':'with lemon','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','id':'5'} ]
category_item =  {'name':'Almo Salmon','description':'Real chunks of salmon'}


@app.route('/')
@app.route('/catalog')
def catalog():
    return render_template('catalog.html', categories=categories)

@app.route('/catalog/new')
def catNew():
    return render_template('catNew.html')

@app.route('/catalog/<int:category_id>/edit')
def catEdit(category_id):
    return render_template('catEdit.html', category=category)

@app.route('/catalog/<int:category_id>/delete')
def catDelete(category_id):
    return render_template('catDelete.html', category=category)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/')
def itemView(category_id, item_id):
    return "Display a specific item"

@app.route('/catalog/<int:category_id>/items/new')
def itemNew(category_id):
    return render_template('itemNew.html')

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit')
def itemEdit(category_id, item_id):
    return render_template('itemEdit.html', category_item=category_item)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete')
def itemDelete(category_id, item_id):
    return render_template('itemDelete.html', category_item=category_item)   

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
