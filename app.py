import os, datetime, re
from unidecode import unidecode
from werkzeug import secure_filename
from flask import Flask, request, render_template, redirect, Markup, current_app, session, flash, url_for
from flask.ext.assets import Environment


from flask.ext.mongoengine import mongoengine
from flask.ext.mongoengine import MongoEngine


from flask.ext.security import Security, MongoEngineUserDatastore
from flask.ext.social import Social, login_failed
from flask.ext.social.utils import get_conection_values_from_oauth_response
from flask.ext.security import login_required, LoginForm, current_user, login_user


from flask.ext.social.utils import get_provider_or_404
from flask.ext.social.views import connect_handler
import boto
import models, forms, tools
import github, twitter, facebook




# ----------------------------------------------------------------- APP CONFIG >>>
app = Flask(__name__)   
app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_TRACKABLE'] = True
app.config['CSRF_ENABLED'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MONGODB_DB'] = 'heroku_app8905639'
app.config['MONGODB_HOST'] = 'mongolab.com'
app.config['MONGODB_PORT'] = '43037'
app.config['SECRET_KEY'] = os.environ.get('AUTH_STR')


# ----------------------------------------------------------------- DATABASE CONNECTION >>>
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))

# ----------------------------------------------------------------- GLOBAL VARIABLES >>>
db = MongoEngine(app)
webassets = Environment(app)
user_datastore = MongoEngineUserDatastore(db, models.User, models.Role)
security = Security(app, user_datastore)

AUTH_STR = os.environ.get('AUTH_STR')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pde', 'js'])





# ---------------------------------------------------------------- HOME >>>
@app.route( "/" )
def index():

	artworks = models.Artwork.objects()

	templateData = {
		'artworks' : artworks,
	}

	return render_template( "index.html", **templateData )


# ----------------------------------------------------------------- LOGIN >>>
@app.route( "/login" )
def login():

    if current_user.is_authenticated():
        return redirect(request.referrer or '/')

    return render_template('login.html', form=LoginForm())

# ----------------------------------------------------------------- REGISTER >>>
@app.route('/register', methods=['GET', 'POST'])
@app.route('/register/<provider_id>', methods=['GET', 'POST'])
def register(provider_id=None):
    if current_user.is_authenticated():
        return redirect(request.referrer or '/')

    form = forms.RegisterForm()

    if provider_id:
        provider = get_provider_or_404(provider_id)
        connection_values = session.get('failed_login_connection', None)
    else:
        provider = None
        connection_values = None

    if form.validate_on_submit():
        ds = current_app.security.datastore
        user = ds.create_user(email=form.email.data, password=form.password.data)
        ds.commit()

        # See if there was an attempted social login prior to registering
        # and if so use the provider connect_handler to save a connection
        connection_values = session.pop('failed_login_connection', None)

        if connection_values:
            connection_values['user_id'] = user.id
            connect_handler(connection_values, provider)

        if login_user(user):
            ds.commit()
            flash('Account created successfully', 'info')
            return redirect(url_for('profile'))

        return render_template('/security/thanks.html', user=user)

    login_failed = int(request.args.get('login_failed', 0))

    return render_template('/security/register.html',
                           form=form,
                           provider=provider,
                           login_failed=login_failed,
                           connection_values=connection_values)



# ----------------------------------------------------------------- PROFILE >>>
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',
        twitter_conn=current_app.social.twitter.get_connection(),
        facebook_conn=current_app.social.facebook.get_connection(),
        google_conn=current_app.social.google.get_connection(),
        github_conn=current_app.social.github.get_connection())


@app.route('/profile/<provider_id>/post', methods=['POST'])
@login_required
def social_post(provider_id):
    message = request.form.get('message', None)

    if message:
        conn = getattr(current_app.social, provider_id).get_connection()
        api = conn['api']

        if provider_id == 'twitter':
            display_name = 'Twitter'
            api.PostUpdate(message)
        if provider_id == 'facebook':
            display_name = 'Facebook'
            api.put_object("me", "feed", message=message)

        flash('Message posted to %s: %s' % (display_name, message), 'info')

    return redirect(url_for('profile'))



# ----------------------------------------------------------------- ADMIN >>>
@app.route('/admin')
@tools.requires_auth
def admin():
    users = models.User.query.all()
    return render_template('admin.html', users=users)


@app.route('/admin/users/<user_id>', methods=['DELETE'])
@tools.requires_auth
def delete_user(user_id):
    user = models.User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'info')
    return redirect(url_for('admin'))


