from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem

app = Flask(__name__)

engine = create_engine('sqlite:///CATalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    return render_template('catalog.html', categories=categories)

@app.route('/catalog/new')
def catNew():
    return render_template('catNew.html')

@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items')
def catView(category_id):
    category = session.query(Category).filter_by(category_id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('catView.html', items=items, category=category)

@app.route('/catalog/<int:category_id>/edit')
def catEdit(category_id):
    return render_template('catEdit.html', category=category)

@app.route('/catalog/<int:category_id>/delete')
def catDelete(category_id):
    return render_template('catDelete.html', category=category)
   
@app.route('/catalog/<int:category_id>/items/new')
def itemNew(category_id):
    return render_template('itemNew.html')

@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def itemEdit(category_id, item_id):
#    return render_template('itemEdit.html', catalog_item=catalog_item)
    editedItem = session.query(CatalogItem).filter_by(item_id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('itemView', category_id=category_id))
    else:
        return render_template(
            'itemEdit.html', category_id=category_id, item_id=item_id, item=editedItem)

@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete')
def itemDelete(category_id, item_id):
    return render_template('itemDelete.html', catalog_item=catalog_item)   

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
