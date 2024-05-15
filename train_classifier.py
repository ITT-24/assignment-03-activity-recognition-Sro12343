import os
import pandas as pd
import numpy as np
from scipy import signal
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score





class train_classifier():
    def __init__(self,number_of_entries):
        self.data_Location = os.path.join(os.getcwd(),"train_data")
        self.processed_data = []
        self.train_data = []
        self.test_data = []
        self.sub_sample_size = number_of_entries
        self.kernel_size = 21
        self.kernel_sigma = 3
        self.kernel = signal.windows.gaussian(self.kernel_size, self.kernel_sigma)
        self.rate = 100
        self.classifier = None
            
    def start_training(self):
        self.load_data()
        #print(self.processed_data)
        #print(len( self.processed_data))
        
        self.split_train_test()
        print("train: ")
        print(self.train_data)
        print("test: ")
        print(self.test_data)
        self.classifier = self.create_classifier()
        self.get_accuracy()   
            
    def decide_lable(self,f):
        if "rowing" in f:
            return "rowing" 
        elif "lifting" in f:
            return "lifting"  
        elif "running" in f:
            return "running"   
        elif "jumping" in f:
            return "jumpingjack"  

    #load all the files from data folder based on activi
    # ty.


    def load_data(self):
        for f in os.listdir(self.data_Location):
            
            entry = {}
            file_p = os.path.join(self.data_Location,f)
            if os.path.isfile(file_p):
                df = pd.read_csv(file_p)
                activity = self.decide_lable(f)
                #devide into smaler data sets
                self.devide_data(activity,df)
                



    #The method for deviding chunks came from CHatGpt          
    def devide_data(self, activity, df):
        num_rows = df.shape[0]
        #num_chunks = (num_rows + self.sub_sample_size - 1) // self.sub_sample_size
        num_chunks = (num_rows - 1)// self.sub_sample_size
        list_of_dfs = [df.iloc[i*self.sub_sample_size : (i+1)*self.sub_sample_size] for i in range(num_chunks)]
        for l in list_of_dfs:
            entry = self.construct_processed_data(activity, l)
            self.processed_data.append(entry)
        #for i in range(df.shape[0]/self.sub_sample_size):
        #    if i *self.sub_sample_size< num_rows:
                
                
                
    def construct_processed_data(self,activity,df):
        entry = {}
        
        #print(df)
        #print(df)
        entry['acc_x_f'] = self.calc_frequency(df['acc_x'])
        entry['acc_y_f'] = self.calc_frequency(df['acc_y'])
        entry['acc_z_f'] = self.calc_frequency(df['acc_z'])
        entry['gyro_x_f'] = self.calc_frequency(df['gyro_x'])
        entry['gyro_y_f'] = self.calc_frequency(df['gyro_y'])
        entry['gyro_z_f'] = self.calc_frequency(df['gyro_z'])
        entry['activity'] = activity
        return entry
        #self.processed_data.append(entry)
            
                

        
    def calc_frequency(self, values):
        
        data = values
        #hamming the input
        
        #data = values * np.hamming(len(values))
        #mitigate background noise 
        #data = np.convolve(data, self.kernel, 'same')

        # Perform Fourier transform to obtain the spectrum
        spectrum = np.abs(np.fft.fft(data))
        # Compute frequencies corresponding to each spectrum component
        #frequencies = np.fft.fftfreq(len(data), d=1 / self.rate)
        # Create a mask for positive frequencies
        #mask = frequencies >=0
        # Find the index of the maximum value in the spectrum
        
        spectrum_max = max(spectrum)
        #spectrum_max = np.argmax(spectrum[mask])
        
        #print("max: " +str(spectrum_max))
        return spectrum_max
        #print("data")
        #print(data)
        
        # Calculate the rate of change between adjacent entries
        #rate_of_change = np.diff(data)

        # Calculate the median rate of change
       # median_rate_of_change = np.median(rate_of_change)
        #return median_rate_of_change
        
    #From ChatGPT
    def split_train_test(self):
        #print("Split")
        self.processed_data = pd.DataFrame(self.processed_data)
        #print(self.processed_data.shape)
        self.train_data, self.test_data = train_test_split(self.processed_data, test_size=0.1, random_state=42)
        self.train_data = pd.DataFrame(self.train_data)
        self.test_data = pd.DataFrame(self.test_data)
        #print(self.train_data.shape)
       # print(self.test_data.shape)
       # print("end_Split")
        pass

    def create_classifier(self):
        
        #Maybe somewhere else?
        #Needs more different Classes for training-> test another data set
        
        
        
        classifier = svm.SVC(kernel='linear')
        x = self.train_data[['acc_x_f','acc_y_f','acc_z_f','gyro_x_f','gyro_y_f','gyro_z_f']]
        y = self.train_data['activity']
        classifier.fit(x,y)
        return classifier
        
        
        
    def get_accuracy(self):
        self.test_data = pd.DataFrame(self.test_data)
        x = self.test_data[['acc_x_f','acc_y_f','acc_z_f','gyro_x_f','gyro_y_f','gyro_z_f']]
        y = self.test_data['activity']
        predictions = self.classifier.predict(x)
        print(predictions)
        accuracy = accuracy_score(y, predictions)
        
        print("Accuracy: " + str(accuracy))
        
    def predict_one(self,live_data):
        self.live_data = live_data
        
        #print("Raw numbers:")
        #print(live_data)
        
        test = {}
        
        
        test['acc_x_f'] = self.calc_frequency([row[0] for row in self.live_data])
        test['acc_y_f'] = self.calc_frequency([row[1] for row in self.live_data])
        test['acc_z_f'] = self.calc_frequency([row[2] for row in self.live_data])
        test['gyro_x_f'] = self.calc_frequency([row[3] for row in self.live_data])
        test['gyro_y_f'] = self.calc_frequency([row[4] for row in self.live_data])
        test['gyro_z_f'] = self.calc_frequency([row[5] for row in self.live_data])
        test = pd.DataFrame([test])
        print("test")
        print(test)
        print(test.shape)
        prediction = self.classifier.predict(test)
        return prediction[0]
        
        
        
        return "predict_one is unfinished"
        
        