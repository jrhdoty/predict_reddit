'''
Created on Nov 17, 2010

@author: johndoty
'''
import Tree_Analysis_Functions as Tree
import couchdb
import couchdb_functions as c_f
import Tree_Analysis_Functions


'''/////////////////////////////////
///
///    CREATE COMMENT TIME SERIES
///
/////////////////////////////////'''
def create_comment_time_frame(node_list):
    '''
    takes structure of nested comment threads
    and returns an array of the comments
    sorted by time earliest to latest
    '''
    
    '''get 1D array of all comments'''
    thread_array = []
    for node in node_list:
        thread_array.extend(rec_create_comment_time_frame(node))
    
    print thread_array
    '''ensure that every element in array has a UTC field'''
    for node in thread_array:
        if not has_utc(node):
            thread_array.remove(node)
    
    '''sort the array based upon comment UTC'''
    thread_array = sorted(thread_array, key=utc_key_func)
    print ("PRINTING THREAD ARRAY FROM FUNC")
    print (thread_array)
    return thread_array
        
        
def rec_create_comment_time_frame(node):
    thread_array = [node]
    children = Tree.get_children(node)
    if children == None or children == "" or children == []:
        return thread_array
    
    for child in children:
        thread_array.extend(rec_create_comment_time_frame(child))
    
    return thread_array 
    
def has_utc(node):
    if 'created_utc' in node:
        return True
    return False

def utc_key_func(node):
    return node['created_utc']


'''/////////////////////////////////
///
///    REBUILD THREAD FROM TIME SERIES
///
/////////////////////////////////'''
def rebuild_tree_from_time_series(tree, comment):
    #this ensures that when a comment is added to the tree its children are not added at the same time
    if comment['replies']:
        comment['replies'] = []
    
    if 'parent_id' not in comment:
        return False
    
    parent = comment['parent_id']
    
    '''if parent is the post then insert at level one'''
    if parent[0:2] == 't3':
        tree.append(comment)
    else:
        for c in tree:
            if rec_rebuild_tree(c, comment, parent):
                return True
    return False


def rec_rebuild_tree(branch, comment, parent):
    '''check to see if root of branch is parent'''
    if 'name' in branch:
        if branch['name'] == parent:
            branch['replies'].append(comment)
            return True
    
    '''check to see if root has children, 
    if so then make recursive call on them'''       
    if 'replies' in branch:
        if branch['replies'] == "" or branch['replies'] == []:
            return False
        for child in branch['replies']:
            if rec_rebuild_tree(child, comment, parent):
                return True
            
    return False

'''////////////////////////////////////////
///
///    GET TIME SERIES DATA FROM DATABASE
///
////////////////////////////////////////'''

def get_time_series_data(dbname, viewname):
    #call the time_series view in couchdb and return the data
    server = couchdb.Server()
    db = server[dbname]
    # URI for view is /database/_design/designdocname/_view/viewname
    data = []
    data.extend(db.view(viewname))
    return data


'''////////////////////////////////////////
///
///    ADD NEW TIME MARKED PROPERTIES
///
////////////////////////////////////////'''
def add_new_time_marked_data(data, func, propertyName):
    '''
    takes in time series and comment data and a function.  
    The function is called at each time point that the score data of the post was monitored
    it is then evaluated and that data is added to the dictionary that describes the state of the post
    at that time point under the name "propertyName"
    format of data is {[time_series, comment_tree][...]}
    '''
    print data
    for post_data in data:
        value = post_data['value']
        
        time_series_data = value[0]
        time_series = time_series_data['time_series']
        comment_tree = value[1]
        time_sorted_comments = create_comment_time_frame(comment_tree)
        tree = []
        for data_point in time_series:
            utc = data_point['utc']
            #rebuild the comment tree up to this time
            while len(time_sorted_comments) > 0 and time_sorted_comments[0]['created_utc'] < utc:
                rebuild_tree_from_time_series(tree, time_sorted_comments[0])
                time_sorted_comments = time_sorted_comments[1:]
            #run the passed function on comment tree
            property_value = func(tree)
            #add the data into the time series dict for this data point
            data_point[propertyName] = property_value
    return

'''////////////////////////////////////////
///
///    UPDATE_DOC
///
////////////////////////////////////////'''
                
if __name__ == '__main__':
    
    '''
    data = get_time_series_data("monitor_reddit_view_tester", "blah/time_series_view2")
    add_new_time_marked_data(data, Tree_Analysis_Functions.total_nodes_in_comments, "total_nodes_in_comments")
    print "AFTER ADDING PROPERTY"
    for item in data:
        print "VALUE IS:"
        print item['value']
    '''
   
   
    
    


