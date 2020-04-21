from flask import request, jsonify, Blueprint
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from app.model import db
from .model import Location

location_api = Blueprint("location_api", __name__)

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


@location_api.route('/post_location', methods=['POST'])
def post_location():
    raw_dict = request.get_json(force=True)
    try:
        print(raw_dict)
        loc = Location(raw_dict["name"], raw_dict["lat"], raw_dict["lng"])
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


@location_api.route('/get_using_postgres/<lat>/<lng>', methods=['GET'])
def get_using_postgres(lat, lng):
    loc_current = func.ll_to_earth(lat, lng)
    loc_locations = func.ll_to_earth(Location.lat, Location.lng)
    distance_func = func.earth_distance(loc_current, loc_locations)
    query = db.session.query(Location, distance_func).filter(distance_func < 5000).order_by(distance_func)

    result = query.all()
    mapped = []
    for row in result:
        # print(row[0].__dict__)
        mapped.append({"name": row[0].__dict__["name"]})
    return jsonify(mapped)


"""*****************************************************
Request URL: <url>/get_using_self
Example: localhost:5000/get_using_self/23.265156/77.403949
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


@location_api.route('/get_using_self/<lat>/<lng>', methods=['GET'])
def get_using_self(lat, lng):
    lat = float(lat)
    lng = float(lng)
    distance_func = func.sqrt((111.12 * (Location.lat - lat)) * (111.12 * (Location.lat - lat)) + (
            111.12 * (Location.lng - lng) * func.cos(lat / 92.215)) * (
                                      111.12 * (Location.lng - lng) * func.cos(lat / 92.215)));
    query = db.session.query(Location, distance_func).filter(distance_func < 5).order_by(distance_func)
    result = query.all()
    mapped = []
    for row in result:
        mapped.append({"name": row[0].__dict__["name"]})
    return jsonify(mapped)
