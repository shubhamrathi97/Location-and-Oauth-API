from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, Index
from datetime import datetime, timedelta
import json, jwt 
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

class oauth(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    client_id = db.Column(db.String(255), unique=True)
    client_secret = db.Column(db.String(255))
    redirect_uri = db.Column(db.String(255))
    
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

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
@app.route('/get_using_self/<lat>/<lng>', methods=['GET'])
def get_using_self(lat, lng):
    lat = float(lat)
    lng = float(lng)                                                 
    distance_func = func.sqrt((111.12 * (location.lat - lat)) * (111.12 * (location.lat - lat)) + (111.12 * (location.lng - lng) * func.cos(lat / 92.215)) * (111.12 * (location.lng - lng) * func.cos(lat / 92.215)));    
    query = db.session.query(location, distance_func).filter(distance_func < 5).order_by(distance_func)
    result = query.all()
    mapped = []
    for row in result:
        #print(row[0].__dict__)
        #print(row[1])
        mapped.append({"name":row[0].__dict__["name"]})
    return json.dumps(mapped)



"""*****************************************************
Request URL: <url>/add_oauth
Request Type: Post
Request Input: JSON Object
        {
            "client_id":"ASDSfjdsfhj121432423",
            "client_secret":"147652268+2665235421",
            "redirect_uri":"www.shubhamrathi.me"
        }
Expected Output: "Successfully Added"
Developed By Shubham Rathi <shubham.rathi97@gmail.com>        
******************************************************"""        
@app.route('/add_oauth',methods=['POST'])
def add_oauth():
    raw_dict = request.get_json(force=True)
    try:
        print(raw_dict)
        temp = oauth(raw_dict["client_id"],raw_dict["client_secret"],raw_dict["redirect_uri"])
        db.session.add(temp)
        db.session.commit()
        return "Successfully Added", 201
            
    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 403
        return resp


"""*****************************************************
Request URL: <url>/oauth/authorize
Example: localhost:5000/oauth/authorize?response_type=code&client_id=123456789&redirect_uri=localhost.com&scope=read
Request Type: GET
Request Input: Params response type, redirect URI, client id, scope
Expected Output:  JSON Object
        {
        "authorization_code": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY3ODkifQ.pSnldg0lX4gom3nf_Cey04X3xYdSF2xGukQEkPKGwhY",
        "client_id": "123456789",
        "redirect_uri": "localhost.com"
        }
Developed By Shubham Rathi <shubham.rathi97@gmail.com>        
******************************************************"""        
@app.route('/oauth/authorize', methods=['GET'])
def authorize():
    auth_details = oauth.query.filter_by(client_id= request.args.get("client_id")).first()
    #Check for client_id in db
    if auth_details.__dict__["client_id"]:
        #Check for redirect uri in db, if match then make auth code
        if auth_details.__dict__["redirect_uri"] == request.args.get("redirect_uri"):
            authorization_code = jwt.encode({'client_id': request.args.get("client_id")}, 'Super_duper_secret', algorithm='HS256') 
            return "http://{0}/callback?code={1}".format(request.args.get("redirect_uri"),authorization_code.decode()), 302
        return jsonify({"error":"Invalid Redirect URI"}), 400
    return jsonify({"error":"Invalid Client Id"}), 400 
        


"""*****************************************************
Request URL: <url>/oauth/token
Example: localhost:5000/oauth/token?client_id=12345645&client_secret=4585sd54das5a&grant_type=authorization_code&code=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY3ODkifQ.pSnldg0lX4gom3nf_Cey04X3xYdSF2xGukQEkPKGwhY&redirect_uri=www.google.com
Request Type: GET
Request Input: Params grant type, redirect URI, client id, client secret, code
Expected Output:  JSON Object
        {
          "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY0NSIsImV4cCI6MTQ5NDEyODkzNCwiaWF0IjoxNDk0MTI4OTM0LCJ0eXBlIjoiYWNjZXNzIn0.IsLqkBcAM4Gk8yXWhg-kXpWZMA8pRYMkRWM7SsTJNQA",
          "expires_in": "300000",
          "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY0NSIsImV4cCI6MTQ5NDEyODkzNCwiaWF0IjoxNDk0MTI4OTM0LCJ0eXBlIjoicmVmcmVzaCJ9.xCv9QosOfjSQ_LvjBdFFmYDSPyMFtWkzJcEul6pJwIM",
          "token_type": "Basic"
        }  
Developed By Shubham Rathi <shubham.rathi97@gmail.com>        
******************************************************"""        
@app.route('/oauth/token', methods=['GET'])
def token():
    auth_details = oauth.query.filter_by(client_id= request.args.get("client_id")).first()
    if not auth_details:
        return jsonify({"error":"Client_id Not Found"}), 404 
    
    if auth_details.__dict__["redirect_uri"] != request.args.get("redirect_uri"):
        return jsonify({"error":"Invalid redirect_uri"}), 400
    
    if auth_details.__dict__["client_secret"] != request.args.get("client_secret"):
        print(auth_details.__dict__["client_secret"])
        print(request.args.get("client_secret"))
        return jsonify({"error":"Invalid client_secret"}), 400        
    
    if request.args.get("grant_type") == "authorization_code":
        authorization_code_decoded = jwt.decode(request.args.get("code"), 'Super_duper_secret', algorithms=['HS256'])
        if authorization_code_decoded["client_id"] != request.args.get("client_id"):
            return jsonify({"error":"Invalid authorization code"}), 400

    elif request.args.get("grant_type") == "refresh_token":
        refresh_token_decoded = jwt.decode(request.args.get("refresh_token"), 'Super_duper_secret', algorithms=['HS256'])
        if refresh_token_decoded["type"] != "refresh":
            return jsonify({"error":"Invalid refresh token"}), 400
    else:
        return jsonify({"error":"Invalid Request"}), 400

    access_token = jwt.encode({'client_id': request.args.get("client_id"),
                        'exp': datetime.utcnow(),
                        'iat': datetime.utcnow(),
                        'type':'access'}, "Super_duper_secret" , algorithm='HS256')

    refresh_token = jwt.encode({'client_id': request.args.get("client_id"),
                        'exp': datetime.utcnow(),
                        'iat': datetime.utcnow(),
                        'type':'refresh'}, "Super_duper_secret" , algorithm='HS256')
    
    return jsonify({ 
                        "access_token"  : access_token.decode(),
                        "token_type"    : "Basic",
                        "expires_in"    : "300000",
                        "refresh_token" : refresh_token.decode(),
                    })