# ---------------------------------------------------------------- SUBMIT >>>
@app.route("/submit/<artwork_slug>", methods=['GET', 'POST'])
def submit( artwork_slug ):
	
	orig = models.Artwork.objects.get( slug = artwork_slug )
	submit_form = models.upload_form(request.form)

	if request.method == "POST":
		
		translation = models.Translation()

		translation.title = request.form.get('title') 				# required
		if translation.title == "":
			return "Please give your translation a title."
		translation.artist = request.form.get('artist')				# required
		if translation.artist == "":
			return "Please include your name."
		translation.artist_email = request.form.get('artist-email')	# required
		if translation.artist_email == "":
			return "Please include your email."
		translation.category = request.form.get('category')			# required, will default to 'direct'
		translation.artist_url = request.form.get('artist-url')
		translation.description = request.form.get('description', 'None')
		descriptionList = translation.description.split("\r\n")
		translation.video = Markup( request.form.get('video') )

		# IMAGE FILE
		photo_upload = request.files['photo-upload']
		if photo_upload and allowed_file(photo_upload.filename):
			now = datetime.datetime.now()
			filename = "p" + now.strftime('%Y%m%d%H%M%s') + secure_filename(photo_upload.filename)
			s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))
			b = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
			k = b.new_key(b)
			k.key = filename
			k.set_metadata("Content-Type", photo_upload.mimetype)
			k.set_contents_from_string(photo_upload.stream.read())
			k.make_public()

			if k and k.size > 0:		
				translation.photo_link = "https://s3.amazonaws.com/recode-files/" + filename

		else:
			return "Uhoh! There was an error uploading " + photo_upload.filename

		# Pasted Code String (required)
		translation.code = "/* \nPart of the ReCode Project (http://recodeproject.com)\n" + "Based on \"" + orig.title + "\" by " + orig.artist + "\n" + "Originally published in \"" + orig.source + "\" " + orig.source_detail + ", " + orig.date + "\nCopyright (c) " + now.strftime('%Y') + " " + translation.artist + " - " + "OSI/MIT license (http://recodeproject/license).\n*/\n\n/* @pjs pauseOnBlur='true'; */\n\n" + request.form.get('code').strip()
		# if translation.code == "":
		# 	return "Your code did not paste successfully. Please try again."

		# JS Boolean
		browser_note = "This sketch does not run in the browser."
		if request.form.get('js') == "True":
			translation.js = True
			browser_note = "This sketch is running in the browser."

		translation.artwork_slug = orig.slug
		translation.slug = slugify( translation.artist + "-" + translation.title + "-" + translation.category + "-" + orig.title + "-" + orig.artist )
		translation.description = translation.description + " " + browser_note
		translation.save()

		orig.hasTranslation = "yes"
		orig.save()

		templateData = {
			'translation' : translation,
			'orig' : orig,
			'descriptionList' : descriptionList
		}

		return redirect("/translation/%s" % translation.slug)
		
	else:

		templateData = {
			'form' : submit_form,
			'orig' : orig
		}
		
		return render_template("submit.html", **templateData)


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
	descriptionList = translation.description.split("\r\n")

	templateData = {
		'translation' : translation,
		'orig' : orig,
		'descriptionList': descriptionList
	}

	return render_template("translation.html", **templateData)


# -------------------------------------------------------- ALL TRANSLATIONS >>>
@app.route("/alltranslations")
def alltranslations():

	translations = []

	allTranslations = models.Translation.objects.order_by('-timestamp')
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
	elif filter_str == "artist":
		artworks = sorted(allArtworks, key=lambda k: k[filter_str])
	elif filter_str == "title":
		artworks = sorted(allArtworks, key=lambda k: k[filter_str])
	elif filter_str == "translator":
		allTranslations = models.Translation.objects()
		translations = sorted(allTranslations, key=lambda k: k["artist"])
	elif filter_str == "js":
		allTranslations = models.Translation.objects()
		for t in allTranslations:
			if t.js == True:
				translations.append( t )


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

@app.route("/license")
def license():


	return render_template("license.html")

# ---------------------------------------------------------------- TEST >>>
@app.route("/test")
def test():

	names = []

	allArtworks = models.Artwork.objects()
	for a in allArtworks:
		name = a.artist
		exists = True
		if exists == False:
			names.append( name )
			app.logger.debug( "* added: " + name )
		else:
			app.logger.debug( "! duplicate: " + name )

	templateData = {
		'names' : names
	}
				

	return render_template("/test.html", **templateData)
	# allTranslations = models.Translation.objects()
	# for t in allTranslations:
	# 	t.update( {$rename : {photo : photo_link }} )

	# return redirect("/")

#----------------------------------------------------------- 404 HANDLER >>>
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))


# ---------------------------------------------------------------- SERVER START-UP >>>
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) 
	app.run(host='0.0.0.0', port=port)

class SocialLoginError(Exception):
    def __init__(self, provider):
        self.provider = provider


@app.before_first_request
def before_first_request():
    try:
        models.db.create_all()
    except Exception, e:
        app.logger.error(str(e))


@app.context_processor
def template_extras():
    return dict(
        google_analytics_id=app.config.get('GOOGLE_ANALYTICS_ID', None))


@login_failed.connect_via(app)
def on_login_failed(sender, provider, oauth_response):
    app.logger.debug('Social Login Failed via %s; '
                     '&oauth_response=%s' % (provider.name, oauth_response))

    # Save the oauth response in the session so we can make the connection
    # later after the user possibly registers
    session['failed_login_connection'] = \
        get_conection_values_from_oauth_response(provider, oauth_response)

    raise SocialLoginError(provider)


@app.errorhandler(SocialLoginError)
def social_login_error(error):
    return redirect(
        url_for('register', provider_id=error.provider.id, login_failed=1))
