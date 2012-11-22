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
		translation.photo = "/static/img/trans/" + request.form.get('photo')
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


# -------------------------------------------------------------------- LIST >>>
@app.route("/translationslist/<filter_str>")
def translationslist( filter_str ):

	filtered_list = []

	allArtworks = models.Artwork.objects()
	if filter_str == "hasTranslation":
		for a in allArtworks:
			if a.hasTranslation == "yes":
				filtered_list.append( a )
	else:
		filtered_list = sorted(allArtworks, key=lambda k: k[filter_str]) 

	templateData = {
		'artworks' : filtered_list,
	}

	return render_template("translationslist.html", **templateData)


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



	