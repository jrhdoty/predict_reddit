'''
Created on Mar 4, 2011

@author: johndoty
'''
import couchdb
import numpy as np
import math
import scipy.stats as stats
from scipy.interpolate import interp1d
import matplotlib.pyplot as mpl

'''////////////////////////////////////////
///
///    Generate Pearson R and P Values
///
////////////////////////////////////////'''
def generate_pearson_values_time_series(time_series_data, properties, property_tuples=None):
    '''
    for every property recorded in time series data
    get its pearson r and p value for every other property
    in the dataset
    format of time_series_data parameters is the return value of duration_view: 
    { {key: id,value: [doc.time_series, doc.comment_thread]}{....}}
    properties is the list of properties that need to be processed to get values
    property_tuples is a list of tuples for which to get r-values if None, then get all combinations
    '''
    
    #determine number of properties
    r_p_values = {}
    property_arrays = {}
    for property in properties:
        property_arrays[property] = []
    #include the nested comment length data
    property_arrays['average_comment_length'] = []
    
    #aggregate all of the data for each property
    for item in time_series_data:
        time_series = item['value'][0]['time_series']
        for data_point in time_series:
            for key in property_arrays.keys():
                if key == 'average_comment_length':
                    property_arrays[key].append(data_point['thread_comment_length_data'][0])
                else:
                    property_arrays[key].append(data_point[key])
                
                
    #create ndarrays with the property arrays
    for key, value in property_arrays.items():
        property_arrays[key] = np.array(value)
    print "Number of total data points is: %d" % len(property_arrays[properties[0]])
    
    #if property_tuples == none then get r-val for all combinations
    properties.append('average_comment_length')
    if property_tuples == None:
        count = 1
        for property1 in properties:
            for property2 in properties[count:]:
                r_p_values[(property1, property2)] = stats.pearsonr(property_arrays[property1], property_arrays[property2])
                
    return r_p_values
        

def distribution_of_score_data(time_series_data, t):
    '''
    return an array of score data for all posts in input
    format of time_series_data parameters is the return value of duration_view: 
    { {key: id, value: [doc.time_series, doc.comment_thread]}{....}}
    the score that is returned is the first score data_point recorded after the
    time input parameter (seconds) + the first recorded utc
    '''
    score_data = []
    for item in time_series_data:
        id = item['key']
        time_series = item['value'][0]['time_series']
        stopTime = time_series[0]['utc'] + t
        data_point = 1
        end = len(time_series)
        while time_series[data_point]['utc'] < stopTime and data_point < end:
            data_point += 1
        #if t is greater than the length of time for which the post was recorded return with error message
        if data_point == end:
            print "Parameter t is an invalid value"
            return None
        score_data.append((time_series[data_point]['score'], id, time_series[data_point]['utc']))
    return score_data
    
    


