import os, json, requests
import re
from unidecode import unidecode

from flask import Flask, jsonify, request, render_template, redirect, abort
from mongoengine import *
from flask.ext.mongoengine import mongoengine

import models

connect( 'mydata', host=os.environ.get('MONGOLAB_URI') )

app = Flask(__name__)   


#------------------------------------- MAIN PAGE >>>
@app.route( "/" )
def index():

	return render_template("index.html")


@app.route("/translations")
def translations():

	artworks = models.Artwork.objects();
	for a in artworks:
		app.logger.debug( a )

	templateData = {
		'artworks' : artworks
	}

	return render_template("translationslist.html", **templateData)


@app.route( "/maketranslationobjects" )
def maketranslationobjects():

	authentication_str = "?client_id=a199482938d9ff482aba&client_secret=189a51834c73b9ae638c89352049fe615995c746"
	base_url = "https://api.github.com/repos/matthewepler/ReCode_Project/contents/Computer_Graphics_and_Art" + authentication_str
	downloads_url = "https://api.github.com/repos/matthewepler/ReCode_Project/downloads"+ authentication_str

	def getRepoContents( url_str ):
		data_request = requests.get( url_str )
		data = data_request.json

		# for every folder in the repo base directory...
		for vol in data: 
			name = vol['name']
			volume = name[1]
			number = name[3]
			if name.startswith('v'):
				links = vol['_links']
				vol_link = links['self']
				vol_request = requests.get( vol_link + authentication_str )
				vol_data = vol_request.json
				# for every artwork folder in the volume directory...
				for piece in vol_data:
					title_temp = piece['name']
					if "-" in title_temp:

						artwork = models.Artwork()
						title_broken = title_temp.split( "-" )
						title = title_broken[0].replace( "_" , " ")
						piecenum = title[:2]
						title = title[3:]
						artist = title_broken[1].replace( "_" , " ")

						for d in downloads:
							descrip_str = d['description'].encode( 'ascii', 'ignore')
							if volume in descrip_str and number in descrip_str and descrip_str.find(volume) > descrip_str.find(number):
								artwork.source_link = d['html_url']

						artwork.title = title
						artwork.artist = artist
						artwork.source = "Computer Graphics and Art"
						artwork.source_detail = vol['name']
						artwork.photo_link = "/static/img/cards/" + vol['name'] + "/" + piecenum + ".png"
						artwork.slug = slugify( artwork.source_detail + artwork.title)
						artwork.save()
						app.logger.debug( artwork )

	return redirect("/translations")
						

	def getDownloads( url_str ):
		data_request = requests.get( url_str + authentication_str )
		data = data_request.json
		for d in data:
			downloads.append(d)
		app.logger.debug( "got your downloads, dude" )

	downloads = []
	getDownloads( downloads_url )
	getRepoContents( base_url )


# --------------------------------------------------------- KILL ALL ARTWORKS!
@app.route("/killallartworks")
def killallartworks():

	artworks = models.Artwork.objects()
	for a in artworks:
		a.delete()

	app.logger.debug( "all Artwork objects destroyed" )
	return redirect("/")		


#------------------------------------- 404 HANDLER >>>
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



#------------------------------------- SERVER START-UP >>>
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	