import os, json, requests
import re
from unidecode import unidecode

from flask import Flask, jsonify, request, render_template, redirect, abort, Markup
from flask.ext.mongoengine import mongoengine

import models

mongoengine.connect( 'mydata', host=os.environ.get('MONGOLAB_URI') )
AUTH_STR = os.environ.get('AUTH_STR')

app = Flask(__name__)   
app.config['CSRF_ENABLED'] = False


# ----------------------------------------------------------------- HOME >>>
@app.route( "/" )
def index():

	artworks = models.Artwork.objects()

	templateData = {
		'artworks' : artworks,
	}

	return render_template( "index.html", **templateData )


# ---------------------------------------------------------------- SUBMIT >>>
@app.route("/submit/<artwork_slug>", methods=['GET', 'POST'])
def submit( artwork_slug ):
	
	orig = models.Artwork.objects.get( slug = artwork_slug )
	submit_form = models.TranslationForm(request.form)

	if request.method == "POST":
	
		translation = models.Translation()

		translation.title = request.form.get('title', 'untitled')
		translation.artist = request.form.get('artist')
		translation.category = request.form.get('category')
		translation.photo_link = "/static/img/trans/" + request.form.get('photo')
		translation.description = request.form.get('description', 'None')
		translation.code = request.form.get('code')
		translation.video = Markup( request.form.get('video') )
		translation.artwork_slug = orig.slug
		translation.slug = slugify( translation.artist + "-" + translation.category + "-" + orig.title + "-" + orig.artist )
		translation.save()

		orig.hasTranslation = "yes"
		orig.save()

		templateData = {
			'translation' : translation,
			'orig' : orig,
		}

		return redirect("/translation/%s" % translation.slug)
		
	else:
		
		return render_template("submit.html", orig=orig)


# ---------------------------------------------------------------- ARTWORK >>>
@app.route( "/artwork/<artwork_slug>" )
def artwork( artwork_slug ):
	
	NoneString = ""	
	artwork = models.Artwork.objects.get( slug = artwork_slug )

	translations = []
	allTranslations = models.Translation.objects()
	for t in allTranslations:
		if t.artwork_slug == artwork_slug:
			translations.append(t)

	if len(translations) == 0:
		NoneString = "(None)"

	templateData = {
		'artwork' : artwork,
		'translations': translations,
		'NoneString' : NoneString
	}

	return render_template("artwork.html", **templateData)


# ------------------------------------------------------------- TRANSLATION >>>
@app.route( "/translation/<trans_slug>")
def translation(trans_slug):

	translation = models.Translation.objects.get( slug=trans_slug )
	orig = models.Artwork.objects.get( slug=translation.artwork_slug )

	templateData = {
		'translation' : translation,
		'orig' : orig,
	}

	return render_template("translation.html", **templateData)


# -------------------------------------------------------- ALL TRANSLATIONS >>>
@app.route("/alltranslations")
def alltranslations():

	translations = []

	allTranslations = models.Translation.objects()
	for t in allTranslations:
		translations.append( t )

	templateData = {
		'translations' : translations
	}

	return render_template("alltranslations.html", **templateData)


# -------------------------------------------------------------------- LIST >>>
@app.route("/translationslist", methods=['GET', 'POST'] )
def translationslist():

	filter_str = request.form.get( 'filter' )
	app.logger.debug(filter_str)

	artworks = []
	translations = []

	allArtworks = models.Artwork.objects()
	if filter_str == "hasTranslation":
		for a in allArtworks:
			if a.hasTranslation == "yes":
				artworks.append( a )
	elif filter_str == "noTranslation":
		for a in allArtworks:
			if a.hasTranslation == None:
				artworks.append( a )
	elif filter_str == "direct":
		allTranslations = models.Translation.objects()
		for t in allTranslations:
			if t.category == "direct":
				translations.append( t )
	elif filter_str == "experimental":
		allTranslations = models.Translation.objects()
		for t in allTranslations:
			if t.category == "experimental":
				translations.append( t )
	else:
		filtered_list = sorted(allArtworks, key=lambda k: k[filter_str]) 

	templateData = {
		'artworks' : artworks,
		'translations' : translations
	}

	return render_template("translationslist.html", **templateData)


# -------------------------------------------------------------- SEARCH >>>
@app.route("/search", methods=['POST'])
def search():

	artworks = []
	translations = []
	allTranslations = models.Translation.objects()

	search_str = request.form.get( 'keyword' )
	app.logger.debug( search_str )
	search_words = search_str.split()
	for word in search_words:
		word.replace(",", "")

		artwork_title = models.Artwork.objects(title__icontains=word)
		if artwork_title is not None:
			for title in artwork_title:
				artworks.append( title )
				for t in allTranslations:
					if t.artwork_slug == title.slug:
						translations.append( t )
		artwork_artist = models.Artwork.objects(artist__icontains=word)
		if artwork_artist is not None:
			for artist in artwork_artist:
				artworks.append( artist )
				for t in allTranslations:
					if t.artwork_slug == artist.slug:
						translations.append( t )
		artwork_source = models.Artwork.objects(source__icontains=word)
		if artwork_source is not None:
			for source in artwork_source:
				artworks.append( source )
				for t in allTranslations:
					if t.artwork_slug == source.slug:
						translations.append( t )
		artwork_date = models.Artwork.objects(date__icontains=word)
		if artwork_date is not None:
			for date in artwork_date:
				artworks.append( date )
				for t in allTranslations:
					if t.artwork_slug == date.slug:
						translations.append( t )
		artwork_descr = models.Artwork.objects(description__icontains=word)
		if artwork_descr is not None:
			for descr in artwork_descr:
				artworks.append( descr )
				for t in allTranslations:
					if t.artwork_slug == descr.slug:
						translations.append( t )


		translation_title = models.Translation.objects(title__icontains=word)
		if translation_title is not None:
			for title in translation_title:
				translations.append( title )
		translation_artist = models.Translation.objects(artist__icontains=word)
		if translation_artist is not None:
			for artist in translation_artist:
				translations.append( artist )
		translation_orig = models.Translation.objects(artwork_slug__icontains=word)
		if translation_orig is not None:
			for orig in translation_orig:
				translations.append( orig )
		translation_descr = models.Translation.objects(description__icontains=word)
		if translation_descr is not None:
			for descr in translation_descr:
				translations.append( descr )

	if len(artworks) > 0  or len(translations) > 0:
		error_str = ""
		templateData = {
			'artworks' : artworks,
			'translations' : translations,
			'error_str' : error_str,
			'search_str' : search_str
		}
		return render_template("searchresults.html", **templateData)
	else:
		error_str = "No results were returned. If you think this is an error, please send us an email using the mail icon at the top-right of your screen."
		return render_template("searchresults.html", error_str=error_str)



# ---------------------------------------------------------------- TEST >>>
@app.route("/test")
def test():

	allTranslations = models.Translation.objects()

	for t in allTranslations:
		artwork = models.Artwork.objects.get( slug=t.artwork_slug )
		artwork.hasTranslation = "yes"
		artwork.save()
		app.logger.debug( artwork.hasTranslation )

	return render_template("/test.html")
	# allTranslations = models.Translation.objects()
	# for t in allTranslations:
	# 	t.update( {$rename : {photo : photo_link }} )

	# return redirect("/")

#----------------------------------------------------------- 404 HANDLER >>>
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Slugify the title to create URLS
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))



#--------------------------------------------------------- SERVER START-UP >>>
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	