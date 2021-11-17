




import json
from zipfile import ZipFile

from numpy.core.fromnumeric import mean
from numpy.lib.function_base import average


def countFile(dayhourS):
    with ZipFile('./TwitterJune2021/geoEurope_202106'+dayhourS+'.zip', 'r') as myzip:
            with myzip.open('geoEurope/geoEurope_202106'+dayhourS+'.json', 'r') as file: # dayS+hourS
                count = 0
                countedTweets = {}
                for line in file:
                    jline = json.loads(line)
                    if 'text' in jline:
                        if not jline['text'] in countedTweets: # will this include retweets? should it?
                            countedTweets[jline['text']] = jline['user']['id_str'] # might not return dictionary? need to json the return?
                            count += 1
                        else:
                            if not jline['user']['id_str'] in countedTweets[jline['text']]:
                                countedTweets[jline['text']]  +=  jline['user']['id_str']
                                count +=1

                return count, dayhourS
def getArgs():
    args = []
    for day in range(1,31):
        dayS = str(day)
        if day < 10:
            dayS = "0"+str(day)
        for hour in range(24):
            hourS = str(hour)
            if hour < 10:
                hourS = "0"+str(hour)
            args.append([dayS, hourS])
    return args


import numpy as np
import pandas as pd
results = pd.DataFrame([], columns= sorted(set(np.array(getArgs())[:,0])), index= sorted(set(np.array(getArgs())[:,1])))


# import concurrent.futures
# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = [executor.submit(countFile,days+hours) for days, hours in getArgs()]
#         lines = []
#         for f in concurrent.futures.as_completed(results):
#             #print(f.result())
#                 lines.append(str(f.result()) + "\n")
#         with open('results.txt', 'w') as file:
#             file.writelines(lines)



def importDataToDF(res):
    with open('results.txt','r') as file:
        for line in file.readlines():
            line = line.replace("(","").replace(")","").replace(" ","").replace("\n","").replace("'","").split(',')
            #print(line[1][2:4])
            res[line[1][0:2]][line[1][2:4]] = int(line[0])
            # line contains tuple make it into array
            # save to res by using substring
    return res

def totalCount():
    return sum(results.sum().values)

import matplotlib.pyplot as plt
def plotTimeSeriesByDay():
    x = results.columns
    y = results.sum().values
    plt.plot(x,y) 
    plt.show()

def weekendAverages():
    return averages(sorted(np.array([results[e].values for e in ['05', '06', '12', '13', '19','20', '26', '27']]).flatten()))

def weekdayAverages():
    data = ['01','02','03','04', '07','08','09','10','11', '14','15','16','17','18','21','22','23','24','25','28','29','30']
    return averages(sorted(np.array([results[e].values for e in data]).flatten()))
    
def averages(values):
    mean = sum(values)/len(values)
    median = np.median(values)
    uq = np.quantile(values, 0.75)
    lq = np.quantile(values, 0.25)

    return mean, lq, uq, median

def tweetsVsTODWeekday():
    inputs = ['01','02','03','04', '07','08','09','10','11', '14','15','16','17','18','21','22','23','24','25','28','29','30']
    times = ['00','01','02','03','04','05','06', '07','08','09','10','11','12','13', '14','15','16','17','18','19','20','21','22','23']
    plt.scatter(times, tweetsVsTOD(inputs))
    plt.title('Weekday')
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Tweets')
    plt.figure()

def tweetsVsTODWeekend():
    inputs =  ['05', '06', '12', '13', '19','20', '26', '27']
    times = ['00','01','02','03','04','05','06', '07','08','09','10','11','12','13', '14','15','16','17','18','19','20','21','22','23']
    plt.scatter(times, tweetsVsTOD(inputs))
    plt.title('Weekend')
    plt.xlabel('Time of Day')
    plt.ylabel('Number of Tweets')
    plt.figure()
def tweetsVsTOD(inputs):
    data = np.array([results[e].values for e in inputs])
    totalCounts = data[0]
    i = 0
    for d in data:
        if i ==0:
            i =1
            continue
        
        for j in range(len(d)):
            totalCounts[j] += d[j]

    return totalCounts/(len(inputs)*24)

#results = importDataToDF(results)
#plotTimeSeriesByDay()
#print(totalCount())
#print(weekendAverages())
#print(weekdayAverages())
# print(tweetsVsTODWeekday())
# print(tweetsVsTODWeekend())
# plt.show()

def importCoordinates():
    res = []
    with open('coordinates.txt','r') as file:
        for line in file.readlines():
            #print(line[1][2:4])
            res.append(line)
            # line contains tuple make it into array
            # save to res by using substring
    return np.array(res)

print(importCoordinates())
import folium

from folium.plugins import HeatMap

mapObject = folium.Map((0.00,0.00), zoom_start=6)


data = [
    [24.399, 80.142],
    [22.252, 80.885],
    [24.311, 80.543],
    [23.195, 82.994],
    [23.431, 80.427],
    [26.363, 81.791],
    [22.942, 83.257],
    [23.751, 79.995],
    [23.215, 81.004],
    [24.541, 79.889]
]

HeatMap(data).add_to(mapObject)

mapObject.save("output.html")

# need to grab coordinates from all tweets
def coordinatesOfFile(dayhourS):
    with ZipFile('./TwitterJune2021/geoEurope_202106'+dayhourS+'.zip', 'r') as myzip:
            with myzip.open('geoEurope/geoEurope_202106'+dayhourS+'.json', 'r') as file: # dayS+hourS
                coordinates = [] 
                countedTweets = {}
                for line in file:
                    jline = json.loads(line)
                    if 'coordinates' in jline:
                        if not jline['coordinates'] == None:
                                if 'text' in jline:
                                    #print(jline['coordinates'] == None)
                                    if 'coordinates' in jline['coordinates']:
                                        if not jline['text'] in countedTweets: # will this include retweets? should it?
                                            countedTweets[jline['text']] = jline['user']['id_str'] 
                                            coordinates.append(jline['coordinates']['coordinates'])
                                        else:
                                            if not jline['user']['id_str'] in countedTweets[jline['text']]:
                                                countedTweets[jline['text']]  +=  jline['user']['id_str']
                                            coordinates.append(jline['coordinates']['coordinates'])
                out = ""
                for c in coordinates:
                    out = out + str(c) + "\n" # check appending string??
                return out

# put new coordinate on each line
# import concurrent.futures
# if __name__ == '__main__':
#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         results = [executor.submit(coordinatesOfFile,days+hours) for days, hours in getArgs()]
#         lines = []
#         for f in concurrent.futures.as_completed(results):
#             #print(f.result())
#                 lines.append(str(f.result()) + "\n")
#         with open('coordinates.txt', 'w') as file:
#             file.writelines(lines)
