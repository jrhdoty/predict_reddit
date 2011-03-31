'''
Created on Dec 15, 2010

@author: johndoty
'''
import math
import comment_thread_time_series_functions as time_series_functions

def comment_length(comment):
    '''takes a string as input
    outputs the number of words in the string'''
    return len(comment.split())
    
def sample_dist(comment_list):
    sample_dist = {}
    size = len(comment_list)
    for comment in comment_list:
        length = comment_length(comment)
        if str(length) in sample_dist:
            sample_dist[str(length)] += 1
        else:
            sample_dist[str(length)] = 1
    return sample_dist, size

def mean_variance(dist):
    num = 0.0
    total_length = 0
    for key, val in dist.items():
        k = int(key)
        num += val
        total_length += val*k
    if num == 0:
        return 0, 0, 0
    else:
        mean = float(total_length)/num
    
    var = 0.0
    for key, val in dist.items():
        k = float(key)
        v = float(val)
        var += (val/num) * ((k - mean)**2)
    
    std_dev = math.sqrt(var)
    return mean, var, std_dev
    
'''////////////////////////////////////////
///
///    GET COMMENT LENGTH DATA FROM THREAD
///
////////////////////////////////////////'''
def thread_comment_length_data(node_list):
    #flatten node_list
    thread_array = time_series_functions.create_comment_time_frame(node_list)
    comment_list = []
    for comment in thread_array:
        comment_list.append(comment['body'])
    dist, size = sample_dist(comment_list)
    mean, var, std = mean_variance(dist)
    return [mean, var, std]

    
if __name__=="__main__":
    s1 = "Here are a collection of random strings"
    s2 = "hello you"
    s3 = "to be or not to be that is the question"
    s4 = "hello world"
    l = [s1, s2, s3, s4]
    
    print (comment_length(s1))
    d, size = sample_dist(l)
    print "dist and size for random strings:"
    print d
    print size
    mean, var, std = mean_variance(d)
    print "mean = %s and var = %s, std_dev=%s" % (mean, var, std)
    
    
    
    
    