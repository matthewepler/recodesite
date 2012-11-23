# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form


class Translation( Document ):
	title = StringField()
	artist = StringField(required=True)
	category = StringField(required=True)
	slug = StringField()
	artwork_slug = StringField()
	file_links = ListField( StringField() )
	code = StringField()
	photo_link = StringField()
	description = StringField()
	video = StringField()

class Artwork( Document ):
	title = StringField()
	artist = StringField()
	source = StringField()
	source_detail = StringField()
	source_link = StringField()
	date = StringField()
	photo_link = StringField()
	code_link = StringField()
	slug = StringField()
	description = StringField()
	hasTranslation = StringField()



# ------ FORMS ----------
ArtworkForm = model_form( Artwork )
TranslationForm = model_form( Translation )