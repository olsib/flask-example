#!/usr/bin/python3

import json
import pymysql
import pymysql.cursors
from flask import Flask
from flask import g
from flask import Response
from flask import request
from flask import render_template, jsonify, redirect


app = Flask(__name__)

@app.before_request
def db_connect():
  g.conn = pymysql.connect(host='172.30.49.196',
                              user='root',
                              passwd='Welcome1',
                              db='linkid_db')
  g.cursor = g.conn.cursor()

@app.after_request
def db_disconnect(response):
  g.cursor.close()
  g.conn.close()
  return response

def query_db(query, args=(), one=False):
  g.cursor.execute(query, args)
  rv = [dict((g.cursor.description[idx][0], value)
  for idx, value in enumerate(row)) for row in g.cursor.fetchall()]
  return (rv[0] if rv else None) if one else rv

@app.route("/")
def hello():
#  return "Whazzuppp!"
  return redirect("127.0.0.1:5005/names")
 
@app.route("/names", methods=['GET'])
def names():
  result_current = query_db("SELECT name, linkid_current FROM linkid_db.nodes_current")
  data_current = json.dumps(result_current)
  new_obj_current = json.loads(data_current)
  for i in range(0,4):
    if new_obj_current[i]['name'] == 'dist1':
      global dist1_current
      dist1_current = new_obj_current[i]['linkid_current']
    elif new_obj_current[i]['name'] == 'dist2':
      global dist2_current
      dist2_current = new_obj_current[i]['linkid_current']
    elif new_obj_current[i]['name'] == 'sync1':
      global sync1_current
      sync1_current = new_obj_current[i]['linkid_current']
    else:
      global sync2_current
      sync2_current = new_obj_current[i]['linkid_current']

  print dist1_current,dist2_current,sync1_current,sync2_current

  result_latest = query_db("SELECT name, linkid_latest FROM linkid_db.nodes")
  data_latest = json.dumps(result_latest)
  new_obj_latest = json.loads(data_latest)
  for j in range(0,4):
    if new_obj_latest[j]['name'] == 'dist1':
      global dist1_latest
      dist1_latest = new_obj_latest[j]['linkid_latest']
    elif new_obj_current[j]['name'] == 'dist2':
      global dist2_latest
      dist2_latest = new_obj_latest[j]['linkid_latest']
    elif new_obj_current[j]['name'] == 'sync1':
      global sync1_latest
      sync1_latest = new_obj_latest[j]['linkid_latest']
    else:
      global sync2_latest
      sync2_latest = new_obj_latest[j]['linkid_latest']
  
#  print data_current,data_latest
  both_obj = data_current + data_latest
  print both_obj

#  return render_template('index.html', json = data_current, obj = both_obj)
  if dist1_latest >= dist1_current and dist2_latest >= dist2_current:
    return render_template('indexgreen.html', title = 'Home', dist1_current=dist1_current, dist2_current=dist2_current)
  elif dist1_latest <= dist1_current or dist2_latest <= dist2_current:
    return render_template('indexred.html', title = 'Home', dist1_current=dist1_current, dist2_current=dist2_current)
  else:
    return render_template('indexyellow.html', title = 'Home', dist1_current=dist1_current, dist2_current=dist2_current)

@app.route("/add", methods=['POST'])
def add():
  req_json = request.get_json()
  g.cursor.execute("UPDATE TABLE linkid_db.nodes set cr(firstname, lastname) VALUES (%s,%s)", (req_json['firstname'], req_json['lastname']))
  g.conn.commit()
  resp = Response("Updated", status=201, mimetype='application/json')
  return resp

if __name__ == "__main__":
  app.debug = True
  app.run(host='0.0.0.0', port=5005)
