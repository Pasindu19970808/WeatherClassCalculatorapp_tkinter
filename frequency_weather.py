import pandas as pd
import numpy as np

data2015 = open(r'SKG2015.txt','r').readlines()
data2016 = open(r'SKG2016.txt','r').readlines()
data2017 = open(r'SKG2017.txt','r').readlines()
data2018 = open(r'SKG2018.txt','r').readlines()
data2019 = open(r'SKG2019.txt','r').readlines()
datacompile = [data2015,data2016,data2017,data2018,data2019]

headings = data2015[0].split()[:-1]
yymm = []
ddhh = []
direction = []
speed = []
PASQ = []
for data in datacompile:
    for i in range(1,len(data)):
        temp = data[i].split()
        yymm.append(float(temp[0][2:]))
        ddhh.append(float(temp[1][-2:]))
        direction.append(float(temp[2]))
        speed.append(float(temp[3])/10)
        PASQ.append(float(temp[4])/10)

yymmarray = np.array(yymm).reshape(-1,1)
ddhharray = np.array(ddhh).reshape(-1,1)
directionarray = np.array(direction).reshape(-1,1)
speedarray = np.array(speed).reshape(-1,1)
pasqarray = np.array(PASQ).reshape(-1,1)

dataset = np.concatenate([yymmarray,ddhharray,directionarray,speedarray,pasqarray],axis = 1)

rawdf = pd.DataFrame(data = dataset, columns  = headings)

#index to remove missing values
idx = rawdf[(rawdf['speed'] == -3276.7) | (rawdf['dir'] == -32767) | (rawdf['dir'] == 9999) | (rawdf['PASQ'] == -3276.7)].index

#6509 pieces of data had to be removed

#dataframe with no missing values
filtereddf = rawdf.drop(idx).reset_index(drop = True)

#Doing 50:50 split on data
idx1_5 = filtereddf[(filtereddf['PASQ'] == 1.5)].index
idx2_5 = filtereddf[(filtereddf['PASQ'] == 2.5)].index
idx3_5 = filtereddf[(filtereddf['PASQ'] == 3.5)].index
idx4_5 = filtereddf[(filtereddf['PASQ'] == 4.5)].index
idx5_5 = filtereddf[(filtereddf['PASQ'] == 5.5)].index

filtereddf.iloc[idx1_5[:int(len(idx1_5)/2)],4] = 1.0
filtereddf.iloc[idx1_5[int(len(idx1_5)/2):],4] = 2.0
filtereddf.iloc[idx2_5[:int(len(idx2_5)/2)],4] = 2.0
filtereddf.iloc[idx2_5[int(len(idx2_5)/2):],4] = 3.0
filtereddf.iloc[idx3_5[:int(len(idx3_5)/2)],4] = 3.0
filtereddf.iloc[idx3_5[int(len(idx3_5)/2):],4] = 4.0
filtereddf.iloc[idx4_5[:int(len(idx4_5)/2)],4] = 4.0
filtereddf.iloc[idx4_5[int(len(idx4_5)/2):],4] = 5.0
filtereddf.iloc[idx5_5[:int(len(idx5_5)/2)],4] = 5.0
filtereddf.iloc[idx5_5[int(len(idx5_5)/2):],4] = 6.0




#classing the PASQ according to its number
filtereddf['Class'] = np.nan
filtereddf.loc[(filtereddf['PASQ'] == 1),'Class'] = 'A'
filtereddf.loc[(filtereddf['PASQ'] == 2),'Class'] = 'B'
filtereddf.loc[(filtereddf['PASQ'] == 3),'Class'] = 'C'
filtereddf.loc[(filtereddf['PASQ'] == 4),'Class'] = 'D'
filtereddf.loc[(filtereddf['PASQ'] == 5),'Class'] = 'E'
filtereddf.loc[(filtereddf['PASQ'] == 6),'Class'] = 'F'

#obtaining day time and night time data

daydf = filtereddf.loc[(filtereddf['ddhh'].astype(int) >= 7) & (filtereddf['ddhh'].astype(int)<=18)].reset_index(drop = True)

nightdf = filtereddf.loc[(filtereddf['ddhh'].astype(int) == 1) | (filtereddf['ddhh'].astype(int) == 2) | (filtereddf['ddhh'].astype(int) == 3) | (filtereddf['ddhh'].astype(int) == 4) | (filtereddf['ddhh'].astype(int) == 5) |\
                (filtereddf['ddhh'].astype(int) == 6) | (filtereddf['ddhh'].astype(int) == 19) | (filtereddf['ddhh'].astype(int) == 20) | (filtereddf['ddhh'].astype(int) == 21) | (filtereddf['ddhh'].astype(int) == 22)|\
                (filtereddf['ddhh'].astype(int) == 23) | (filtereddf['ddhh'].astype(int) == 24)].reset_index(drop = True)



weather_classes = ['A','B','C','D','E','F']
day_index = [2,4,6,8,daydf['speed'].max()]
night_index = [2,4,6,8,nightdf['speed'].max()]

dayspeedfrequencies = pd.DataFrame(data = np.nan, columns = weather_classes, index = day_index)
nightspeedfrequencies = pd.DataFrame(data = np.nan, columns = weather_classes, index = night_index)

for weather in weather_classes:
    for speed in day_index:
        if day_index[-1] != speed:            
            dayspeedfrequencies.loc[speed,weather] = len(daydf.loc[(daydf['Class'] == weather) & ((daydf['speed'] >= (speed - 2)) & (daydf['speed'] < speed))])
        else:
            dayspeedfrequencies.loc[speed,weather] = len(daydf.loc[(daydf['Class'] == weather) & ((daydf['speed'] >= day_index[-2]))])
            
            
for weather in weather_classes:
    for speed in night_index:
        if night_index[-1] != speed:            
            nightspeedfrequencies.loc[speed,weather] = len(nightdf.loc[(nightdf['Class'] == weather) & ((nightdf['speed'] >= (speed - 2)) & (nightdf['speed'] < speed))])
        else:
            nightspeedfrequencies.loc[speed,weather] = len(nightdf.loc[(nightdf['Class'] == weather) & ((nightdf['speed'] >= night_index[-2]))])

