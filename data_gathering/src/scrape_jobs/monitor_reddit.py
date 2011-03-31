'''
Created on Dec 26, 2010

@author: johndoty
'''

import scraper_functions as s_f
import couchdb_functions as c_f
import simplejson as json
import time
import heapq

def get_new_posts(timeSeries, updateQueue):
    '''
    scrape new page
    check post id's against those already in timeSeries (dictionary)
    input new posts to timeSeries and updateQueue (PriorityQueue)
    '''
    IDList = s_f.get_post_id_list(1,"", "new", "sort", "new")
    NewIDs = []
    if IDList == None:
        return None
    for ID in IDList:
        if ID not in timeSeries.keys():
            NewIDs.append(ID)
    if len(NewIDs) != 0:
        new_data  = s_f.get_multiple_post_info(NewIDs)
        if new_data == None:
            return None
        parsed_data = s_f.parse_post_data(new_data, ['created_utc'])
        for ID in NewIDs:  
            utc = parsed_data[ID]['created_utc']
            timeSeries[ID] = [{"utc": utc, "ups":1, "downs":0, "score":1}]
            heapq.heappush(updateQueue, (0, ID))

def update_time_series(stopTime, updateFrequency, timeSeries, updateQueue):
    '''
    if queue is empty, then put all posts into it ordered by the last time their score was checked
    if it is too soon to refresh the score of the next post from the queue wait, else get 25 posts or 
    make a query to reddit to get JSON data
    gather relevant info: utc, ups, downs, score
    update timeSeries entry with new score info
    iterate
    '''
    IDlist = []
    count = 0
    page = "http://www.reddit.com/by_id/"
    suf = ".json"
    next = True
    #while not time to stop, query reddit for data related to score/time 
    while time.time() <= stopTime:
        qEntries = len(updateQueue)

        if qEntries <= 0:
            for key, val in timeSeries.items():
                heapq.heappush(updateQueue, (val[-1]['utc'], key))  #the post ID and time of last update
        else:
            time_to_update = time.time() - updateFrequency
            IDlist = []
            while count < 25 and len(updateQueue) > 0:
                next = heapq.heappop(updateQueue)
                if time_to_update < next[0]:
                    heapq.heappush(updateQueue, next)
                    break
                IDlist.append(next[1])
                count += 1
        #get raw JSON data
        if count >= 1:
            raw_data = s_f.get_multiple_post_info(IDlist)     
            #parse the JSON data
                #if reddit or internet failure, note that data was missed for this time period
            if raw_data == None:
                missed_time = time.time()
                parsed_data = {}
                for ID in IDlist:
                    parsed_data[ID] = {'utc': missed_time, 'score': "N/A", 'ups': "N/A", 'downs': "N/A"}
            else:
                attributes = ['score', 'ups', 'downs']
                parsed_data = s_f.parse_post_data(raw_data, attributes)
            #update timeSeries with parsed data
            for key, val in parsed_data.items():
                timeSeries[key].append(val)         
        count = 0
        

def backup_job_progress(python_object, prefix):
    '''takes a python object, attempts to turn it into a JSON object
    outputs to a file with name "prefix_year_month_day_hr_min_sec"
    returns 1 if success, None otherwise
    '''
    timeObj = time.localtime()
    fileName = prefix + "_" + str(timeObj[0]) #year
    fileName += "_" + str(timeObj[1])  #month
    fileName += "_" + str(timeObj[2])  #day
    fileName += "_" + str(timeObj[3])  #hour
    fileName += "_" + str(timeObj[4])  #min
    fileName += "_" + str(timeObj[5])  #sec
    
    #create file
    backupFile = open(fileName, 'a')
    #try to serialize object as JSON
    try:
        json.dump(python_object, backupFile)
    except json.encoder.JSONEncodeError:
        print "Error in backing up job progress"
    
def recover_backup(name):
    '''sanity check function to make sure that
    backup_job_progress is displaying the correct behavior'''
    file = open(name, 'r')
    try: 
        data = json.load(file)
        print data
    except json.decoder.JSONDecodeError:
        print"failed at recovering data"


def monitor_new_posts(updateFrequency, newPostFrequency, backupFrequency, runTime):
    '''monitors the "new" page for new reddit posts, all parameters are considered to be in seconds,
    records the up, down, and total votes for the post every "updateFrequency" seconds
    backups the gathered info as JSON to a text file every backupFrequency seconds        
    the max number of new posts it can gather is a function of the max number of posts'
    data it can gather in "updateFrequency" time
    '''
    jobStartTime = time.time()
    jobFinishTime = jobStartTime + runTime
    #max number of posts that can be gathered in updateFreq time 
    #maxPosts = updateFreq  / 2(sec b/w queries) * 25 posts per query 
    maxPosts = (updateFrequency/2) * 25 
    backupTime = jobStartTime + backupFrequency
    getNewTime = 0
    updateQueue = []
    timeSeries = {}
    queryPostList = []
    
    while time.time() <= jobFinishTime:
        #check if time for backup
        if backupTime <= time.time():
            backup_job_progress(timeSeries, "Monitor_Reddit")
            backupTime = time.time() + backupFrequency
        #check if time for scraping 'new' page
        if getNewTime <= time.time():
            get_new_posts(timeSeries, updateQueue)
            getNewTime = time.time() + newPostFrequency
        # while its not time to scrape new page again
        stopTime = getNewTime
        update_time_series(stopTime, updateFrequency, timeSeries, updateQueue)       
    #when job is finished perform final backup
    backup_job_progress(timeSeries, "Final_Monitor_Reddit")
    

def monitor_new_posts_max

if __name__ == "__main__":
    '''
    testObject = {"test": 1, "testing": 2}
    backup_job_progress(testObject, "TESTING")
    '''
    updateFrequency     = 180
    newPostFrequency    = 30
    backupFrequency     = 900
    runTime             = 28800 
    monitor_new_posts(updateFrequency, newPostFrequency, backupFrequency, runTime)
    
    
    
    