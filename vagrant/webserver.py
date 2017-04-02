from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi #to recieve message via fields

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):    #handles all get requests web server recieves
        try:

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(ids=restaurantIDPath).one()                

                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s</h1>" %myRestaurantQuery.name

                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" %restaurantIDPath
                    output += "<input type='submit' value='DELETE'>"
                    output += "</form>"
                    output +="</body></html>"
                    self.wfile.write(output)
                    print output
                    return 

            
            if self.path.endswith("/edit"):
                    
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(ids=restaurantIDPath).one() #returns list
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h2>%s</h2>" %myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" %restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder='%s' >" %myRestaurantQuery.name
                    output += "<input type='submit' value='RENAME'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output) #to write output back to clients
                    print output
                    return    

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                items = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here </a>"
                output += "</br></br>"

                for item in items:
                    output += item.name
                    output += "</br>"
                    output += "<a href='restaurants/%s/edit'>Edit</a>" %item.ids
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" %item.ids
                    output += "</br></br>"
               
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
                output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></html></body>"
                self.wfile.write(output)
                return


        except IOError:    # exception handling
            self.send_error(404, 'File Not Found: %s' % self.path)



    def do_POST(self):
        try:

            if self.path.endswith("/delete"):


                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(ids=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants') #redirects to homepage
                    self.end_headers()
                


            
            if self.path.endswith("/edit"): #self.path returns a string
                ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(ids=restaurantIDPath).one()
                    if myRestaurantQuery != []:
                            
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants') #redirect to restaurants homepage
                        self.end_headers()
    




            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName') #all the things submitted by you in form

                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants') #redirect to restaurants homepage
                    self.end_headers()
                

        except:
            pass

def main():
    try:
        port = 8080    #instance of httpseverclass based on tcp server class
        server = HTTPServer(('',port),webServerHandler)    # webserverHandler is handler class, host is left as an empty string
        print "Web server running on port %s" % port
        server.serve_forever()    #to make server constantly listen til keyboardinterrupt

    except KeyboardInterrupt:    #built in exception in python triggered when hold ctrl+C
        print "^C entered, stopping web server ......"
        server.socket.close()


if __name__ == '__main__':    # to make main entry code
    main()
