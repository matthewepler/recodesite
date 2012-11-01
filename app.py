import os, datetime

from flask import Flask, request 
from flask import render_template

app = Flask(__name__)   



#------------------------------------- MAIN PAGE >>>
@app.route("/")
def index():
	
	return render_template("index.html")





#------------------------------------- 404 HANDLER >>>

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


#------------------------------------- SERVER START-UP >>>
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	