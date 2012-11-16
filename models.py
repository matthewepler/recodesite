# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form

class Artwork( Document ):
	title = StringField()
	artist = StringField()
	source = StringField()
	source_detail = StringField()
	source_link = StringField()
	date = StringField()
	language = StringField()
	photo_link = StringField()
	code_link = StringField()
	slug = StringField()


class Artist( EmbeddedDocument ):
	name = StringField();
	bio = StringField();
	photo_link = StringField();
	links = ListField( StringField() )


class Translation( EmbeddedDocument ):
	title = StringField()
	artist = StringField()
	artist_url = StringField()
	language = StringField()
	photo_link = StringField()
	code_link = StringField()


# ------ FORMS ----------
ArtworkForm = model_form( Artwork )
ArtistForm = model_form( Artist )
TranslationForm = model_form( Translation )