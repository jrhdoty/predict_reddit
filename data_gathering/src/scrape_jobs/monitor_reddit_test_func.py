'''
Created on Jan 3, 2011

@author: johndoty
'''
import scraper_functions as s_f
import couchdb_functions as c_f
import monitor_reddit as m_r
import mox
import time
import heapq
import unittest

class test_get_new_posts_timeSeries(unittest.TestCase):
    timeSeries = {}
    updateQueue = []
    
    def test_timeSeries_valid(self):
        '''test that timeSeries contains 25 new entries whose keys are an ID36 and other values are 0 '''
        m_r.get_new_posts(self.timeSeries, self.updateQueue)
        self.assertEqual(25, len(self.timeSeries))
        for item in self.timeSeries.keys():
            self.assertEqual("t3_", item[:3])
            self.assertEqual(8, len(item))
        
    def test_updateQueue_valid(self):
        '''test that updateQueue contains the 25 new entries and priority is determined by utc'''
        self.timeSeries = {}
        self.updateQueue = []
        m_r.get_new_posts(self.timeSeries, self.updateQueue)
        self.assertEqual(25, len(self.updateQueue))
        

class test_update_time_series(unittest.TestCase):
    timeSeries = {}
    updateQueue = []
    id_list = s_f.get_id_list_from_file("new_post_names_input")
    id_list = id_list[1:]
    updateFrequency = 300  
    
    def test_update_all_queue(self):
        '''test to see that after updating all the posts that are in the queue
        it will wait until time for next update'''
        altered_list = self.id_list[:30]
        self.timeSeries = {}
        self.updateQueue = []
        for ID in altered_list:
            heapq.heappush(self.updateQueue, (0, ID))
            self.timeSeries[ID] = [{"utc":0, "up":0, "down":0, "score":0}]
        stopTime = time.time() + 10
        m_r.update_time_series(stopTime, self.updateFrequency, self.timeSeries, self.updateQueue)
        #check that all items are in timeSeries
        for ID in altered_list:
            self.assertTrue(ID in self.timeSeries.keys())
        testCount = 0
        for key, val in self.timeSeries.items():
            testCount += 1
            self.assertEqual(len(val), 2)   #assert there are two entries for each ID
            
            
        
    def test_partial_update_queue(self):
        '''test to see that handles the case where function only has time to update part of the updateQueue 
        before time to exit'''
        for ID in self.id_list[:200]:
            heapq.heappush(self.updateQueue, (0, ID))
            self.timeSeries[ID] = [{"utc":0, "up":0, "down":0, "score":0}]
        stopTime = time.time() + 5
        m_r.update_time_series(stopTime, self.updateFrequency, self.timeSeries, self.updateQueue)
        updated = False
        unupdated = False
        for key, val in self.timeSeries.items():
            if len(val) == 2:
                updated = True
            if len(val) == 1:
                unupdated = True
        self.assertTrue(updated)
        self.assertTrue(unupdated)
        
    def test_empty_queue(self):
        '''handles case in which the queue is empty'''
        self.updateQueue = []
        m_r.update_time_series(time.time()+5, self.updateFrequency, self.timeSeries, self.updateQueue)
        self.assertEqual(len(self.updateQueue), 0)

