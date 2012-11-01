# Getting Started with Flask and Templates

## Sample code

Download from [Github](https://github.com/johnschimmel/ITP-DWD-Week4-Templates).
See demo [http://rentspiritanimals.herokuapp.com/](http://rentspiritanimals.herokuapp.com/).

## Quick Start

* Download code.
* Open code directory in Terminal console.
* Create Virtualenv (only needs to be run once).

		virtualenv venv

* Initial PIP requirements install / Or when you need to update Python modules after modifying requirements.txt

		. runpip

	The **runpip** file is a helper file and has the following commands

		. venv/bin/activate
		pip install -r requirements.txt

* Start the Server & Activate the Virtualenv if not already active.

		. start

	The **start** file has the following commands

		. venv/bin/activate
		foreman start

* If successful you can navigate to <a href='http://localhost:5000'>http://localhost:5000</a>.


# Templates

Templates keep your code separated from your code and vice versa. Using templates allows you to focus on the code, logic and data then pass the needed data to an HTML template.

People often call this MVC, of Model-View-Controller, where data structures (M), templates (V) and code (C) are separated into different files and directories.

Our templates are located in the /templates directory. These can be organized in directories if needed. The templates are regular HTML files

Using a template library, we can inject data into HTML with the template library specific syntax.

Flask comes ready with Jinja2 for templates. Jinja2 is easy to use and learn, simple syntax. To use templates we'll include this line at the top of **app.py**,

	import render_template

## Template example

A basic HTML template with a single variable.

**index.html**

	<html>
		<title>My first template</title>
		<body>
			<h1>{{ message }}</h1>
		</body>
	</html>

A Flask route, passing a variable into a template

	@app.route('/')
	def mainpage():
		message = 'Hello World'
		return render_template('index.html', message=message)


## Template multiple variables example

**index.html**

	<html>
		<title>My first template</title>
		<body>
			<h1>{{ message }}</h1>
			<p>{{ a_sentence }}</p>
		</body>
	</html>

The Flask route

	@app.route('/')
	def mainpage():
		
		templateData = {
			'message' : 'Hello World',
			'a_sentence' : 'A year passed: winter changed into spring, spring changed into summer, summer changed back into winter, and winter gave spring and summer a miss and went straight on into autumn... until one day..'
		}

		return render_template('index.html', **templateData)

The ** operator in Python will convert a dictionary into a keyword list. The ** operator does the equilivent of this,
	
	return render_template('index.html', message = 'Hello World', a_sentence = 'A year passed....')

## Jinja2 basic

You can see all of Jinja2's reference guide here, [http://jinja.pocoo.org/docs/templates/](http://jinja.pocoo.org/docs/templates/)

## Displaying a variable

	{{ foo }}  <!-- string or int -->
	{{ foo['bar'] }} <!-- bar from dictionary -->
	{{ foo.bar }}  <!-- bar from object -->

## Loops in

	{% for name in names %}
	<li>{{ name }}</li>
	{% endfor %}

## If/Elif/Else in Jinja2

	{% if price == "1.00" %}
	That's cheap!

	{% elif price == "50.00" %}
	Eh, okay, here's $50

	{% else %}
	I'll pay anything.

	{% endif %}


## Static files in Flask apps

You can put your CSS, images, JavaScript and other static files inside **/static**. This directory is known to Flask as the static directory and files inside can be referenced directly. For example a file css/styles.css can be referenced

	/static/css/styles.css

Or an image, if it exists

	/static/img/dog.jpg

The static file directory can also be referenced inside your templates with a function

	{{ url_for('static', filename='css/styles.css') }}
	{{ url_for('static', filename='img/dog.jpg') }}

