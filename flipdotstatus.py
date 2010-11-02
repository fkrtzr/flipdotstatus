from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import images
import cgi

class Status(db.Model):
    status = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)


class Ping(webapp.RequestHandler):
    def get(self):
	status = Status()
	try:
		url = "http://www.google.de/"
		result = urlfetch.fetch(url)

	
		if result.status_code == 200:
 			status.status = True
		
				
		else:
 			status.status = False
	except:
		status.status = False
		
	
	status.put()
	self.response.out.write(str(status.status))

class StatusView(webapp.RequestHandler):
	def get(self):
		statuses = db.GqlQuery("SELECT * FROM Status ORDER BY date DESC LIMIT 1")
		for status in statuses:
			if status.status:
				
				self.redirect('/img/gruen.jpg')
        		
			else:
				self.redirect('/img/rot.jpg')
        		
		

application = webapp.WSGIApplication(
                                     	[('/ping', Ping),
					('/status', StatusView)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
