from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CatalogItem, User


from flask import session as login_session
from flask import make_response
from flask import flash
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Client"

engine = create_engine('sqlite:///CATalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Routes that return JSON Serialized Data
@app.route('/catalog/JSON')
@app.route('/JSON')
def allCatsJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])


@app.route('/catalog/<int:category_id>/items/JSON')
@app.route('/catalog/<int:category_id>/JSON')
def oneCatJSON(category_id):
    category = session.query(Category).filter_by(category_id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return jsonify(CatalogItems=[i.serialize for i in items])


@app.route('/catalog/<int:category_id>/items/<int:item_id>/JSON')
@app.route('/catalog/<int:category_id>/<int:item_id>/JSON')
def oneItemJSON(category_id, item_id):
    Catalog_Item = session.query(CatalogItem).filter_by(item_id=item_id).one()
    return jsonify(Catalog_Item=Catalog_Item.serialize)


# Login Route. Create and store a state token in the session
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                    string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Connect via Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Validate Token
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # Abort if there is an error
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify the correct access token is for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
                json.dumps("Token ID doesn't match current ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('User is already logged in.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store the token for later use
    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data["name"]
    login_session['email'] = data["email"]

    # Check if User already Exists, if not create new user.
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    flash("You are now logged in as %s" % login_session['email'])
    return "Welcome."


# Revoke token / reset login_session and disconnect.
@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        flash("You are not logged in.")
        return redirect(url_for('catalog'))

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You have disconnected.")
        return redirect(url_for('catalog'))
    else:
        # The given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        flash("Disconnection failed.")
        return redirect(url_for('catalog'))


# Add a new user to the User table with login session data
def createUser(login_session):
    newUser = User(
                    name=login_session['username'],
                    email=login_session['email'])
    session.add(newUser)
    session.commit()

    user = session.query(User).filter_by(email=login_session['email']).first()
    return user.user_id


# Return an entry in the user table for a specific user
def getUserInfo(user_id):
    user = session.query(User).filter_by(user_id=user_id).one()
    return user


# Return a user id for a specific user's email
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.user_id
    except:
        return None


# Routes for the CAT-A-LOG Website
@app.route('/')
@app.route('/catalog')
def catalog():
    categories = session.query(Category).all()
    return render_template('catalog.html', categories=categories)


@app.route('/catalog/<int:category_id>/')
@app.route('/catalog/<int:category_id>/items')
def catView(category_id):
    category = session.query(Category).filter_by(category_id=category_id).one()
    items = session.query(CatalogItem).filter_by(
        category_id=category_id).all()
    return render_template('catView.html', items=items, category=category)


@app.route('/catalog/<int:category_id>/items/new', methods=['GET', 'POST'])
def itemNew(category_id):
    # Check for login
    if 'email' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = CatalogItem(
                            name=request.form['name'],
                            description=request.form['description'],
                            price=request.form['price'],
                            category_id=category_id,
                            user_id=login_session['user_id'])
        session.add(newItem)
        session.commit()
        flash("Item Created.")
        return redirect(url_for('catView', category_id=category_id))
    else:
        return render_template('itemNew.html', category_id=category_id)

    return render_template('itemNew.html', category=category)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/edit',
           methods=['GET', 'POST'])
def itemEdit(category_id, item_id):
    editItem = session.query(CatalogItem).filter_by(item_id=item_id).one()
    # Check for login
    if 'email' not in login_session:
        return redirect('/login')
    if editItem.user_id != login_session['user_id']:
        flash("You are not authorized to edit this item.")
        return redirect(url_for('catView', category_id=category_id))

    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['price']:
            editItem.price = request.form['price']
        session.add(editItem)
        session.commit()
        flash("Item edited.")
        return redirect(url_for('catView', category_id=category_id))
    else:
        return render_template(
            'itemEdit.html',
            category_id=category_id,
            item_id=item_id,
            item=editItem)


@app.route('/catalog/<int:category_id>/items/<int:item_id>/delete',
           methods=['GET', 'POST'])
def itemDelete(category_id, item_id):
    deleteItem = session.query(CatalogItem).filter_by(item_id=item_id).one()
    # Check for login
    if 'email' not in login_session:
        return redirect('/login')
    if deleteItem.user_id != login_session['user_id']:
        flash("You are not authorized to delete this item.")
        return redirect(url_for('catView', category_id=category_id))
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash("Item deleted.")
        return redirect(url_for('catView', category_id=category_id))
    else:
        return render_template(
                            'itemDelete.html',
                            category_id=category_id,
                            item=deleteItem)

# Generate a random secret key
catSecret = ''.join(
                    random.choice(
                                string.ascii_uppercase +
                                string.digits) for x in xrange(32))

if __name__ == '__main__':
    app.secret_key = catSecret
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
