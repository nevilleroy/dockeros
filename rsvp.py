from flask import Flask, render_template, redirect, url_for, request,make_response
from flaskext.mysql import MySQL
import socket
import os


app = Flask(__name__)

# password for testing, use host file during production.
app.config['MYSQL_DATABASE_PASSWORD'] = 'jeevan123'
app.config['MYSQL_DATABASE_HOST'] = 'mysql'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'rsvp_data'

# Init and connect SQL to database.
mysql = MySQL()
mysql.init_app(app)

TEXT1=os.environ.get('TEXT1', "Hackfest")
TEXT2=os.environ.get('TEXT2', "Registration")
ORGANIZER=os.environ.get('ORGANIZER', "UVCE")


# Default root (index page)
@app.route('/')
def rsvp():
    new_connection = mysql.connect()
    new_cursor = new_connection.cursor()
    
    # to check if table exists
    new_cursor.execute('SHOW TABLES;')
    tables = [table for table in new_cursor]
    
    # create table if table doesn't exist
    if len(tables) < 1:
        new_cursor.execute(
            'CREATE TABLE rsvp_users(name VARCHAR(45) NOT NULL, email VARCHAR(45) NOT NULL)'
            )
        new_connection.commit()
    
    # get people from the database
    new_cursor.execute('SELECT * FROM rsvp_users;')
    people = new_cursor.fetchall()
    
    # get the count and pass data onto profile.html
    count = len(people)
    hostname = socket.gethostname()
    return render_template('profile.html', counter=count, hostname=hostname,\
                           people=people, TEXT1=TEXT1, TEXT2=TEXT2, ORGANIZER=ORGANIZER)


# to add people to the database, only POST, not view
@app.route('/new', methods=['POST'])
def new():

    #get data from the form in profile.html
    name = request.form['name']
    email = request.form['email']

    # insert the data into the database.
    new_connection = mysql.connect()
    new_cursor = new_connection.cursor()
    new_cursor.execute("INSERT INTO rsvp_users(name, email) VALUES(%s, %s);", (name, email))
    new_connection.commit()

    # to stay on the same page after POST
    return redirect(url_for('rsvp'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
