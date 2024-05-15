from train_classifier import train_classifier
import pyglet

class live_recognizer():
    def __init__(self,number_of_entries):
        self.activity_list = []
        self.id_counter = 0
        self.interval = 1/100
        self.number_of_entries = number_of_entries
        self.model = train_classifier(self.number_of_entries)
        self.config = pyglet.gl.Config(double_buffer=True, depth_size=24)

    #setup the model/classifier
    def start(self):
        self.model.start_training()


    def live_record(self,data):
        #check if enough data was gathered to make a prediction
        if self.id_counter < self.number_of_entries:   
            #Not enough data gathered jet         
            self.activity_list.append(data)
            self.id_counter +=1
            return "No measurement"
        else:
            #make a prediction
            result = self.model.predict_one(self.activity_list)
            self.id_counter = 0
            self.activity_list.clear()
            return result
