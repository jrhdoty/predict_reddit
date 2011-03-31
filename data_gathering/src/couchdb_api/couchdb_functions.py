'''
Created on Dec 16, 2010

@author: johndoty
'''

import couchdb
import httplib2
import simplejson as json
import random


'''///////////////////////////////////////////////////
///
///    COUCH DATABASE FUNCTIONS
///
///////////////////////////////////////////////////'''

def insert_JSON_objects_DB(db_name, obj_list):
    couch = couchdb.Server()
    db = couch[db_name]
    for obj in obj_list:
        db.save(obj)
    
    
def clearDatabase(dbName):
    couch = couchdb.Server()
    db = couch[dbName]
    doclist = []
    for doc in db:
        doclist.append(doc)
    
    objList = []
    for item in doclist:
        objList.append(db[item])
    
    for item in objList:
        db.delete(item)

'''///////////////////////////////////////////////////
///
///    VIEW FUNCTIONS
///
///////////////////////////////////////////////////'''

def create_design_doc(dbname, docname):
    '''
    creates a design document in the given database with the given name if the database exists and
    there does not already exist a doc with the same name
    '''
    #checks to see that the database exists and that the doc does not
    #returns true if successful, returns false if failure for some reason
    couch = couchdb.Server()
    try:
        db = couch[dbname]
    except NameError:
        print "Database %s doesn't exist" % dbname
        return False
    doc_id = "_design/%s" % docname
    
    if doc_id in db:
        print "The document %s already exists" % docname
        return False
    id = "_design/%s" % docname
    design_doc = {"_id": id, "views" : {} }
    db.save(design_doc)
    return True


def create_view(dbname, docname, viewname, view):
    '''
    creates a view in the given database and design doc if they exist
    with the name 'viewname' and function 'view'
    '''
    #check to see that database exists
    couch = couchdb.Server()
    try:
        db = couch[dbname]
    except NameError:
        print "Database %s doesn't exist" % dbname
        return False
    
    #see if doc already exists
    #if it is then get it
    #otherwise create from scratch
    doc_id = "_design/%s" % docname
    if doc_id in db:
        doc = db[doc_id]
        print doc
        #check to see that there isn't a view of the same name already
        if viewname in doc["views"]:
            print "View %s already exists in the design document %s" % (viewname, docname)
            return False
        #if it isn't then insert view and place doc back in db
        doc["views"][viewname] = view
        db.save(doc)
    else:
        #otherwise create the doc from scratch and put in the db
        design_doc = {"_id" : doc_id, "views" : {viewname: view}}
        db.save(design_doc)
    return True

def remove_view(dbname, docname, viewname):
    '''
    removes the specified view from a document
    the use case is if a view with bad coding was placed into a db 
    or if one wishes to alter the way in which a view with a given name was coded
    but doens't want to insert an entirely new view
    '''
    update_document(dbname, docname, update_design_doc_remove_view, viewname)
    

def call_view():
    '''sanity check function'''
    domain = "http://127.0.0.1:5984/testing_views_fruit/_design/example/_view/foo"
    h = httplib2.Http()
    resp, cont = h.request(domain)
    return cont

'''////////////////////////////////////////
///
///    UPDATE_DOC
///
////////////////////////////////////////'''
def update_document(db, doc_id, func, args):
    '''
    takes in a database name, document id, an altering function and its parameters as parameters
    gets the entire doc from database, runs the function to update it
    then puts the updated version back into the database
    '''
    server = couchdb.Server()
    db = server[db]
    doc = db[doc_id]
    func(doc, args)
    db[doc_id] = doc
    
'''////////////////////////////////////////
///
///    UPDATE_DOC_FUNCTIONS
///
////////////////////////////////////////'''
def update_doc_time_series(doc, time_series):
    doc['time_series'] = time_series
    
def update_design_doc_remove_view(doc, viewname):
    del doc['views'][viewname]
    


if __name__=="__main__":
    
    
    '''
    #create_view(dbname, docname, viewname, view):
    view = {"map": "function(doc){if(doc.post['subreddit'] && doc.post['title']){emit([doc.post['subreddit'], doc.post['score']], doc.post['title'])}}"}
    simpleview1 = {"map": "function(doc){ emit(doc._id, doc._rev)}"}
    time_series_view = {"map": "function(doc){if(doc.time_series && doc.comment_thread){emit(doc._id, [doc.time_series, doc.comment_thread])}}"}
    duration_view = {"map": "function(doc){if(doc.time_series && doc.post){emit(doc.time_series['duration'], [doc.post, doc.time_series])}}"}
    subreddit_and_score = {"map": "function(doc){if(doc.time_series && doc.post){emit([doc.post['subreddit'], doc.post['score']], doc.id)}}"}
    score = {"map": "function(doc){if(doc.time_series && doc.post){emit(doc.post['score'], doc.post['subreddit'])}}"}
    #create_view(dbname, docname, viewname, view)
    create_view("model_training", "data_lookup", "score", score)
    
    #remove_view(dbname, docname, viewname)
    #remove_view("model_training", "_design/data_lookup", "score")
    '''
    
    
    
    
    
    
    
    
    
    
    
    