from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api import urlfetch
from google.appengine.api import images
import cgi
import datetime

class Status(db.Model):
    status = db.BooleanProperty()
    date = db.DateTimeProperty(auto_now_add=True)

# cron job target for url-availability-testing
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

# return status jpeg-pixel
class StatusView(webapp.RequestHandler):
	def get(self):
		statuses = db.GqlQuery("SELECT * FROM Status ORDER BY date DESC LIMIT 1")
		for status in statuses:
			if status.status:
				
				self.redirect('/img/gruen.jpg')
        		
			else:
				self.redirect('/img/rot.jpg')

#evaluate overall         		
class OverallOpeningTime(webapp.RequestHandler):
	def get(self):
		
		statuses = Status.all()
		opened = datetime.timedelta() 
		closed = datetime.timedelta() 
		count = statuses.count()
		statuses = statuses.run()		
		while count >= 2:
			first = statuses.next()
			second = statuses.next()
			if first.status and second.status:
				opened += second.date - first.date
			elif (not first.status) and (not second.status):
				closed += second.date - first.date
			count = count - 2
		self.redirect("http://chart.apis.google.com/chart?cht=p3&chd=t:"+str(opened.seconds)+","+str(closed.seconds)+"&chs=350x100&chl=Open|Closed&chdl="+str(opened.seconds/60)+"%20hours|"+str(closed.seconds/60)+"%20hours")

			
			
				

application = webapp.WSGIApplication(
                                     	[('/ping', Ping),
					('/status', StatusView),
					('/overall', OverallOpeningTime)],
							debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
