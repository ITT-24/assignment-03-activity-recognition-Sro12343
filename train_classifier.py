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
        self.rate = 100
        self.kernel = signal.windows.gaussian(self.kernel_size, self.kernel_sigma)
        self.classifier = None
            
    def start_training(self):
        #load and preprocess the data
        self.load_data()       
        #split data into a trainings and test set
        self.split_train_test()
        #create classifier
        self.classifier = self.create_classifier()
        
        #determin the accuracy
        self.get_accuracy()   
            
    #Load data from File
    def load_data(self):
        for f in os.listdir(self.data_Location):
            file_p = os.path.join(self.data_Location,f)
            if os.path.isfile(file_p):
                df = pd.read_csv(file_p)
                activity = self.decide_label(f)
                #devide into smaler data sets
                self.devide_data(activity,df)

    #dacide what activity a data set is, based on the file name
    def decide_label(self,f):
        if "rowing" in f:
            return "rowing" 
        elif "lifting" in f:
            return "lifting"  
        elif "running" in f:
            return "running"   
        elif "jumping" in f:
            return "jumpingjack"  
        elif "nothing" in f:
            return "nothing"
        
        
        
    #Devide date into smaler data sets
    #The method for deviding chunks came from ChatGpt          
    def devide_data(self, activity, df):
        num_rows = df.shape[0]
        num_chunks = (num_rows - 1)// self.sub_sample_size
        list_of_dfs = [df.iloc[i*self.sub_sample_size : (i+1)*self.sub_sample_size] for i in range(num_chunks)]
        for l in list_of_dfs:
            entry = self.construct_processed_data(activity, l)
            self.processed_data.append(entry)
            
    
    #Prepare to create data frame
    def construct_processed_data(self,activity,df):
        entry = {}
        entry['acc_x_f'] = self.calc_frequency(df['acc_x'])
        entry['acc_y_f'] = self.calc_frequency(df['acc_y'])
        entry['acc_z_f'] = self.calc_frequency(df['acc_z'])
        entry['gyro_x_f'] = self.calc_frequency(df['gyro_x'])
        entry['gyro_y_f'] = self.calc_frequency(df['gyro_y'])
        entry['gyro_z_f'] = self.calc_frequency(df['gyro_z'])
        entry['activity'] = activity
        return entry

    
    #Calculate max spectrum for data
    def calc_frequency(self, values):
        
        data = values
        
        # Perform Fourier transform to obtain the spectrum
        spectrum = np.abs(np.fft.fft(data))
       
        # Find the index of the maximum value in the spectrum
        spectrum_max = max(spectrum)

        return spectrum_max
       
       
    #Split data into training and test data
    #From ChatGPT
    def split_train_test(self):
        self.processed_data = pd.DataFrame(self.processed_data)
        self.train_data, self.test_data = train_test_split(self.processed_data, test_size=0.1, random_state=42)
        self.train_data = pd.DataFrame(self.train_data)
        self.test_data = pd.DataFrame(self.test_data)
        pass

    #Create and trains the Classifier
    def create_classifier(self):
        classifier = svm.SVC(kernel='linear')
        x = self.train_data[['acc_x_f','acc_y_f','acc_z_f','gyro_x_f','gyro_y_f','gyro_z_f']]
        y = self.train_data['activity']
        classifier.fit(x,y)
        return classifier
        
        
    #Check the accuracy of the classifier against the test_data
    def get_accuracy(self):
        self.test_data = pd.DataFrame(self.test_data)
        x = self.test_data[['acc_x_f','acc_y_f','acc_z_f','gyro_x_f','gyro_y_f','gyro_z_f']]
        y = self.test_data['activity']
        predictions = self.classifier.predict(x)
        print(predictions)
        accuracy = accuracy_score(y, predictions)
        print("Accuracy: " + str(accuracy))
        
        
    #predict what activity is being recorded by the sensor
    def predict_one(self,live_data):
        if len(live_data) >0 and live_data[0][0]!=None:
            self.live_data = live_data
            test = {}
            test['acc_x_f'] = self.calc_frequency([row[0] for row in self.live_data])
            test['acc_y_f'] = self.calc_frequency([row[1] for row in self.live_data])
            test['acc_z_f'] = self.calc_frequency([row[2] for row in self.live_data])
            test['gyro_x_f'] = self.calc_frequency([row[3] for row in self.live_data])
            test['gyro_y_f'] = self.calc_frequency([row[4] for row in self.live_data])
            test['gyro_z_f'] = self.calc_frequency([row[5] for row in self.live_data])
            test = pd.DataFrame([test])
            prediction = self.classifier.predict(test)
            return prediction[0]
        else:
            return "No measurement"        
        