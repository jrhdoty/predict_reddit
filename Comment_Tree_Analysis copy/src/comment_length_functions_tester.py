'''
Created on Mar 1, 2011

@author: johndoty
'''
import unittest
import comment_length_functions
import comment_thread_time_series_functions as time_series_functions

class test_all_functions(unittest.TestCase):
    data = time_series_functions.get_time_series_data("monitor_reddit_view_tester", "blah/time_series_view2")
    
    def test_thread_comment_length_data(self):
        #get list of comment trees
        for post_data in self.data:
            value = post_data['value']
            comment_tree = value[1]
            length_data = comment_length_functions.thread_comment_length_data(comment_tree)
            print "MEAN: %f \nVar: %f \n Std: %f" % (length_data[0], length_data[1], length_data[2])
            

if __name__ == "__main__":
    unittest.main()