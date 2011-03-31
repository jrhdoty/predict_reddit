'''
Created on Mar 1, 2011

@author: johndoty
'''
import couchdb_functions as c_f
import unittest

class couchdb_test_cases(unittest.TestCase):
    time_series = {
       "duration": 13517.625690937042,
       "data_points": 30,
       "testing input": 10,
       "time_series": [
           {
               "utc": 1296781477,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296781542.485595,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296781908.419636,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296782267.473303,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296782644.405428,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296783020.418586,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296783409.331248,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296783798.552518,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296784195.208782,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296784611.74638,
               "downs": 0,
               "score": 1,
               "ups": 1
           },
           {
               "utc": 1296785059.706235,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296785478.171286,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296785915.255121,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296786369.705278,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296786835.712804,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296787300.825724,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296787779.441198,
               "downs": 0,
               "score": 2,
               "ups": 2
           },
           {
               "utc": 1296788272.863627,
               "downs": 0,
               "score": 3,
               "ups": 3
           },
           {
               "utc": 1296788775.10594,
               "downs": 0,
               "score": 4,
               "ups": 4
           },
           {
               "utc": 1296789273.705546,
               "downs": 0,
               "score": 4,
               "ups": 4
           },
           {
               "utc": 1296789787.951972,
               "downs": 1,
               "score": 5,
               "ups": 6
           },
           {
               "utc": 1296790305.231178,
               "downs": 1,
               "score": 5,
               "ups": 6
           },
           {
               "utc": 1296790853.90882,
               "downs": 1,
               "score": 5,
               "ups": 6
           },
           {
               "utc": 1296791405.04134,
               "downs": 0,
               "score": 6,
               "ups": 6
           },
           {
               "utc": 1296792004.348497,
               "downs": 0,
               "score": 7,
               "ups": 7
           },
           {
               "utc": 1296792574.203342,
               "downs": 1,
               "score": 6,
               "ups": 7
           },
           {
               "utc": 1296793166.645355,
               "downs": 1,
               "score": 7,
               "ups": 8
           },
           {
               "utc": 1296793772.100052,
               "downs": 0,
               "score": 8,
               "ups": 8
           },
           {
               "utc": 1296794371.520541,
               "downs": 0,
               "score": 8,
               "ups": 8
           },
           {
               "utc": 1296794994.625691,
               "downs": 1,
               "score": 8,
               "ups": 9
           }
       ]}
       
    def test_update_document(self):
        c_f.update_document("monitor_reddit_view_tester", "d24317293903faa9391d79f35e700d70", c_f.update_doc_time_series, self.time_series)

if __name__ == '__main__':
    unittest.main()
        