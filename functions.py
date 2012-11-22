# functions.py

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