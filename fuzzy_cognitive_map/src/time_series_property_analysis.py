'''
Created on Mar 1, 2011

@author: johndoty
'''

import couchdb_functions
import comment_thread_time_series_functions as time_series_functions
import Tree_Analysis_Functions
import comment_length_functions

def first_analysis():
    #gather all of the time_series data from entires in database
    data = time_series_functions.get_time_series_data("processed_time_series", "time_series/time_series_view")
    # add new time marked data for each desired property
    time_series_functions.add_new_time_marked_data(data, Tree_Analysis_Functions.total_nodes_in_comments, "total_nodes_in_comments")
    time_series_functions.add_new_time_marked_data(data, Tree_Analysis_Functions.average_max_depth, "average_max_depth")
    time_series_functions.add_new_time_marked_data(data, Tree_Analysis_Functions.max_depth_tree, "max_depth_tree")
    time_series_functions.add_new_time_marked_data(data, Tree_Analysis_Functions.average_branching_factor_of_branches, "average_branching_factor")
    time_series_functions.add_new_time_marked_data(data, Tree_Analysis_Functions.ratio_of_stubs, "ratio_of_stubs")
    time_series_functions.add_new_time_marked_data(data, comment_length_functions.thread_comment_length_data, "thread_comment_length_data")
    
    #update database with altered documents
    for post in data:
        key = post['id']
        time_series = post['value'][0]
        couchdb_functions.update_document("processed_time_series", key, 
                                          couchdb_functions.update_doc_time_series, time_series)
    return

if __name__ == '__main__':
    #first_analysis()
    
    #testing parametrized view
    server = couchdb.Server()
    db = server["processed_time_series"]
    # URI for view is /database/_design/designdocname/_view/viewname
    result = db.view("time_series/time_series_view")
    print data[0]
    '''
    data = [28626:28628]
        for item in data:
            print item['value']['post']
            '''
    
    

        
    
    