from datetime import datetime

import jwt
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from app.model import db
from .model import OauthModel

oauth_api = Blueprint("oauth_api", __name__)

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


@oauth_api.route('/add_oauth', methods=['POST'])
def add_oauth():
    raw_dict = request.get_json(force=True)
    try:
        temp = OauthModel(raw_dict["client_id"], raw_dict["client_secret"], raw_dict["redirect_uri"])
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


@oauth_api.route('/oauth/authorize', methods=['GET'])
def authorize():
    auth_details = OauthModel.query.filter_by(client_id=request.args.get("client_id")).first()
    # Check for client_id in db
    if auth_details.__dict__["client_id"]:
        # Check for redirect uri in db, if match then make auth code
        if auth_details.__dict__["redirect_uri"] == request.args.get("redirect_uri"):
            authorization_code = jwt.encode({'client_id': request.args.get("client_id")}, 'Super_duper_secret',
                                            algorithm='HS256')
            return "http://{0}/callback?code={1}".format(request.args.get("redirect_uri"),
                                                         authorization_code.decode()), 302
        return jsonify({"error": "Invalid Redirect URI"}), 400
    return jsonify({"error": "Invalid Client Id"}), 400


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


@oauth_api.route('/oauth/token', methods=['GET'])
def token():
    auth_details = OauthModel.query.filter_by(client_id=request.args.get("client_id")).first()
    if not auth_details:
        return jsonify({"error": "Client_id Not Found"}), 404

    if auth_details.__dict__["redirect_uri"] != request.args.get("redirect_uri"):
        return jsonify({"error": "Invalid redirect_uri"}), 400

    if auth_details.__dict__["client_secret"] != request.args.get("client_secret"):
        print(auth_details.__dict__["client_secret"])
        print(request.args.get("client_secret"))
        return jsonify({"error": "Invalid client_secret"}), 400

    if request.args.get("grant_type") == "authorization_code":
        authorization_code_decoded = jwt.decode(request.args.get("code"), 'Super_duper_secret', algorithms=['HS256'])
        if authorization_code_decoded["client_id"] != request.args.get("client_id"):
            return jsonify({"error": "Invalid authorization code"}), 400

    elif request.args.get("grant_type") == "refresh_token":
        refresh_token_decoded = jwt.decode(request.args.get("refresh_token"), 'Super_duper_secret',
                                           algorithms=['HS256'])
        if refresh_token_decoded["type"] != "refresh":
            return jsonify({"error": "Invalid refresh token"}), 400
    else:
        return jsonify({"error": "Invalid Request"}), 400

    access_token = jwt.encode({'client_id': request.args.get("client_id"),
                               'exp': datetime.utcnow(),
                               'iat': datetime.utcnow(),
                               'type': 'access'}, "Super_duper_secret", algorithm='HS256')

    refresh_token = jwt.encode({'client_id': request.args.get("client_id"),
                                'exp': datetime.utcnow(),
                                'iat': datetime.utcnow(),
                                'type': 'refresh'}, "Super_duper_secret", algorithm='HS256')

    return jsonify({
        "access_token": access_token.decode(),
        "token_type": "Basic",
        "expires_in": "300000",
        "refresh_token": refresh_token.decode(),
    })
