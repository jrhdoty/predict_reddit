'''
Created on Nov 9, 2010

@author:  johndoty
'''
import httplib2
import urllib
import couchdb
import simplejson as json
import time
import couchdb_functions as db

HEADERS = {#'Accept-Charset': 'utf-8',
           #'Accept-Encoding':'gzip',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'User-Agent':'httplib2'
          }

DOMAIN = "http://www.reddit.com/"
SUFFIX = ".json"

'''/////////////////////////////////
///
///    GET JSON DATA FROM PAGE
///
/////////////////////////////////'''
def get_JSON_object_from_page(page_name, data=None, sleep = 1):
    '''param: URL, querry parameters, time in secs to wait before performing querry
    returns a python object decoding of the JSON object fetched from URL''' 
    if sleep == 1:
        time.sleep(2)   #so bot doesn't get in trouble
    print "Page Name is : %s" %page_name
    print data
    h = httplib2.Http()
    if data == None:
        try:
            resp, content = h.request(page_name, 'GET', headers=HEADERS)
        except httplib2.HttpLib2Error:
            content = None
    else:
        data = urllib.urlencode(data)
        try:
            resp, content = h.request(page_name,'GET', body=data, headers=HEADERS,)
        except httplib2.HttpLib2Error:
            content = None
    
    try:
        content = json.loads(content)
    except json.decoder.JSONDecodeError:
        print ("encountered JSONDecodeError in 'get_JSON_object_from_page'")
        print content
        content = None
    except TypeError:
        print ("encountered TypeError")
         
    
    '''return the JSON object if successful, return None otherwise'''
    return content
    
'''/////////////////////////////////
///
///    GET LIST OF POST ID'S
///
/////////////////////////////////'''
def get_post_id_list(num_pages, subreddit = "", dir = "", paramType ="", param = ""):
    '''
    gets all of the object ids from posts on the first
    num_pages of reddit.com/r/subreddit
    '''
    count = 0
    last_id = ""
    
    '''generate the correct url to begin search '''
    if subreddit != "":
        page = DOMAIN + "r/" + subreddit + '/'
    else:
        page = DOMAIN
        
    if dir != "":
        page = page + dir + '/' + SUFFIX
    else:
        page = page + SUFFIX
    
    '''scrape the front page '''
    body = ""
    data = {}
    if paramType != "" and param != "":
        data[paramType] = param
        body = '?'+urllib.urlencode(data)
    obj = get_JSON_object_from_page(page+body)
    if obj != None:  
        id_list = get_ids(obj)
    else:
        id_list = [""]

    '''use params to continue getting data from subsequent pages up to num_page'''
    num_pages = num_pages-1
    cur = 25
    last_id = id_list[-1]
    data['after']=last_id
    data['count']=cur
     
    while (num_pages > 0):
        body = '?' + urllib.urlencode(data)
        next_page = page + body
        obj = get_JSON_object_from_page(next_page)
        if obj != None:
            id_list += get_ids(obj)
        num_pages = num_pages-1
        data['after'] = id_list[-1]
        data['count'] = data['count'] + 25 
        
    return id_list

'''///////////////////////////////////////
///
///    TAKES LIST OF POST ID'S AND 
///    RETURNS JSON INFO ON ALL OF THEM 
///
///////////////////////////////////////'''
def get_multiple_post_info(id_list):
    page = "http://www.reddit.com/by_id/"
    suf = ".json"
    id_string = ",".join(id_list)
    url = page + id_string + suf
    data = get_JSON_object_from_page(url, data=None)
    return data



'''///////////////////////////////////////
///
///    TAKES POST JSON AND RETURNS ITS ID
///
///////////////////////////////////////'''
def get_ids(obj):
    '''
    returns a list of post id's from a listing of posts
    '''
    id_list = []
    children = obj['data']['children']
    for child in children:
        id_list.append(child['data']['name'])
        
    try:
        f = open("/Users/johndoty/Documents/workspace/Data_Aggregation/src/post_ids", 'a')
        for id in id_list:
            f.write(" " + id)
        f.close()
    except IOError:
        print ("IOError")
        pass
    
    return id_list

'''///////////////////////////////////////
///
///    TAKES POST JSON AND RETURNS ITS TITLE
///
///////////////////////////////////////'''
def get_titles(obj):
    '''
    returns a list of post titles from a listing of posts
    '''
    title_list = []
    children = obj['data']['children']
    for child in children:
        title_list.append(child['data']['title'])
    return title_list

'''///////////////////////////////////////////////////////////////
///
///    TAKE LIST OF ID'S AND RETURN POST/COMMENT THREADS as JSON
///
///////////////////////////////////////////////////////////////'''
def get_post_and_comments(id_list):
    '''
    returns a list of posts and its comment thread
    '''
    obj_list = []
    schema = "http://www.reddit.com/comments/%s/.json"
    for id in id_list:
        id_suffix = id[3:]
        link = schema % (id_suffix)
        obj = get_JSON_object_from_page(link)
        if obj != None:
            obj_list.append(obj)
    return obj_list


