from flask import Flask, render_template, request, url_for, redirect, jsonify, flash  # noqa
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Car, MenuItem, User

# New imports for this step
from flask import session as login_session
import random
import string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import logging


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Car Menu Application"

engine = create_engine('sqlite:///carmenuuser.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login to the website
@app.route('/login')
def login():
    ''' Create anti-forgery state token '''
    state = ''.join(random.choice(
      string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('logina.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    ''' Validate state token '''
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        # print ("Token's client ID does not match app's.")
        logging.error("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Add provider for login sesion
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;">'  # noqa
    flash("you are now logged in as %s" % login_session['username'])
    print ('Done')
    return output


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    ''' disconnect only the connected user '''
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))  # noqa
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON API to show  all Car Companies
@app.route('/car/JSON')
def carJSON():
    cars = session.query(Car).all()
    return jsonify(cars=[car.serialize for car in cars])


# JSON API to show Car Company and its all items
@app.route('/car/<int:car_id>/menu/JSON')
def carMenuJSON(car_id):
    car = session.query(Car).filter_by(id=car_id).one()
    items = session.query(MenuItem).filter_by(car_id=car.id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# JSON ENDPOINT: to show an item within car company
@app.route('/car/<int:car_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(car_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


# Show all Car companies
@app.route('/')
@app.route('/car/')
def carMenu():
    cars = session.query(Car).order_by(desc(Car.name))
    if 'username' not in login_session:
        return render_template('publiccar.html', cars=cars)
    else:
        return render_template('car.html', cars=cars)


# Create a new car company
@app.route('/car/new', methods=['GET', 'POST'])
def newCarMenu():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newComp = Car(name=request.form['name'], user_id=login_session['user_id'])  # noqa
        session.add(newComp)
        session.commit()
        flash('New Car Company %s Successfully Created' % newComp.name)
        return redirect(url_for('carMenu'))
    else:
        return render_template('newcar.html')


# Edit car company
@app.route('/car/<int:car_id>/edit', methods=['GET', 'POST'])
def editCarMenu(car_id):
    editedcomp = session.query(Car).filter_by(id=car_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedcomp.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this car company. Please create your own car company in order to edit.');}</script><body onload='myFunction()''>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedcomp.name = request.form['name']
            flash('Car Company %s Successfully Edited' % editedcomp.name)
            return redirect(url_for('carMenu'))
    else:
        return render_template('editcar.html', car=editedcomp)


# Delete car company
@app.route('/car/<int:car_id>/delete', methods=['GET', 'POST'])
def deleteCarMenu(car_id):
    deletedcomp = session.query(Car).filter_by(id=car_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedcomp.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this car company. Please create your own car company in order to delete.');}</script><body onload='myFunction()''>"  # noqa
    if request.method == 'POST':
        session.delete(deletedcomp)
        flash('Car Company %s Successfully Deleted' % deletedcomp.name)
        session.commit()
        return redirect(url_for('carMenu', car_id=car_id))
    else:
        return render_template('deletecar.html', car=deletedcomp)


# Show all car company items
@app.route('/car/<int:car_id>/')
@app.route('/car/<int:car_id>/menu/')
def carMenuItem(car_id):
    car = session.query(Car).filter_by(id=car_id).one()
    creator = getUserInfo(car.user_id)
    items = session.query(MenuItem).filter_by(car_id=car_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:  # noqa
        return render_template(
            'publiccaritem.html', car=car, items=items, creator=creator)
    else:
        return render_template(
            'menu.html', car=car, items=items, creator=creator)


# Show all datails in car company item
@app.route('/car/<int:car_id>/menu/<int:menu_id>')
def carMenuItemOne(car_id, menu_id):
    carmenuone = session.query(MenuItem).filter_by(id=menu_id).one()
    car = session.query(Car).filter_by(id=car_id).one()
    creator = getUserInfo(car.user_id)
    return render_template(
        'menuitem.html', car=car, item=carmenuone, creator=creator)


# Create a new car company item
@app.route('/car/<int:car_id>/menu/new', methods=['GET', 'POST'])
def newCarMenuItem(car_id):
    if 'username' not in login_session:
        return redirect('/login')
    car = session.query(Car).filter_by(id=car_id).one()
    if login_session['user_id'] != car.user_id:
        return "<script>function myFunction() {alert('You are not authorized to create car item. Please login to your own car company in order to create it.');}</script><body onload='myFunction()''>"  # noqa
    if request.method == 'POST':
        newCar = MenuItem(name=request.form['name'], description=request.form['description'], price=request.form['price'], item_type=request.form['item_type'], car_id=car_id, user_id=car.user_id)  # noqa
        session.add(newCar)
        session.commit()
        flash('New %s Car Successfully Created' % newCar.name)
        return redirect(url_for('carMenuItem', car_id=car_id))
    else:
        return render_template('newcaritem.html', car_id=car_id)


# Edit car company item
@app.route('/car/<int:car_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])  # noqa
def editCarMenuItem(car_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedcarmenu = session.query(MenuItem).filter_by(id=menu_id).one()
    car = session.query(Car).filter_by(id=car_id).one()
    if login_session['user_id'] != car.user_id:
        return "<script>function myFunction(){alert('You are not authorized to edit this car item. Please create your own car item in order to edit.');}</script><body onload='myFunction()''>"  # noqa
    if request.method == 'POST':
        if request.form['name']:
            editedcarmenu.name = request.form['name']
        if request.form['description']:
            editedcarmenu.description = request.form['description']
        if request.form['price']:
            editedcarmenu.price = request.form['price']
        if request.form['item_type']:
            editedcarmenu.item_type = request.form['item_type']
        session.add(editedcarmenu)
        session.commit()
        flash('%s Car Successfully Edited' % editedcarmenu.name)
        return redirect(url_for('carMenuItem', car_id=car_id))
    else:
        return render_template('editItem.html', car_id=car_id, menu_id=menu_id, item=editedcarmenu)  # noqa


# Delete car company item
@app.route('/car/<int:car_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])  # noqa
def deleteCarMenuItem(car_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    deletedcaritem = session.query(MenuItem).filter_by(id=menu_id).one()
    car = session.query(Car).filter_by(id=car_id).one()
    if login_session['user_id'] != car.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this car item. Please create your own car item in order to edit.');} </script> <body onload = 'myFunction()''>"  # noqa
    if request.method == 'POST':
        session.delete(deletedcaritem)
        session.commit()
        flash('%s Car Successfully Deleted' % deletedcaritem.name)
        return redirect(url_for('carMenuItem', car_id=car_id))
    else:
        return render_template('deleteitem.html', item=deletedcaritem)


# Disconnect based on login_session
@app.route('/disconnect')
def disconnect():
    ''' Logout the user from session and delete all information '''
    if 'username' in login_session:
        gdisconnect()
        del login_session['gplus_id']
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('carMenu'))
    else:
        flash("You were not logged in")
        return redirect(url_for('carMenu'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