if __name__ == "__main__":
    print "RUNNING STATISTICAL ANALYSIS MODULE"
    print "GOODBYE"
    '''
    mt = 'model_training'
    mtv = 'data_lookup/time_series'
    #mt = 'monitor_reddit_view_tester'
    #mtv = 'blah/time_series_view2'
    server = couchdb.Server()
    db = server[mt]
    viewname = mtv
    time_series = db.view(viewname)
    
    
    #test distribution of score data
    #distribution_of_score_data(time_series_data, t)
    score_data = distribution_of_score_data(time_series, 7200)
    score_data.sort()
    
    score_list = []
    for item in score_data:
        print item[0].__class__
        score_list.append(item[0])
    print "SOME TESTS TO FIT DATA TO A PROBABILITY DISTRIBUTION"
    score_data_narray = np.array(score_list)
    freq_data = {}
    for score in score_list:
        if score in freq_data.keys():
            freq_data[score] +=1
        else:
            freq_data[score] = 1
            
    #the raw score/frequency data
    scores = []
    frequencies = []
    xy = []
    for score, freq in freq_data.items():
        scores.append(score)
        frequencies.append(freq)
        xy.append((score, freq))
    
    xy.sort()
    print xy
    scores = []
    frequencies = []
    for item in xy:
        scores.append(item[0])
        frequencies.append(item[1])
    #the interpolated score/frequency data
    f = interp1d(scores, frequencies)
    xi = [x*0.1 for x in range(min(scores), max(scores)*10)]
    yi = f(xi)
    
    mpl.ylabel("Score")
    mpl.xlabel("Frequency")
    mpl.plot(scores, frequencies)
    mpl.title("PLOTING THE RAW SCORE DATA")
    mpl.show()
    
    mpl.title("PLOTING THE INTERPOLATED SCORE DATA")
    mpl.plot(xi, yi)
    mpl.show()
    
    log_score = []
    log_freq = []
    log_xi = []
    log_yi = []
    for i in range(len(scores)):
        if scores[i] != 0:
            log_score.append(math.log10(scores[i]))
        else:
            log_score.append(0)
        if frequencies[i] != 0:
            log_freq.append(math.log10(frequencies[i]))
        else:
            log_freq.append(0)
            
        if xi[i] != 0:
            log_xi.append(math.log10(xi[i]))
        else:
            log_xi.append(0)
        if yi[i] != 0:
            log_yi.append(math.log10(yi[i]))
        else:
            log_yi.append(0)
    
    
    
    mpl.title("PLOTING THE RAW DATA LOG SCALE")
    mpl.plot(log_score, log_freq)
    mpl.show()
    
    mpl.title("PLOTING THE INTERPOLATED SCORE DATA LOG SCALE")
    mpl.plot(log_xi, log_yi)
    mpl.show()

    print "PRINTING DIFFERENT FUNCTION LOOK"
    
    mpl.ylabel("Score")
    mpl.xlabel("Frequency")
    mpl.title("PLOT OF RAW SCORE DATA")
    mpl.plot(scores, frequencies, 'bo')
    mpl.savefig("/Users/johndoty/Desktop/raw_score")
    mpl.show()
    
    mpl.ylabel("Score")
    mpl.xlabel("Frequency")
    mpl.title("PLOT OF LOGARITHMIC TRANSFORMATION RAW DATA")
    mpl.plot(log_score, log_freq, 'bo')
    mpl.savefig("/Users/johndoty/Desktop/log_score")
    

    '''
   
    
    '''
    quantiles = [0.0, 0.01, 0.05, 0.1, 1-0.10, 1-0.05, 1-0.01, 1.0]
    print "\nTESTING NORMAL DISTRIBUTION"
    print 'normal skewtest teststat = %6.3f pvalue = %6.4f' % stats.skewtest(score_data_narray)
    print 'normal kurtosistest teststat = %6.3f pvalue = %6.4f' % stats.kurtosistest(score_data_narray)
    print "\nTESTING UNIFORM DISTRIBUTION"
    shape, loc, scale = stats.uniform.fit(score_data_narray)
    
    print "\nTESTING PARETO DISTRIBUTION"
    shape, loc, scale = stats.pareto.fit(score_data_narray)
    print "\nTESTING POWERLAW DISTRIBUTION"
    shape, loc, scale = stats.power.fit(score_data_narray)
    
    '''
    '''
    print "Printing Score Data"
    for item in score_data:
        print item
    #get list of score data
    score_list = []
    for item in score_data:
        score_list.append(item[0])
    np_score_list = np.array(score_list)
    mpl.hist(np_score_list, 10)
    mpl.show()
    mpl.hist(np_score_list, 6)
    mpl.show()
    
    score_zero = 0
    score_one = 0
    my_hist = [0, 0, 0, 0, 0, 0, 0]
    for item in score_list:
        if item <= 5:
            my_hist[0] +=1
        elif item <= 10:
            my_hist[1] +=1
        elif item <= 15:
            my_hist[2] +=1
        elif item <= 20:
            my_hist[3] +=1
        elif item <= 25:
            my_hist[4] +=1
        elif item <= 30:
            my_hist[5] +=1
        elif True:
            my_hist[6]+=1
        
        elif item <= 70:
            my_hist[6] +=1
        elif item <= 80:
            my_hist[7] +=1
        elif item <= 90:
            my_hist[8] +=1
        elif True:
            my_hist[9] +=1
        
        
        if item == 0:
            score_zero += 1
        if item == 1:
            score_one +=1
            
    count = 0
    for item in my_hist:
        print "ITEM %d is: %d" % (count, item)
    print "Number of items with a score of 0: %d" % score_zero
    print "Number of items with a score of 1: %d" % score_one
        
    
    '''
    
    
    '''
    #GENERATE PEARSON R VALUES FOR PROPERTIES IN PROPERTY LIST
    property_list = ['score', 'ups', 'downs', 'total_nodes_in_comments', 
                     'average_branching_factor', 'max_depth_tree', 'ratio_of_stubs', 'average_max_depth', ]
    #generate_pearson_values_time_series(time_series_data, properties, property_tuples=None)
    values = generate_pearson_values_time_series(time_series, property_list)
    keys = values.keys()
    keys.sort()
    for key in keys:
        print "Key is: "
        print key
        print "value is: "
        print values[key]
        print "\n"
    '''
    '''
   #print time_series['d24317293903faa9391d79f35e62b88a']['time_series'][0]
    doc = db['d24317293903faa9391d79f35e62b88a']
    print doc['time_series']['time_series'][0]['utc']
    '''