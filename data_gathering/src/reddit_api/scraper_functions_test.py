'''
Created on Jan 20, 2011

@author: johndoty
'''

import scraper_functions as s_f
import unittest

class test_parse_post_data(unittest.TestCase):
    input = {"kind": "Listing", "data": {"modhash": "", "children": [{"kind": "t3", "data": {"domain": "imgur.com", "media_embed": {}, "levenshtein": None, "subreddit": "pics", "selftext_html": None, "selftext": "", "likes": None, "saved": False, "id": "f5x76", "clicked": False, "author": "repseki", "media": None, "score": 1433, "over_18": False, "hidden": False, "thumbnail": "http://thumbs.reddit.com/t3_f5x76.png", "subreddit_id": "t5_2qh0u", "downs": 3976, "is_self": False, "permalink": "/r/pics/comments/f5x76/my_girlfriend_and_i_saved_a_red_shouldered_hawk/", "name": "t3_f5x76", "created": 1295571002.0, "url": "http://imgur.com/KS94y.jpg", "title": "My girlfriend and I saved a Red Shouldered Hawk that was on the side of the road yesterday :D", "created_utc": 1295545802.0, "num_comments": 985, "ups": 5409}}], "after": None, "before": None}}
    
    def test_single_entry(self):
        attrList1 = ['domain', "subreddit"]
        attrList2 = ['score', 'ups', 'downs']
        ret1 = s_f.parse_post_data(self.input, attrList1)
        ret2 = s_f.parse_post_data(self.input, attrList2)
        
        id = 't3_f5x76'
        #assertions for first case
        self.assertTrue(id in ret1)
        val = ret1[id]
        self.assertEqual(val['domain'], "imgur.com")
        self.assertEqual(val['subreddit'], "pics")
        
        
        #assertions for second case
        self.assertTrue(id in ret1)
        val = ret2[id]
        self.assertEqual(val['score'], 1433 )
        self.assertEqual(val['ups'], 5409)
        self.assertEqual(val['downs'], 3976)
        
        
if __name__ == "__main__":
    unittest.main()
        
        
        
        
        