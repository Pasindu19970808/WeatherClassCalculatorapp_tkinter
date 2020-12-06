import tkinter as tk
import pandas as pd
import numpy as np
import os
from tkinter import ttk
from tkinter import filedialog


class parentclass(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        nb = ttk.Notebook(self)
        self.container1 = tk.Frame(nb, background = 'red4')
        self.container1.pack(fill = 'both', expand = True)
        
        self.pageframes = {}
        
        #instantiate the classes to put in container
        uploadpage_frame = uploadpage(self.container1,self)
        frequencyprocess_frame = processpercentageframe(self.container1,self)
        showtreeview_frame = showtreeview(self.container1,self)
        produceexcel_frame = produceexcelsheet_frequencies(self.container1, self)
        
        self.container1.grid_columnconfigure(0,weight = 1)
        self.container1.grid_columnconfigure(1,weight = 2)
       
        #uploadpage_frame.tkraise()
        uploadpage_frame.grid(row = 1, column = 0, sticky = 'nsew')
        frequencyprocess_frame.grid(row = 2, column = 0, sticky = 'nsew')
        showtreeview_frame.grid(row = 3, column = 0, sticky = 'nsew')
        produceexcel_frame.grid(row = 4, column = 0, sticky = 'nsew')
        
        self.pageframes[uploadpage] = uploadpage_frame
        self.pageframes[processpercentageframe] = frequencyprocess_frame
        self.pageframes[showtreeview] = showtreeview_frame
        self.pageframes[produceexcelsheet_frequencies] = produceexcel_frame
        
        nb.add(self.container1, text = 'Uploading and Processing')
        nb.pack(expand = 1, fill = 'both')
        
    def get_frame(self,framename):
        return self.pageframes[framename]
    
    def showfrequencyresults(self):
        frequencyresults_frame = treeviewresults(self.container1,self)
        frequencyresults_frame.grid(row = 1, column = 1)
        
    

        
class uploadpage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        #self.controller.geometry("1000x1000")
        self.config(background = 'red4')
        
        self.uploadframe = tk.LabelFrame(self, text = 'Upload Weather Data Txt Files', padx = 10, pady = 10)
        self.uploadframe.pack(side = 'top', fill = 'both')
        
        self.uploadbutton = tk.Button(self.uploadframe, text = 'Select Txt Files', command = lambda:self.uploadtxtfiles())
        self.uploadbutton.grid(row = 1, column = 1, padx = 10, pady = 10)
        
    
        self.statuslabel = tk.Label(self.uploadframe,text = 'Select Weather files to proceed')
        self.statuslabel.grid(row = 2, column = 1, padx = 10, pady = 10, stick = 'w')
        
        
        
    def uploadtxtfiles(self):
        try:
            file_directory = filedialog.askdirectory()
            os.chdir(file_directory)
            file_selection = filedialog.askopenfilenames()
            self.data_compiled = list()
            for filepath in file_selection:
                data = open(filepath,'r').readlines()
                self.data_compiled.append(data)
            
            self.statuslabel.configure(text = 'Txt Files Uploaded')
            
            
            print('hi')
        except:
            self.statuslabel.configure(text = 'Please Select the Required Txt Files')

class processpercentageframe(tk.Frame):
        def __init__(self,parent,controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            
            
            
            self.processoneframe = tk.LabelFrame(self, text = 'Process Weather Data', padx = 10, pady = 10)
            self.processoneframe.pack(side = 'top', fill = 'both') 
            
            self.frequency1 = tk.Button(self.processoneframe,text = 'Calculate Frequency of Weather Class and Speed',command = lambda:self.frequencyprocessing())
            self.frequency1.grid(row = 1, column = 1, padx = 10, pady = 10)
            
            self.statuslabel2 = tk.Label(self.processoneframe,text = 'Calculate % of Wind Speed and Weather Class')
            self.statuslabel2.grid(row = 2, column = 1, padx = 10, pady = 10, stick = 'w')
            
            
        def frequencyprocessing(self):
            uploadeddata = self.controller.get_frame(uploadpage)
            compileddatalist = uploadeddata.data_compiled
            
            print('hi')
            headings = compileddatalist[0][0].split()[:-1]
            yymm = []
            ddhh = []
            direction = []
            speed = []
            PASQ = []
            for data in compileddatalist:
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

            dataset = np.c_[yymmarray,ddhharray,directionarray,speedarray,pasqarray]
            rawdf = pd.DataFrame(data = dataset, columns  = headings)
            #index to remove missing values
            idx = rawdf[(rawdf['speed'] == -3276.7) | (rawdf['dir'] == -32767) | (rawdf['dir'] == 9999) | (rawdf['PASQ'] == -3276.7)].index
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

            self.dayspeedfrequencies = pd.DataFrame(data = np.nan, columns = weather_classes, index = day_index)
            self.nightspeedfrequencies = pd.DataFrame(data = np.nan, columns = weather_classes, index = night_index)
            
            for weather in weather_classes:
                for speed in day_index:
                    if day_index[-1] != speed:            
                        self.dayspeedfrequencies.loc[speed,weather] = len(daydf.loc[(daydf['Class'] == weather) & ((daydf['speed'] >= (speed - 2)) & (daydf['speed'] < speed))])
                    else:
                        self.dayspeedfrequencies.loc[speed,weather] = len(daydf.loc[(daydf['Class'] == weather) & ((daydf['speed'] >= day_index[-2]))])
            
            
            for weather in weather_classes:
                for speed in night_index:
                    if night_index[-1] != speed:            
                        self.nightspeedfrequencies.loc[speed,weather] = len(nightdf.loc[(nightdf['Class'] == weather) & ((nightdf['speed'] >= (speed - 2)) & (nightdf['speed'] < speed))])
                    else:
                        self.nightspeedfrequencies.loc[speed,weather] = len(nightdf.loc[(nightdf['Class'] == weather) & ((nightdf['speed'] >= night_index[-2]))])
             
            self.statuslabel2.configure(text = 'Completed Processing Data')
             
class showtreeview(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        #we can pack the place the dataframe into this frame
        self.controller = controller
        self.treeframe = tk.LabelFrame(self,text = 'Day Time Data')
        self.treeframe.pack(side = 'top',fill = 'both')
        
        self.showdata = tk.Button(self.treeframe, text = 'Show Processed Results', command = lambda:self.showfrequencyresults())
        self.showdata.grid(row = 1,column = 1, padx = 10, pady = 10)
    
    def showfrequencyresults(self):
        self.controller.showfrequencyresults()
        

class produceexcelsheet_frequencies(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.excelfrequencyframe = tk.LabelFrame(self, text = 'Extract Results')
        self.excelfrequencyframe.pack(side = 'top',fill = 'both')
        
        self.produce_excel_button = tk.Button(self.excelfrequencyframe, text = 'Extract results to excel file', command = lambda:self.extractexcelfrequency())
        self.produce_excel_button.grid(row = 1, column = 1, padx = 10, pady = 10)
        
    def extractexcelfrequency(self):
        processeddata = self.controller.get_frame(processpercentageframe)
        savepath = filedialog.askdirectory()
        os.chdir(savepath)
        with pd.ExcelWriter('Frequency_Results.xlsx') as writer:
            processeddata.dayspeedfrequencies.to_excel(writer, sheet_name = 'Day Data')
            processeddata.nightspeedfrequencies.to_excel(writer, sheet_name = 'Night Data')
        writer.close()

class treeviewresults(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.resultsframe = tk.LabelFrame(self, text = 'Results for Day Time and Night Time')
        self.resultsframe.pack(side = 'top',fill = 'both')
        
        processeddata = self.controller.get_frame(processpercentageframe)
        daydata = processeddata.dayspeedfrequencies.astype(int)
        nightdata = processeddata.nightspeedfrequencies.astype(int)
        
        my_tree1 = ttk.Treeview(self.resultsframe)
        
        my_tree1["column"] = daydata.columns.tolist()
        my_tree1["show"] = "headings"
        
        for column in my_tree1["columns"]:
            my_tree1.heading(column,text = column)
        daydata_rows = daydata.to_numpy().tolist()
        for row in daydata_rows:
            my_tree1.insert("","end",values = row)
            
        my_tree2 = ttk.Treeview(self.resultsframe)
        
        my_tree2["column"] = nightdata.columns.tolist()
        my_tree2["show"] = "headings"
        
        for column in my_tree2["columns"]:
            my_tree2.heading(column,text = column)
        nightdata_rows = nightdata.to_numpy().tolist()
        for row in nightdata_rows:
            my_tree2.insert("","end",values = row)
        my_tree1.pack(side = 'top',fill = 'both')
        my_tree2.pack(side = 'top',fill = 'both')
            
            
        
        
        
        
                
        
root = parentclass()
root.mainloop()