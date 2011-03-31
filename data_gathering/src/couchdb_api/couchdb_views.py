'''
Created on Nov 22, 2010

@author: johndoty
'''

import couchdb
import httplib2
import simplejson as json

def create_subreddit_view(subreddit):
    
    design_doc =  """{"_id" : "_design/%s_doc", "views" : 
    {"get_all" : {"map" : 
        "function(doc) {if(doc.post && doc.comment_thread){if(doc.post['subreddit']== '%s'){emit(doc.post['score'], doc._id)}}}"}}}""" % (subreddit, subreddit)
    print design_doc
    
    '''load the document into server'''
    domain = "http://127.0.0.1:5984/reddit_test/_design/%s_doc" % subreddit
    h = httplib2.Http()
    print h.request(domain, "PUT", body=design_doc)
    print domain
    

def get_all_subreddit_posts(subreddit):
    domain = "http://127.0.0.1:5984/reddit_test/_design/%s_doc/_view/get_all" % subreddit
    h = httplib2.Http()
    resp, cont = h.request(domain)
    return cont
    
    
    
def call_view():
    domain = "http://127.0.0.1:5984/testing_views_fruit/_design/example/_view/foo"
    h = httplib2.Http()
    resp, cont = h.request(domain)
    return cont
    
    
    
if __name__ == "__main__":
    create_subreddit_view("atheism")
    print get_all_subreddit_posts("atheism")
    
    