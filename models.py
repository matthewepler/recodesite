# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime


class Translation( mongoengine.Document ):
	title = mongoengine.StringField()
	artist = mongoengine.StringField(required=True)
	artist_url = mongoengine.StringField()
	category = mongoengine.StringField(required=True)
	slug = mongoengine.StringField()
	artwork_slug = mongoengine.StringField()
	photo_link = mongoengine.StringField()
	pde_link = mongoengine.StringField()
	js = mongoengine.BooleanField()
	description = mongoengine.StringField()
	width = mongoengine.StringField()
	height = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())
	video = mongoengine.StringField()	# depreciated 12/21/12
	code = mongoengine.StringField()	# depreciated 12/21/12

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



# ------ FORMS ----------
ArtworkForm = model_form( Artwork )
TranslationForm = model_form( Translation )

class upload_form( TranslationForm ):
	photo_upload = FileField('jpg, png, or gif', validators=[])
	file_upload = FileField('place all code in a single .pde file')