'''
class test_parser_func(unittest.TestCase):
        'test that the data parser to get score and utc data works'
        raw_data = {'kind': 'Listing', 'data': {'modhash': '', 'children': [{'kind': 't3', 'data': {'domain': 'destructoid.com', 'media_embed': {}, 'levenshtein': None, 'subreddit': 'gaming', 'selftext_html': None, 'selftext': '', 'likes': None, 'saved': False, 'id': 'emn4e', 'clicked': False, 'author': 'Pudgyhipster', 'media': None, 'score': 4, 'over_18': False, 'hidden': False, 'thumbnail': 'http://thumbs.reddit.com/t3_emn4e.png', 'subreddit_id': 't5_2qh03', 'downs': 1, 'is_self': False, 'permalink': '/r/gaming/comments/emn4e/telltale_games_back_to_the_future_dated_for/', 'name': 't3_emn4e', 'created': 1292475125.0, 'url': 'http://www.destructoid.com/first-episode-of-back-to-the-future-dated-189725.phtml', 'title': "Telltale Game's Back to the Future dated for December 22nd!", 'created_utc': 1292475125.0, 'num_comments': 2, 'ups': 5}}, {'kind': 't3', 'data': {'domain': 'i.imgur.com', 'media_embed': {}, 'levenshtein': None, 'subreddit': 'pics', 'selftext_html': None, 'selftext': '', 'likes': None, 'saved': False, 'id': 'en9a3', 'clicked': False, 'author': 'Mattimos', 'media': None, 'score': 0, 'over_18': False, 'hidden': False, 'thumbnail': 'http://thumbs.reddit.com/t3_en9a3.png', 'subreddit_id': 't5_2qh0u', 'downs': 10, 'is_self': False, 'permalink': '/r/pics/comments/en9a3/im_doing_secret_santa_mine_likes_photography/', 'name': 't3_en9a3', 'created': 1292564381.0, 'url': 'http://i.imgur.com/r4PMV.jpg', 'title': 'I\'m doing secret santa. Mine likes photography, panda bears, her favorite color is "All colors," her favorite candy is Now n\' Laters, and she\'s a jesuit and a bit homophobic. I stuffed a panda bear with Now n\' Laters, colored it rainbow, and took this. I\'m going to include it in the package.', 'created_utc': 1292564381.0, 'num_comments': 5, 'ups': 7}}, {'kind': 't3', 'data': {'domain': 'vimeo.com', 'media_embed': {'content': '&lt;iframe src="http://player.vimeo.com/video/17045021" width="480" height="272" frameborder="0"&gt;&lt;/iframe&gt;', 'width': 480, 'scrolling': False, 'height': 272}, 'levenshtein': None, 'subreddit': 'Music', 'selftext_html': None, 'selftext': '', 'likes': None, 'saved': False, 'id': 'en9a2', 'clicked': False, 'author': 'yell-ow', 'media': {'type': 'vimeo.com', 'oembed': {'provider_url': 'http://vimeo.com/', 'description': 'Official Video of "Undercover Martyn" by Two Door Cinema Club!', 'title': 'Two Door Cinema Club - Undercover Martyn', 'author_name': 'ISMAYA', 'height': 272, 'width': 480, 'html': '&lt;iframe src="http://player.vimeo.com/video/17045021" width="480" height="272" frameborder="0"&gt;&lt;/iframe&gt;', 'thumbnail_width': 200, 'version': '1.0', 'provider_name': 'Vimeo', 'thumbnail_url': 'http://b.vimeocdn.com/ts/105/315/105315377_200.jpg', 'type': 'video', 'thumbnail_height': 150, 'author_url': 'http://vimeo.com/ismaya'}}, 'score': 1, 'over_18': False, 'hidden': False, 'thumbnail': '', 'subreddit_id': 't5_2qh1u', 'downs': 0, 'is_self': False, 'permalink': '/r/Music/comments/en9a2/two_door_cinema_club_undercover_martyn_this/', 'name': 't3_en9a2', 'created': 1292564379.0, 'url': 'http://vimeo.com/17045021', 'title': 'Two Door Cinema Club - Undercover Martyn.  This ginger sounds like he has a soul.', 'created_utc': 1292564379.0, 'num_comments': 0, 'ups': 1}}], 'after': None, 'before': None}}
        def test_parser(self):
            processed_data = m_r.parse_score_utc_data(self.raw_data)
            keys = processed_data.keys()
            self.assertTrue('t3_emn4e' in keys)
            self.assertTrue('t3_en9a3' in keys)
            self.assertTrue('t3_en9a2' in keys)
            self.assertEqual(processed_data['t3_emn4e']['score'], 4 )
            self.assertEqual(processed_data['t3_en9a3']['score'], 0 )
            self.assertEqual(processed_data['t3_en9a2']['score'], 1 )
            
            self.assertEqual(processed_data['t3_emn4e']['down'], 1 )
            self.assertEqual(processed_data['t3_en9a3']['down'], 10 )
            self.assertEqual(processed_data['t3_en9a2']['down'], 0)
            
            self.assertEqual(processed_data['t3_emn4e']['up'], 5 )
            self.assertEqual(processed_data['t3_en9a3']['up'], 7 )
            self.assertEqual(processed_data['t3_en9a2']['up'], 1 )
        
'''        


class test_monitor_reddit(unittest.TestCase):
    updateFrequency     = 15
    newPostFrequency    = 10
    backupFrequency     = 30
    runTime             = 120   
    
def test_short_scrape_job(self):
    m_r.monitor_new_posts(self.updateFrequency, self.newPostFrequency, self.backupFrequency, self.runTime)
    
    
    
    
    


def num_post_test1(num_posts, filename):
    '''
    s_fget_id_list_from_file
    try to get num_posts in single querry
    '''
    id_list = s_f.get_id_list_from_file(filename)
    page = "http://www.reddit.com/by_id/"
    suf = ".json"
    id_list = id_list[:num_posts]
    
    id_string = ",".join(id_list)
    id_string = id_string[1:]
    print id_string
    
    url = page + id_string + suf
    print url
    
    data = s_f.get_JSON_object_from_page(url, data=None, sleep = 0)
    
    new_list = s_f.get_ids(data)
    id_list = id_list[1:]
    print id_list
    print new_list
    
    old_set = set(id_list)
    new_set = set(new_list)
    print "SIZE OF OLD: %d" % len(old_set)
    print "SIZE OF NEW %d"  % len(new_set)
    if old_set == new_set:
        print "THE SETS ARE EQUAL"
    else:
        print "THE SETS ARE UNEQUAL"
        
        
        
if __name__ == '__main__':
    unittest.main()