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


#------------------------------------- MAIN PAGE >>>
@app.route( "/" )
def index():

	artworks = models.Artwork.objects()

	templateData = {
		'artworks' : artworks,
	}

	return render_template( "index.html", **templateData )

@app.route("/test")
def test():
	# script1 = Markup("<script src='/static/js/processing.js'></script><script type='text/processing' data-processing-target='mycanvas'>")
	# script2 = Markup("</script>")
	# canvas = Markup("<canvas id='mycanvas' width='1000' height='1000' style='margin-top:8%;margin-left:40%;margin-bottom:100px'></canvas>")

	# templateData = {
	# 	'script1' : script1,
	# 	'canvas' : canvas,
	# 	'script2' : script2
	# }

	return render_template("/test.html")


@app.route("/submit/<artwork_slug>", methods=['GET', 'POST'])
def submit( artwork_slug ):
	
	orig = models.Artwork.objects.get( slug = artwork_slug )
	submit_form = models.TranslationForm(request.form)

	if request.method == "POST":
	
		translation = models.Translation()

		translation.title = request.form.get('title', 'untitled')
		app.logger.debug( request.form.get('title') )

		translation.artist = request.form.get('artist')
		app.logger.debug( request.form.get('artist' ) )

		translation.category = request.form.get('category')
		app.logger.debug( request.form.get('category') )

		translation.description = request.form.get('description', 'None')
		app.logger.debug( request.form.get('description') 
			)
		translation.code = request.form.get('code')
		app.logger.debug( request.form.get('code') )

		translation.artwork_slug = orig.slug
		translation.slug = slugify( translation.artist + "-" + translation.category + "-" + orig.title + "-" + orig.artist )
		
		translation.save()

		script1 = Markup("<script src='/static/js/processing.js'></script><script type='text/processing' data-processing-target='mycanvas'>")
		script2 = Markup("</script>")
		canvas = Markup("<canvas id='mycanvas' width='1000' height='1000' style='margin-top:8%;margin-left:40%;margin-bottom:100px'></canvas>")
		
		
		templateData = {
			'translation' : translation,
			'orig' : orig,
			'script1' : script1,
			'canvas' : canvas,
			'script2' : script2
		}

		return render_template("success.html", **templateData)
		

	else:
		

		return render_template("submit.html", orig=orig)



@app.route( "/artwork/<artwork_slug>" )
def artwork( artwork_slug ):
	
	translations = []

	artwork = models.Artwork.objects.get( slug = artwork_slug )

	allTranslations = models.Translation.objects()
	for t in allTranslations:
		if t.artwork_slug in artwork_slug:
			translations.append(t)

	templateData = {
		'artwork' : artwork,
		'translations': translations
	}

	return render_template("artwork.html", **templateData)


@app.route( "/translation/<trans_slug>")
def translation(trans_slug):

	scriptTag = Markup("<script type='application/processing' target='mysketch'>")
	code = ""
	scriptTag2 = Markup("</script>")
	canvasTag = Markup("<canvas id='mysketch' width='1000' height='1000' style='margin-top:8%;margin-left:40%;margin-bottom:100px'></canvas>")
	
	orig = None
	translation = models.Translation.objects.get( slug=trans_slug )
	

	allArtworks = models.Artwork.objects()
	for a in allArtworks:
		if translation.orig_title in a.title:	
			orig = a


	templateData = {
		'translation' : translation,
		'original' : orig,
		'script1' : scriptTag,
		'code' : code,
		'canvas' : canvasTag,
		'script2' : scriptTag2
	}

	return render_template("translation.html", **templateData)


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
						app.logger.debug( artwork.title + " - " + artwork.artist )

						data_request = requests.get( artwork.api_link + authentication_str )
						data = data_request.json
						for folder in data:
							if folder is not None: # if there are translation folders inside the categories, go in
								fType = folder['type'].decode('UTF-8', 'strict')
								fName = folder['name'].decode('UTF-8', 'strict')
								if fType == "dir":
									folder_name = folder['name'].decode('UTF-8', 'strict')
									category = folder_name[2:]
									app.logger.debug("category:" + category)
									contents_req = requests.get( folder['url'] + authentication_str )
									contents_data = contents_req.json
									for artist in contents_data:
										artistName = artist['name'].decode('UTF-8', 'strict')
										if not ".txt" in artistName:
											app.logger.debug("artistName: " + artistName)
											repo_link = artist['html_url'].decode('UTF-8', 'strict')
											app.logger.debug("repo_link: " + repo_link)
											artist_contents_req = requests.get( artist['url'] + authentication_str)
											artist_contents = artist_contents_req.json
											for project in artist_contents:
												projectName = project['name'].decode('UTF-8', 'strict')
												app.logger.debug("projectName: " + projectName)
												project_contents_req = requests.get( project['url'] + authentication_str)
												project_data = project_contents_req.json
												for pFile in project_data:
													if pFile is not None:
														filename = pFile['name'].decode('UTF-8', 'strict')
														file_link = pFile['url'].decode('UTF-8', 'strict')
														photo_link = ""
														if "png" in filename:
																photo_link = pFile['html_url'].decode('UTF-8', 'strict')
																app.logger.debug("photo_link: " + photo_link)
														elif "jpg" in filename:
																photo_link = pFile['html_url'].decode('UTF-8', 'strict')
																app.logger.debug("photo_link: " + photo_link)
															
														translation = models.Translation()
														translation.slug = slugify( artistName + category + filename )
														
														app.logger.debug( "slugify = " + artistName + " + " + category + " + " + filename)
														
														translation.photo_link = photo_link
														translation.file_links.append(file_link)
														translation.files.append(filename)
														translation.title = projectName
														translation.repo_link = repo_link
														translation.artist = artistName
														translation.category = category
														
														translation.orig_artist = artwork.artist
														translation.orig_title = artwork.title
														translation.artwork_slug = artwork.slug
														translation.save()
									
	
	def updatethatshit():
		allArtworks = models.Artwork.objects()
		for a in allArtworks:
			if "v1" in a.source_detail:
				a.date = "1976"
				a.save()
			if "v2" in a.source_detail:
				a.date = "1977"
				a.save()
			if "v3" in a.source_detail:
				a.date = "1978"
				a.save()


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
	updatethatshit()

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



	