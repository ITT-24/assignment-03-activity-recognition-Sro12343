# this program recognizes activities
from time import sleep
from DIPPID import SensorUDP        
import pyglet
import os
from live_recognizer import live_recognizer


#from DIPPID import SensorSerial
#from DIPPID import SensorWiimote

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)

#Setup pyglet window            
window_size_x = 704
window_size_y = 704    
window = pyglet.window.Window(window_size_x, window_size_y)   


#setup size of input for comparisson
number_of_entries = 100

#Setup recognizer
live_recognizer = live_recognizer(number_of_entries)
live_recognizer.start()

#Setup Trainings images
current_dir = os.path.dirname(__file__)
image_list_1 = []
image_list_2 = []
activity_names = ["jumpingjack","lifting","rowing","running"]
index = 0

#Setup the colors
neutral_color = (205,205,205,255)
correct_color = (20,255,20,255)
false_color = (255,20,20,255)
background_color = (50,50,50,255)

#Create labels
label_Instructions = pyglet.text.Label(text="Do: "+activity_names[index], x=10, y=650,color=neutral_color)
label_output = pyglet.text.Label(text="Your Activity: ", x=10, y=550,color=neutral_color)
label_space = pyglet.text.Label(text="Press Space for the next exercise", x=350, y=10,color=neutral_color, anchor_x='center')

#Load the different imagey
for n in activity_names:
    image_path = os.path.join(current_dir, 'images',n+"_1.png")
    image = pyglet.image.load(image_path)
    image_list_1.append(image)
    image_path = os.path.join(current_dir, 'images',n+"_2.png")
    image = pyglet.image.load(image_path)
    image_list_2.append(image)
    
    
#Create the sprites
sprit1 = pyglet.sprite.Sprite(img=image_list_1[index], x=100, y=100)
sprit1.scale = 0.2
sprit2 = pyglet.sprite.Sprite(img=image_list_2[index], x=300, y=100)
sprit2.scale = 0.2
background = pyglet.shapes.Rectangle(0,0,1000,1000,background_color)


@window.event
def on_key_press(symbol, modifiers):
    #Switch through the exercises
    global index
    if symbol == pyglet.window.key.SPACE:
        if index+1 <= len(activity_names)-1:
            index += 1
        else:
            index = 0
        sprit1.image = image_list_1[index]
        sprit2.image = image_list_2[index]
        label_Instructions.text = "DO: "+ activity_names[index]
            
            
@window.event
def on_draw():
    window.clear()
    background.draw()
    sprit2.draw()
    sprit1.draw()
    label_output.draw()
    label_Instructions.draw()
    label_space.draw()


def record():
    #load the live data of the user input
    if(sensor.has_capability('accelerometer') and sensor.has_capability('gyroscope')):
        acc_x = sensor.get_value('accelerometer')['x']
        acc_y = sensor.get_value('accelerometer')['y']
        acc_z = sensor.get_value('accelerometer')['z']
        gyro_x = sensor.get_value('gyroscope')['x']
        gyro_y = sensor.get_value('gyroscope')['y']
        gyro_z = sensor.get_value('gyroscope')['z']    
        new_entry = [acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
        return new_entry
          
    
def update(dt):
    data = record()
    result = live_recognizer.live_record(data)
    #check if a correct activity was detected
    if result !="No measurement":
        print(result)
        label_output.text = "Your Activity: " + result
        
        if result == activity_names[index]:
            label_output.color = correct_color
        else:
            label_output.color = false_color
 
#Start pyglet update and app loop       
pyglet.clock.schedule_interval(update, 1/100)
pyglet.app.run()




