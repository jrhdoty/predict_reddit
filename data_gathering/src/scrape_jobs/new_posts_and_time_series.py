'''
Created on Dec 14, 2010

@author: johndoty
'''
import scraper_functions as s_f
import get_front_page as front_page
import time

def get_new_post_names(time_period):
    '''gathers new post titles for time_period minutes
    inserts the names into a file to be used later'''
    try:
        f = open("/Users/johndoty/Documents/workspace/Data_Aggregation/src/Scrape_Jobs/new_post_names", 'a')
    except IOError:
        print ("IOError")
        pass
    
    current = time.time()
    print current
    finish = current + (60*time_period)
    print finish
    
    while finish >= time.time():
        names = s_f.get_post_id_list(1, dir='new', paramType='sort', param='new')
        names = [name+',' for name in names]
        f.writelines(names)
        time.sleep(45)
    f.close()


def num_names():
    try:
        f = open("/Users/johndoty/Documents/workspace/Data_Aggregation/src/Scrape_Jobs/new_post_names", 'r')
    except IOError:
        print ("IOError")
        pass
    str = f.read()
    f.close()
    l = str.split(',')
    print "Num total entries is: %d" % len(l)
    print "Num unique entries is: %d" % len(remove_duplicates(l))
    
    

    
if __name__=='__main__':
    filename = "/Users/johndoty/Documents/workspace/Data_Aggregation/src/Scrape_Jobs/new_post_names"
    num_names()
    l = [1, 2, 3, 4, 4, 5, 6]
    print l
    l2 = remove_duplicates(l)
    print l
    print l2
    print len(s_f.get_id_list_from_file(filename))
     
    
    
    
    
    
    
    
   