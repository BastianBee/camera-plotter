import numpy as np
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd
from support_code.reader import csv_reader, dat_reader
from helper_test2 import helper_test_function2


###Let's see if this commit works

def main():
    print("Hello from camera-plotter!")


if __name__ == "__main__":
    main()

### Store table of RPI filename number (findex) with experimental parameter (Vp) for each measurement
### Save .csv file as f"{date}_Experiment{}" This will be the info table
### Index refers to the excel row number

def handler(directory, info_filename, date, index, samples):
    findex = csv_reader(directory+info_filename).iloc[index+1,1] #RPI filename parameter
    Vp = csv_reader(directory+info_filename).iloc[index+1,0] #Experimental parameter

    data = dat_reader(directory+f"RPI_{date}_{findex}.dat") #camera data 
    
    T = np.array(data.iloc[0:,0] - data.iloc[0,0]) #Converting unix epoch time to seconds starting at zero
    T_interval = T[samples-1] - T[0]

    intensity = np.array(data.iloc[0:,1])
    

    average = np.average(intensity[0:samples])
    std = np.std(intensity[0:samples])
    return T, intensity, Vp, average, std, T_interval
    


### Input file information here

##Example
# directory = "/home/octonator/Desktop/Augustus_Electrode/LED_Sensing/data/20260921/"
# info_filename = "RPI_Camera_File_Tracker_20260921.csv"
# date = "20260921"
# samples = 200
# N_measurements = 17

directory = "/home/octonator/Desktop/Augustus_Electrode/LED_Sensing/data/20261030/"
info_filename = "RPI_Camera_File_Tracker_20261030.csv"
date = "20261030"
samples = 100
N_measurements = 184

### Making lists of data arrays
intensity_avg_array = np.zeros(N_measurements) 
Vp_array = np.zeros(N_measurements)
std_array = np.zeros(N_measurements)
Ts = []
Is = []
background = handler(directory, info_filename, date, 0, samples)[3]
print(f"Background: {background}")

for i in range(N_measurements):
    handler_returns = handler(directory, info_filename, date, i, samples)

    Ts.append(handler_returns[0])
    Is.append(handler_returns[1])
    Vp_array[i] = handler_returns[2]
    intensity_avg_array[i] = handler(directory, info_filename, date, i, samples)[3] - background
    std_array[i] = handler_returns[4]

print(f"Intensity Average: {intensity_avg_array}")

###Log of array

logr = np.log(intensity_avg_array)

### Plotting averaged intensity 
fig, ax = plt.subplots(figsize=(10,10))
# lines = ax.plot(Vp_array, logr, linestyle='none', marker='.', markersize=10)
lines2 = ax.plot(Vp_array, intensity_avg_array, linestyle='none', marker='.', markersize=10)
ax.set_title("Average Intensity, R = 139.7, 140 kHz", fontsize=20)
ax.tick_params(axis='both', labelsize=14)
ax.set_xlabel("Drive Voltage, Vp", fontsize=15)
ax.set_ylabel("Average Intensity", fontsize=15)

mplcursors.cursor(lines2)

plt.show()


# ###Setting up subplots
# fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(10,10), layout="constrained")


# ## Plotting intensity vs time for multiple measurements
# for i in range(N_measurements):

#     ax1.plot(Ts[i][0:samples], Is[i][0:samples], linestyle='none', marker='.', markersize=1, label=f"Vp = {Vp_array[i]}")
#     ax1.tick_params(axis='both', labelsize=14)
#     ax1.legend(bbox_to_anchor=(-0.1,0.5), loc="center right")

# ax1.set_xlabel("Seconds")
# ax1.set_ylabel("Intensity")

# ### Plotting averaged intensity 

# ax2.plot(Vp_array, intensity_avg_array, linestyle='none', marker='.', markersize=10)
# ax2.set_title("Average Intensity, R = 139.7, 140 kHz")
# ax2.tick_params(axis='both', labelsize=14)
# ax2.set_xlabel("Vp", fontsize=10)
# ax2.set_ylabel("Average Intensity", fontsize=10)

# ## Plotting standard deviation
# ax3.plot(Vp_array, std_array, linestyle='none', marker='.', markersize=10)
# ax3.tick_params(axis='both', labelsize=14)
# ax3.set_xlabel("Vp")
# ax3.set_ylabel("Standard Deviation")


# plt.show()

