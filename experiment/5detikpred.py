import pandas as pd
import os
import csv

truth = {
    "time" : [],
    "tp" : []
}
directory=os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(directory,'output-lstm-Rosa.csv')) as f:
    for line in f:
        x = line.split(",")
        # print(x)
        start = float(x[0]) + 1
        end = float(x[1])
        
        truth["time"].append(float(start))
        truth["tp"].append((end))
print(truth)
with open('output-5detik1.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["time","prediction"])
            for x in range(len(truth["time"])):
                writer.writerow([truth["time"][x],truth["tp"][x]])
        