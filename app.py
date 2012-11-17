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

	artworks = models.Artwork.objects()

	templateData = {
		'artworks' : artworks,
	}

	return render_template( "index.html", **templateData )



@app.route( "/translation/<trans_slug>")
def translation(trans_slug):

	orig = None

	translation = models.Translation.objects.get( slug=trans_slug )
	
	allArtworks = models.Artwork.objects()
	for a in allArtworks:
		if translation.orig_title in a.title:	
			orig = a

	templateData = {
		'translation' : translation,
		'original' : orig
	}

	return render_template("translation.html", **templateData)



@app.route( "/artwork/<artwork_slug>" )
def artwork( artwork_slug ):
	
	translations = []

	artwork = models.Artwork.objects.get( slug = artwork_slug)
	authentication_str = "?client_id=a199482938d9ff482aba&client_secret=189a51834c73b9ae638c89352049fe615995c746"
	data_request = requests.get( artwork.api_link + authentication_str )
	data = data_request.json
	for f in data:
		if not f['name'].startswith("_"):
			catLink = f['url']
			catName = f['name']
			catName = catName[2:]
			cat_request = requests.get( catLink + authentication_str )
			catData = cat_request.json
			if len(catData) > 2:
				for c in catData:
					if not c['name'].startswith("_"):
						artist = c['name'].replace("_", " ")
						data_url = c['url']

						test = models.Translation()
						test.artist = artist
						test.data_link = data_url
						test.repo_link = catLink
						test.category = catName
						test.artwork_slug = artwork_slug
						test.orig_artist = artwork.artist
						test.orig_title = artwork.title
						test.slug = slugify( artist + "-" + catName + "-" + artwork.artist )

						hazTest = "no"

						allTranslations = models.Translation.objects()
						for a in allTranslations:
							if a.artwork_slug is artwork_slug:
								translations.append(t)

						for t in translations:
							if t.repo_link == test.repo_link:
								hazTest = "yes"
						if hazTest is "no":
							test.save()
							translations.append(test)


	templateData = {
		'artwork' : artwork,
		'translations': translations
	}

	return render_template("artwork.html", **templateData)


@app.route("/translationslist/<filter_str>")
def translationslist( filter_str ):

	filtered_list = {}

	artworks = models.Artwork.objects()
	if filter_str is "hasTranslation":
		for a in artworks:
			if a.hasTranslation == "yes":
				filtered_list.append( a )
	else:
		filtered_list = sorted(artworks, key=lambda k: k[filter_str]) 

	templateData = {
		'artworks' : filtered_list,
	}

	return render_template("translationslist.html", **templateData)



@app.route( "/makedatamagic" )
def makedatamagic():

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
						artwork.code_link = piece['html_url']
						artwork.api_link = piece['url']
						artwork.save()
						app.logger.debug( artwork )

						data_request = requests.get( artwork.api_link + authentication_str )
						data = data_request.json
						for folder in data:
						if folder is not None:
							fType = folder['type'].decode('UTF-8', 'strict')
							fName = folder['name'].decode('UTF-8', 'strict')
							if fType == "dir":
								folder_name = folder['name'].decode('UTF-8', 'strict')
								category = folder_name[2:]
								app.logger.debug("category:" + category)
								translation = models.Translation()
								translation.category = category
								contents_req = requests.get( folder['url'] + authentication_str )
								contents_data = contents_req.json
								for artist in contents_data:
									artistName = artist['name'].decode('UTF-8', 'strict')
									if not ".txt" in artistName:
										app.logger.debug("artistName: " + artistName)
										translation.artist = artistName
										repo_link = artist['url'].decode('UTF-8', 'strict')
										app.logger.debug("repo_link: " + repo_link)
										translation.repo_link = repo_link
										artist_contents_req = requests.get( artist['url'] + authentication_str)
										artist_contents = artist_contents_req.json
										for project in artist_contents:
											app.logger.debug(project)
											projectName = project['name'].decode('UTF-8', 'strict')
											app.logger.debug("projectName: " + projectName)
											translation.title = projectName
											project_contents_req = requests.get( project['url'] + authentication_str)
											project_data = project_contents_req.json
											for pFile in project_data:
												filename = pFile['name'].decode('UTF-8', 'strict')
												app.logger.debug("filename: " + filename)
												translation.files.append(filename)
												file_link = pFile['url']
												app.logger.debug("file_link: " + file_link)
												translation.file_links.append(file_link)
												if ".png" in filename:
													photo_link = pFile['html_url']
													app.logger.debug("photo_link: " + photo_link)

													translation.photolink = photo_link
												elif ".jpg" in filename:
													photo_link = pFile['html_url']
													app.logger.debug("photo_link: " + photo_link)

													translation.photo_link = photo_link
												elif ".pde" in filename:
													raw_request = requests.get( file_link + authentication_str)
													raw_data = raw_request.json
													raw = raw_data['content']
													raw_encoded = raw.decode('base64', 'strict')
													translation.raw_files.append( raw_encoded )
													translation.raw_files.append( raw_encoded )

													translation.slug = slugify( artistName + category + filename )

								translation.orig_artist = artwork.artist
								translation.orig_title = artwork.title
								translation.artwork_slug = artwork.slug
								translation.save()

								app.logger.debug(translation.slug)

		return redirect("/")
						

	def getDownloads( url_str ):
		data_request = requests.get( url_str + authentication_str )
		data = data_request.json
		for d in data:
			volume = models.Volume()
			title_str = d['name']
			volume.title = title_str[:-12].replace( "_", " ").title()
			volume_str = title_str[26:-4]
			volume.volume_detail = volume_str[:3] + " " + volume_str[3:]
			volume.download_link = d['html_url']
			downloads.append(d)
			app.logger.debug( volume.title )
			volume.save()

	downloads = []
	getDownloads( downloads_url )
	getRepoContents( base_url )


# --------------------------------------------------------- UPDATES
@app.route("/updatethatshit")
def updatethatshit():

	allArtworks = models.Artwork.objects()
	for a in allArtworks:
		if "v1" in a.source_detail:
			a.date = "1976"
		if "v2" in a.source_detail:
			a.date = "1977"
		if "v3" in a.source_detail:
			a.date = "1978"

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



	