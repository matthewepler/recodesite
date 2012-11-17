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
	api_link = StringField()
	slug = StringField()
	description = StringField()
	hasTranslation = StringField()

class Artist( EmbeddedDocument ):
	name = StringField();
	bio = StringField();
	photo_link = StringField();
	links = ListField( StringField() )


class Translation( Document ):
	title = StringField()
	artist = StringField()
	orig_artist = StringField()
	orig_title = StringField()
	photo_link = StringField()
	repo_link = StringField()
	category = StringField()
	slug = StringField()
	artwork_slug = StringField()
	files = ListField( StringField() )
	file_links = ListField( StringField() )
	raw_files = ListField( StringField() )

class Volume( Document ):
	title = StringField()
	volume_detail = StringField()
	download_link = StringField()



# ------ FORMS ----------
ArtworkForm = model_form( Artwork )
ArtistForm = model_form( Artist )
TranslationForm = model_form( Translation )