'''///////////////////////////////////////////////////
///
///    CREATE CLEAN JSON MADE UP OF POST AND COMMENT THREAD
///
///////////////////////////////////////////////////'''
def post_comments_into_JSON(obj_list):
    '''takes a list of json objects containing post and comments
    and cleans up the formatting'''
    new_list = []
    for obj in obj_list:
        '''test case'''
        try:
            post = clean_up_post_JSON(obj[0])
            thread = clean_up_comment_thread_JSON(obj[1])
            new_list.append({"post": post, 
                         "comment_thread": thread }) 
        except KeyError:
            print("KeyError")
        
    return new_list

'''///////////////////////////////////////////////////
///
///    FUNCTIONS FOR PROCESSING POST JSON
///
///////////////////////////////////////////////////'''
def clean_up_post_JSON(obj):
    new_obj = obj['data']['children'][0]['data']
    new_obj['kind'] = 't3'
    return new_obj

'''///////////////////////////////////////////////////
///
///    FUNCTIONS FOR PROCESSING COMMENT THREAD JSON
///
///////////////////////////////////////////////////'''
def clean_up_comment_thread_JSON(thread):
    if thread == "":
        #print("reached base case")
        return ""
    response_list = []
    
    '''remove extraneous material'''
    children = thread['data']['children']
    
    for child in children:
        '''format children'''
        child = child['data']
        child['kind'] = 't1'
        
        '''make recursive call on sub-children'''
        if "replies" in child:
            new_replies = clean_up_comment_thread_JSON(child['replies'])
            child['replies'] = new_replies
            response_list.append(child)
    '''return the list of reformatted responses'''
    return response_list

'''///////////////////////////////////////////////////
///
///    FUNCTIONS FOR PROCESSING ID's IN FILES
///
///////////////////////////////////////////////////'''

def get_id_list_from_file(filename):
    '''takes a name of a file that contains ',' demarcated post id's
    returns a list of the ids with no repetitions'''
    try:
        f = open(filename, 'r')
    except IOError:
        print ("IOError")
        return None
        pass
    id_list = f.read()
    id_list = id_list.split(',')
    id_list = list(set(id_list))
    f.close()
    return id_list


def file_JSON_DB(inputFile, statusFile, db_name):
    id_list = get_id_list_from_file(inputFile)
    if id_list == None:
        return False
    f = open(statusFile, 'a')
    for id in id_list:
        post_comments = [id]
        post_comments = get_post_and_comments(post_comments)
        post_comments = post_comments_into_JSON(post_comments)
        db.insert_JSON_objects_DB(db_name, post_comments)
        f.write(id)
    return True

def output_file_dif():
    input_list = get_id_list_from_file("/Users/johndoty/Documents/workspace/Data_Aggregation/src/Scrape_Jobs/new_post_names")
    f_status = open("/Users/johndoty/Documents/workspace/Data_Aggregation/src/Scrape_Jobs/new_post_names_input_status", 'a')
    str = f_status.read()
    status_list = str.split("t3")
    status = []
    for item in status_list:
        status.append("t3" + item)
    status = status[1:]
    status = set(status)
    input = set(input_list)
    dif = list(input.difference(status))
    dif = dif[1:]
    dif = [item + ',' for item in dif]
    f_new_input = open("/Users/johndoty/Documents/workspace/Data_Aggregation/src/Scrape_Jobs/new_post_names_input", "a")
    f_new_input.writelines(dif)
   
   
'''///////////////////////////////////////////////////
///
///    FUNCTIONS FOR PARSING RAW REDDIT API DATA
///
///////////////////////////////////////////////////'''
   
def parse_post_data(data, attributes):
    '''takes the data passed from get_multiple_post_info
    and a list of attributes to gather data for
    and parses out attribute values for each post, 
    time stamps each entry
    creates a dictionary of dictionaries that contain the values '''
    nextTimeSeries = {}
    try: 
        post_list = data['data']['children']
    except KeyError:
        print "No Data to Parse"
        return
    
    for post in post_list:
        post_data = post['data']
        nextID = post_data['name']
        nextData = {}
        nextData['utc'] = time.time()
        for attribute in attributes:
            try:
                nextData[attribute] = post_data[attribute]
            except KeyError:
                print "Error the key %s does not exist as an attribute" %attribute
        nextTimeSeries[nextID] = nextData
    return nextTimeSeries   
   

def process_time_series_data(filename):
    '''takes as input the filename of the timeseries info
    creates a list of all id's its gathered, gets post info for each
    attaches the time series to each posts json
    returns as a list of posts and associated info'''
    try:
        f = open(filename, 'r')
    except IOError:
        print ("IOError")
        return None
    time_series = json.load(f)
    print "Num of entries in series: %d" % len(time_series.keys())
    output = []
    for key, value in time_series.items():
        data = get_post_and_comments([key])
        data = post_comments_into_JSON(data)
        data = data[0]
        #get the duration that the post was monitored (seconds)
        #and the number of data points
        start = value[0]['utc']
        end = value[-1]['utc']
        duration = end-start
        time_series_data = {"duration": duration, "data_points": len(value), "time_series": value}
        data["time_series"] = time_series_data
        output.append(data)
    return output
        

if __name__ == '__main__':
    #if main is called a small example will run
    print "PRINTING JSON REPRESENATION OF CURRENT REDDIT FRONT PAGE\n"
    data = get_JSON_object_from_page(DOMAIN+SUFFIX, data=None, sleep = 1)
    data = data['data']['children']
    for post in data:
        print post
    
    
    
    
    
