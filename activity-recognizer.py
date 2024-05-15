# this program recognizes activities
from train_classifier import train_classifier

import time
from time import sleep
from DIPPID import SensorUDP        
import pyglet
import os
PORT = 5700
sensor = SensorUDP(PORT)



class live_recorder():
    def __init__(self,number_of_entries):
        self.activity_list = []
        self.id_counter = 0
        self.interval = 1/100
        self.number_of_entries = number_of_entries
        self.model = train_classifier(self.number_of_entries)
        
        self.config = pyglet.gl.Config(double_buffer=True, depth_size=24)
        
        
        
        

    #from DIPPID import SensorSerial
    #from DIPPID import SensorWiimote

    # use UPD (via WiFi) for communication

    def start(self):
        self.model.start_training()

    def live_record(self,data):
        #start_time = time.time()
        #print(self.id_counter)
        if self.id_counter < self.number_of_entries:
            
            self.activity_list.append(data)
            self.id_counter +=1
            #self.record()
            return "No measurement"
        else:
            self.id_counter = 0
            #print("Check Clear")
            #print(self.activity_list)
            result = self.model.predict_one(self.activity_list)
            self.activity_list.clear()
            
            #print(self.activity_list)
            return result
        #elapsed_time = time.time() - start_time
        #sleep_time = self.interval - elapsed_time
        # if sleep_time > 0:
        #    sleep(sleep_time)



    def record(self):
        if(self.sensor.has_capability('accelerometer') and self.sensor.has_capability('gyroscope')):
            # print whole accelerometer object (dictionary)
            #print('accelerometer data: ', sensor.get_value('accelerometer'))

            # print only one accelerometer axis
            #print('accelerometer X: ', sensor.get_value('accelerometer')['x'])
            
   
            #new_entry = activity_entry(id_counter,time_stamp,sensor.get_value('accelerometer')['x'],sensor.get_value('accelerometer')['y'],sensor.get_value('accelerometer')['z'],sensor.get_value('gyroscope')['x'],sensor.get_value('gyroscope')['y'],sensor.get_value('gyroscope')['z'])
            acc_x = self.sensor.get_value('accelerometer')['x']
            acc_y = self.sensor.get_value('accelerometer')['y']
            acc_z = self.sensor.get_value('accelerometer')['z']
            gyro_x = self.sensor.get_value('gyroscope')['x']
            gyro_y = self.sensor.get_value('gyroscope')['y']
            gyro_z = self.sensor.get_value('gyroscope')['z']
            
            
            #print(str(id_counter),str(time_stamp),str(acc_x),str(acc_y),str(acc_z),str(gyro_x),str(gyro_y),str(gyro_z)) 
            
            new_entry = [acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
            self.activity_list.append(new_entry)
            self.id_counter +=1
            
            
            
            
window_size_x = 704
window_size_y = 704    
window = pyglet.window.Window(window_size_x, window_size_y)   

number_of_entries = 200
live_recorder = live_recorder(number_of_entries)
live_recorder.start()
current_dir = os.path.dirname(__file__)
image_list_1 = []
image_list_2 = []
activity_names = ["jumpingjack","lifting","rowing","running"]
index = 0

neutral_color = (205,205,205,255)
correct_color = (20,255,20,255)
false_color = (255,20,20,255)
background_color = (50,50,50,255)

lable_Instructions = pyglet.text.Label(text="Do: "+activity_names[index], x=10, y=650,color=neutral_color)
lable_output = pyglet.text.Label(text="Your Activity: ", x=10, y=550,color=neutral_color)





for n in activity_names:
    image_path = os.path.join(current_dir, 'images',n+"_1.png")
    image = pyglet.image.load(image_path)
    image_list_1.append(image)
    image_path = os.path.join(current_dir, 'images',n+"_2.png")
    image = pyglet.image.load(image_path)
    image_list_2.append(image)
    
    
sprit1 = pyglet.sprite.Sprite(img=image_list_1[index], x=100, y=100)
sprit1.scale = 0.2
sprit2 = pyglet.sprite.Sprite(img=image_list_2[index], x=300, y=100)
sprit2.scale = 0.2
background = pyglet.shapes.Rectangle(0,0,1000,1000,background_color)


@window.event
def on_key_press(symbol, modifiers):
    global index
    if symbol == pyglet.window.key.SPACE:
        if index+1 < len(activity_names)-1:
            index += 1
        else:
            index = 0
        sprit1.image = image_list_1[index]
        sprit2.image = image_list_2[index]
        lable_Instructions.text = "DO: "+ activity_names[index]
            
            
@window.event
def on_draw():
    window.clear()
    background.draw()
    
    sprit2.draw()
    sprit1.draw()
    lable_output.draw()
    lable_Instructions.draw()
    
    
    
    
def test():

    if(sensor.has_capability('accelerometer') and sensor.has_capability('gyroscope')):

        acc_x = sensor.get_value('accelerometer')['x']
        acc_y = sensor.get_value('accelerometer')['y']
        acc_z = sensor.get_value('accelerometer')['z']
        gyro_x = sensor.get_value('gyroscope')['x']
        gyro_y = sensor.get_value('gyroscope')['y']
        gyro_z = sensor.get_value('gyroscope')['z']
        
        
        #print(str(id_counter),str(time_stamp),str(acc_x),str(acc_y),str(acc_z),str(gyro_x),str(gyro_y),str(gyro_z)) 
        
        new_entry = [acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
        return new_entry
        #activity_list.append(new_entry)
          
    
def update(dt):
    data = test()
    result = live_recorder.live_record(data)
    print(result)
    if result !="No measurement":
        lable_output.text = "Your Activity: " + result
        
        if result == activity_names[index]:
            lable_output.color = correct_color
        else:
            lable_output.color = false_color
        
pyglet.clock.schedule_interval(update, 1/100)
pyglet.app.run()




