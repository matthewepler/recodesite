# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * 
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime
from flask.ext.security import UserMixin, RoleMixin



class Translation( mongoengine.Document ):
	title = mongoengine.StringField(required=True)
	artist = mongoengine.StringField(required=True)
	artist_url = mongoengine.StringField()
	artist_email = mongoengine.StringField(required=True)
	category = mongoengine.StringField(required=True)
	slug = mongoengine.StringField()
	artwork_slug = mongoengine.StringField()
	photo_link = mongoengine.StringField(required=True)
	pde_link = mongoengine.StringField()  # depreciated 01/10/13
	js = mongoengine.BooleanField()
	description = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())
	video = mongoengine.StringField()	  # depreciated 12/21/12
	code = mongoengine.StringField(required=True)	

class Artwork( mongoengine.Document ):
	title = mongoengine.StringField()
	artist = mongoengine.StringField()
	source = mongoengine.StringField()
	source_detail = mongoengine.StringField()
	source_link = mongoengine.StringField()
	date = mongoengine.StringField()
	photo_link = mongoengine.StringField()
	code_link = mongoengine.StringField()
	slug = mongoengine.StringField()
	description = mongoengine.StringField()
	hasTranslation = mongoengine.StringField()

class Role(mongoengine.Document, RoleMixin):
    name = mongoengine.StringField(max_length=80, unique=True)
    description = mongoengine.StringField(max_length=255)

class User(mongoengine.Document, UserMixin):
    email = mongoengine.StringField(max_length=255)
    password = mongoengine.StringField(max_length=255)
    active = mongoengine.BooleanField(default=True)
    confirmed_at = mongoengine.DateTimeField()
    last_login_at = mongoengine.DateTimeField()
    current_login_at = mongoengine.DateTimeField()
    last_login_ip = mongoengine.DateTimeField()
    current_login_ip = mongoengine.DateTimeField()
    login_count = mongoengine.DateTimeField()
    roles = mongoengine.ListField(mongoengine.ReferenceField(Role), default=[])


class Connection(mongoengine.Document):
    id = mongoengine.IntField(primary_key=True)
    user_id = mongoengine.ReferenceField('User', dbref=True)
    provider_id = mongoengine.StringField(max_length=255)
    provider_user_id = mongoengine.StringField(max_length=255)
    access_token = mongoengine.StringField(max_length=255)
    secret = mongoengine.StringField(max_length=255)
    display_name = mongoengine.StringField(max_length=255)
    profile_url = mongoengine.StringField(max_length=512)
    image_url = mongoengine.StringField(max_length=512)
    rank = mongoengine.IntField()



# ------ FORMS ----------
ArtworkForm = model_form( Artwork )
TranslationForm = model_form( Translation )

class upload_form( TranslationForm ):
	photo_upload = FileField('jpg, png, or gif', validators=[])
	file_upload = FileField('place all code in a single .pde file')