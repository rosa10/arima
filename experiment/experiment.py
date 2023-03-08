import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.holtwinters import SimpleExpSmoothing
from timeit import default_timer as timer
from sklearn.preprocessing import StandardScaler
import os
import csv
import sys
import time
import logging
from watchdog.observers import Observer  #creating an instance of the watchdog.observers.Observer from watchdogs class.
from watchdog.events import FileSystemEventHandler  #implementing a subclass of watchdog.events.FileSystemEventHandler which is LoggingEventHandler in our case
index = 0
train_len = 25
train_len_sec = 10 #in sec
forecast_length = 1
forecast_length_sec = 5 #in sec
zero_filter = 0
low_value_filter = 0
p = 0
d = 0
q = 1
model_type = "MA"

GroupByXTime = 5
truthSmooth = {
    "time" : [],
    "tp" : []
}
truth = {
    "time" : [],
    "tp" : [],
    "start" : []
}
directory=os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(directory,'perdetikesp3.txt')) as f:
    for line in f:
        x = line.split(";")
        
        start = float(x[1]) + float(x[2])/1000000
        end = float(x[3]) + float(x[4])/1000000
        
        truth["time"].append(float(end))
        truth["tp"].append(round(float(x[0])/(end-start)))
        
        truth["start"].append(float(start))  
print(start)
print(end)
df = pd.DataFrame(truth, columns=["time","tp","start"])
startTime = df["start"][0]

tpList=[]
buffer = 0
endTime = startTime + GroupByXTime
indexx = 0
for index, row in df.iterrows():
    if row["time"] <= endTime:
        tpList.append({'tp':row["tp"],'waktu': row["time"] - row["start"]})
        
        buffer = buffer + (row["time"] - row["start"])
        
    elif row["time"] > endTime:
        sum = 0
        if buffer == 0:
            truthSmooth["time"].append(endTime-GroupByXTime)
            truthSmooth["tp"].append(0)
            endTime = endTime + GroupByXTime
            continue
    
        for x in tpList:
            sum = sum + (x["waktu"]/GroupByXTime*(x["tp"]))
            
              
        indexx = indexx + 1
        tpList = []
        
        truthSmooth["time"].append(endTime-GroupByXTime)
        truthSmooth["tp"].append(sum)
        endTime = endTime + GroupByXTime
        tpList.append({'tp':row["tp"],'waktu': row["time"] - row["start"]})
        buffer = row["time"] - row["start"]
print("INI OY")
print(truthSmooth["tp"])
dfSmooth = pd.DataFrame(truthSmooth, columns=["time","tp"])
print(dfSmooth)

with open('5detik1.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["time","prediction"])
            for x in range(len(dfSmooth)):
                writer.writerow([truthSmooth["time"][x],truthSmooth["tp"][x]])

def a(inde):
    if (True) :
        
        tp_data = []
        row = {
            'byte': [],
            'start': [],
            'end': [],
            'diff': [],
            'tp/sec':[]
        }

        columns = ['byte','start','end','diff','tp/sec']
       
        start1 = time.time()
        #READ FILE A FILE
        directory=os.path.dirname(os.path.abspath(__file__))
        print(directory)
        a_file = open(os.path.join(directory,"perdetikesp3.txt"), "r")
        lines = a_file.readlines()
        last_xlines = lines[-(9999):]
        a_file.close()
        #CLOSE FILE
        
        for data in last_xlines:
            split = data.split(";")
            row['byte'].append(split[0])
            start = float(split[1]) + (float(split[2])/1000000)
            end = float(split[3]) + (float(split[4])/1000000)
            
            row['start'].append(str(start))
            row['end'].append(str(end))
            row['diff'].append(end-start)
            row['tp/sec'].append(round(float(split[0])/(end-start)))
            
        end1 = time.time()
        
        print(end1-start1)     
        df = pd.DataFrame(row, columns=columns)
       	
        total_forecast = []
        list_forecast = []

        tes1 = []
        tes2 = []
        
        buffer = 0
        listOfTp = []
        startExperiment = float(df.iloc[0]["start"])
        endExperiment = float(df.iloc[len(df.index) - 1]["end"])
        listOfPointing = []
        while startExperiment < endExperiment:
            
            startExperiment = startExperiment + forecast_length_sec
            listOfPointing.append(startExperiment)
            
        index = 0
        for poin in listOfPointing:
            index = index + 1
            print(index)
            for x in range (0, len(last_xlines) ):
		        
                start = float(df.iloc[x]["start"])
                
                if start < (poin - train_len_sec):
                    continue
                elif start > poin:
                    if len(listOfTp) == 1:
                        
                        tes1.append({"time" : poin, "prediction" : listOfTp[0]})
                        
                    elif len(listOfTp) == 0:
                        tes1.append({"time" : poin, "prediction" : 0})
                    else :

                        ### do prediction
                        model = sm.tsa.arima.ARIMA(listOfTp, order=(p, d, q))
                        fitted = model.fit()
                        fc = fitted.forecast(forecast_length, alpha=0.05)  # 95% conf
                        fc = fc.tolist()
                        
                        tes1.append({"time" : poin, "prediction" : fc[0]})
                        
                        
                    listOfTp = []
                    
                    break
                else:
                    listOfTp.append(df.iloc[x]["tp/sec"])
                
            
        print(tes1)
        with open('outesp3ma.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["time","prediction"])
            for data in tes1:
                
                writer.writerow([data["time"],data["prediction"]])
        print(tes2)
        with open('out2.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tes2)
# s = sched.scheduler(time.time, time.sleep)
# def do_something(sc): 
#     print("Doing stuff...")
#     # do your stuff
#     a()
#     sc.enter(15, 1, do_something, (sc,))

# s.enter(15, 1, do_something, (s,))
# s.run()
last_trigger = time.time()

class Handler(FileSystemEventHandler):
    
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
  
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            global last_trigger 
            current_time = time.time()
            if event.src_path.find('~') == -1 and (current_time - last_trigger) > 0.1:
                last_trigger = current_time
                global index 
                index = index + 1
                a(index)

if __name__ == "__main__":
    a(1)
    




