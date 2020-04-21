from app.model import db


class OauthModel(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    client_id = db.Column(db.String(255), unique=True)
    client_secret = db.Column(db.String(255))
    redirect_uri = db.Column(db.String(255))

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
