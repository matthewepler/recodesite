# -*- coding: utf-8 -*-
from datetime import datetime
from flask_mongoengine import MongoEngine


db = MongoEngine()


class Translation(db.Document):
    meta = {'strict': False}
    title = db.StringField(required=True)
    artist = db.StringField(required=True)
    artist_url = db.StringField()
    artist_email = db.StringField(required=True)
    category = db.StringField(required=True)
    slug = db.StringField()
    artwork_slug = db.StringField()
    photo_link = db.StringField(required=True)
    pde_link = db.StringField()  # depreciated 01/10/13, brought back 01/16/13
    js = db.BooleanField()
    description = db.StringField()
    timestamp = db.DateTimeField(default=datetime.now())
    video = db.StringField()  # depreciated 12/21/12
    code = db.StringField(required=True)


class Artwork(db.Document):
    meta = {'strict': False}
    title = db.StringField()
    artist = db.StringField()
    source = db.StringField()
    source_detail = db.StringField()
    source_link = db.StringField()
    date = db.StringField()
    photo_link = db.StringField()
    code_link = db.StringField()
    slug = db.StringField()
    description = db.StringField()
    hasTranslation = db.StringField()
