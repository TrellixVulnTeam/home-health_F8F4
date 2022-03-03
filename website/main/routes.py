from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from website.auth.forms import LoginForm, SignupForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm

from werkzeug.urls import url_parse
from datetime import datetime
# add for thingspeak communication
import urllib
from bs4 import BeautifulSoup
import re # for regex
from flask_mail import Mail
from time import time
import jwt
import random
import numpy as np
from datetime import datetime
import json
import csv
import pandas as pd
from pandas import DataFrame
from io import StringIO
from website.models import User, Packet
from website.main import bp
from website.models import people
from website import db

seen_packets = [] # initialize seen packet list
# test type dict stores channel id for each test type
test_types = {'EMG': 'https://api.thingspeak.com/channels/1664068/feeds.csv?api_key=NJCHLCB72TL1X017', 'PULSE': 'https://api.thingspeak.com/channels/1649676/feeds.csv?api_key=JLVZFZMPYNBHIU33'}


# APP ROUTES
# route for the grab new test data button on user profile page    
@bp.route('/newtest/<username>')
def newtest(username):
    user = User.query.filter_by(username=username).first_or_404()
    if not new_packet(user, 'PULSE'):
        flash('No New Test Results Available')
    else:
        flash('New Test Result was Grabbed') 
    # render user page again with new packet added
    return render_template('user.html', user=user, packets=user.packets.all())

# route for delete all tests button
# deletes all packets for the given user
@bp.route('/deletetests/<username>')
def delete_all_tests(username):
    user = User.query.filter_by(username=username).first_or_404()
    packets = user.packets.all()
    for p in packets:
        db.session.delete(p)
    db.session.commit()
    return render_template('user.html', user=user, packets=user.packets.all()) 
 
# route for delete this test button
@bp.route('/deletetest/<username>/<packet_id>')
def deletetest(username, packet_id):
    user = User.query.filter_by(username=username).first_or_404()
    p = Packet.query.filter_by(id=packet_id).first_or_404()
    db.session.delete(p)
    db.session.commit()
    return render_template('user.html', user=user, packets=user.packets.all())

# this function loops through all the rows in the appropriate csv table
# checks seen_packets for each row's entry id
# new entry id --> create new packet for the user with the data from this row
# then add this row's entry id to the seen_packets array
# otherwise check the next row 
# returns false if no new test result was found
def new_packet(user, test_type):
    global seen_packets
    global test_types
    grab = 0
    done = False
    url = test_types[test_type] # grab from appropriate channel. each test type will has its own channel
    thingspeak_read = urllib.request.urlopen(url)
    bytes_csv = thingspeak_read.read()
    data=str(bytes_csv,'utf-8')
    thingspeak_data = pd.read_csv(StringIO(data))
    body_df = pd.DataFrame(thingspeak_data)
    # creates new packet for every row in index and adds packet to our packet_queue 
    while grab < len(body_df.index) and done is False: 
        this_row = thingspeak_data.iloc[grab] 
        entry_id = str(this_row['entry_id']) # save the entry id for this row
        # check seen packets array for this entry_id
        if entry_id not in seen_packets:
            test_taken = "Date: "+ str(this_row['field4'])+" Time: "+str(this_row['field5'])
            # create a new packet associated for user 
            p = Packet(body=str(this_row['field3']), author=user, test_type=str(this_row['field2']), test_taken=test_taken) # field2 = test_type
            db.session.add(p) # add packet to db
            db.session.commit()
            seen_packets.append(entry_id) # add this entry id to the seen packets array
            done = True
        grab += 1 
    return done

# route for view entire test result 
@bp.route('/open_packet/<username>/<packet_id>')
def open_packet(username, packet_id):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('view_test.html', user=user, packet=Packet.query.get(packet_id))

# route for test visualization/chart page
@bp.route('/open_packet/<username>/test_chart')
def test_chart(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('test_chart.html', user=user)


# routes for about page
@bp.route('/about')
def about():
    return render_template('about.html', people=people.people)

@bp.route('/hardware_team')
def hardware():
    return render_template('hardware_team.html', people=people.people)

@bp.route('/software_team')
def software():
    return render_template('software_team.html', people=people.people)

@bp.route('/introduction')
def introduction():
    return render_template('introduction.html', people=people.people)

@bp.route('/progress')
def progress():
    return render_template('progress.html', people=people.people)
## end about page routes