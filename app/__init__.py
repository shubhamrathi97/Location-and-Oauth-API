from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, Index
import json

#Define App
app = Flask(__name__)
#Configuring app from config.py file
app.config.from_object('config')

db = SQLAlchemy(app)

# Define models
class location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    #for faster calculation of Distance Difference
    Index('dist', func.ll_to_earth(lat, lng), postgresql_using='gist')

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng

"""*****************************************************
Request URL: <url>/post_location
Request Type: Post
Request Input: JSON Object
        {
            "name":"bhopal accurate 2",
            "lat":"23.258926",
            "lng":"77.414120"
        }
Expected Output: "Successfully Added"
Developed By Shubham Rathi <shubham.rathi97@gmail.com>        
******************************************************"""        
@app.route('/post_location',methods=['POST'])
def post_location():
    raw_dict = request.get_json(force=True)
    try:
        print(raw_dict)
        loc = location(raw_dict["name"],raw_dict["lat"],raw_dict["lng"])
        db.session.add(loc)
        db.session.commit()
        return "Successfully Added", 201
            
    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 403
        return resp


"""*****************************************************
Request URL: <url>/get_using_postgres/<lat>/<lng>
Example - localhost:5000/get_using_postgres/23.265156/77.403949
Request Type: Get
Request Input: Params lat and lng
Expected Output: JSON
        [
          {
            "name": "bhopal accurate"
          },
          {
            "name": "bhopal accurate 2"
          }
        ]

Developed By Shubham Rathi <shubham.rathi97@gmail.com>        
******************************************************"""        
@app.route('/get_using_postgres/<lat>/<lng>', methods=['GET'])
def get_using_postgres(lat, lng):
    loc_current = func.ll_to_earth(lat, lng)
    loc_locations = func.ll_to_earth(location.lat, location.lng)
    distance_func = func.earth_distance(loc_current, loc_locations)
    query = db.session.query(location, distance_func).filter(distance_func < 5000).order_by(distance_func)

    result = query.all()
    mapped = []
    for row in result:
        #print(row[0].__dict__)
        mapped.append({"name":row[0].__dict__["name"]})
    return json.dumps(mapped)


"""*****************************************************
Request URL: <url>/get_using_self
Request Type: GET
Request Input: Params lat, lng
Expected Output:  JSON Object
        [
          {
            "name": "bhopal accurate"
          },
          {
            "name": "bhopal accurate 2"
          }
        ]
Developed By Shubham Rathi <shubham.rathi97@gmail.com>        
******************************************************"""        
@app.route('/get_using_self/<lat>/<lng>', methods=['GET'])
def get_using_self(lat, lng):
    return json.dumps()
