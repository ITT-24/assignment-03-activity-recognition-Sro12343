# this program gathers sensor data
import time
from time import sleep
from activity_entry import activity_entry
import csv
from datetime import datetime


from DIPPID import SensorUDP
#from DIPPID import SensorSerial
#from DIPPID import SensorWiimote

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)



#setup the data collection
id_counter = 0
activity_list = [["id","timestamp","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z"]]
time_stamp = 0
is_recording= True
interval = 1/100
number_of_entries = 1000
recording_num = 0

print("enter name")
recording_name = input()

#Write activity_list into csv


def test():
    global is_recording
    global id_counter
    global recording_num 
    while(is_recording == True):
        start_time = time.time()
        if id_counter < number_of_entries:
            if(sensor.has_capability('accelerometer') and sensor.has_capability('gyroscope')):

                time_stamp = datetime.now()
                acc_x = sensor.get_value('accelerometer')['x']
                acc_y = sensor.get_value('accelerometer')['y']
                acc_z = sensor.get_value('accelerometer')['z']
                gyro_x = sensor.get_value('gyroscope')['x']
                gyro_y = sensor.get_value('gyroscope')['y']
                gyro_z = sensor.get_value('gyroscope')['z']
                
                
                #print(str(id_counter),str(time_stamp),str(acc_x),str(acc_y),str(acc_z),str(gyro_x),str(gyro_y),str(gyro_z)) 
                
                new_entry = [id_counter,time_stamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
                print(new_entry)
                activity_list.append(new_entry)
                id_counter +=1
        else: 
            print("end")
            is_recording = False
                
        elapsed_time = time.time() - start_time
        sleep_time = interval - elapsed_time
        if sleep_time > 0:
            sleep(sleep_time)
    print("end")
    write_to_csv(activity_list)
    recording_num +=1
    id_counter = 0
    
        
def record_data(position):
    global is_recording
    global id_counter
    global recording_num 
    while(True):
        start_time = time.time()
        if id_counter < number_of_entries:
            if(sensor.has_capability('accelerometer') and sensor.has_capability('gyroscope')):
        # print whole accelerometer object (dictionary)
        #print('accelerometer data: ', sensor.get_value('accelerometer'))

        # print only one accelerometer axis
        #print('accelerometer X: ', sensor.get_value('accelerometer')['x'])
        
        
                time_stamp = datetime.now()
                
                
                print(sensor.get_value('accelerometer')['x'])
                #new_entry = activity_entry(id_counter,time_stamp,sensor.get_value('accelerometer')['x'],sensor.get_value('accelerometer')['y'],sensor.get_value('accelerometer')['z'],sensor.get_value('gyroscope')['x'],sensor.get_value('gyroscope')['y'],sensor.get_value('gyroscope')['z'])
                acc_x = sensor.get_value('accelerometer')['x']
                acc_y = sensor.get_value('accelerometer')['y']
                acc_z = sensor.get_value('accelerometer')['z']
                gyro_x = sensor.get_value('gyroscope')['x']
                gyro_y = sensor.get_value('gyroscope')['y']
                gyro_z = sensor.get_value('gyroscope')['z']
                
                
                #print(str(id_counter),str(time_stamp),str(acc_x),str(acc_y),str(acc_z),str(gyro_x),str(gyro_y),str(gyro_z)) 
                
                new_entry = [id_counter,time_stamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
                #print(new_entry)
                activity_list.append(new_entry)
                id_counter +=1
            #record_single_data()
        else:
            break
        elapsed_time = time.time() - start_time
        sleep_time = interval - elapsed_time
        if sleep_time > 0:
            sleep(sleep_time)
            
    write_to_csv(activity_list)
    is_recording = False
    print("end")
    recording_num +=1
    id_counter = 0
    
def record_single_data():
    global id_counter   
    global sensor
    #print('capabilities: ', sensor.get_capabilities())
        # check if the sensor has the 'accelerometer' capability
    if(sensor.has_capability('accelerometer') and sensor.has_capability('gyroscope')):
        # print whole accelerometer object (dictionary)
        #print('accelerometer data: ', sensor.get_value('accelerometer'))

        # print only one accelerometer axis
        #print('accelerometer X: ', sensor.get_value('accelerometer')['x'])
        
        
        time_stamp = datetime.now()
        
        
        print(sensor.get_value('accelerometer')['x'])
        #new_entry = activity_entry(id_counter,time_stamp,sensor.get_value('accelerometer')['x'],sensor.get_value('accelerometer')['y'],sensor.get_value('accelerometer')['z'],sensor.get_value('gyroscope')['x'],sensor.get_value('gyroscope')['y'],sensor.get_value('gyroscope')['z'])
        acc_x = sensor.get_value('accelerometer')['x']
        acc_y = sensor.get_value('accelerometer')['y']
        acc_z = sensor.get_value('accelerometer')['z']
        gyro_x = sensor.get_value('gyroscope')['x']
        gyro_y = sensor.get_value('gyroscope')['y']
        gyro_z = sensor.get_value('gyroscope')['z']
        
        
        #print(str(id_counter),str(time_stamp),str(acc_x),str(acc_y),str(acc_z),str(gyro_x),str(gyro_y),str(gyro_z)) 
        
        new_entry = [id_counter,time_stamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
        #print(new_entry)
        activity_list.append(new_entry)
        id_counter +=1
            
        #check if finished
        
        

def write_to_csv(data):
    print("write")
    file_path = "./data/"+recording_name+".csv"
    #this was done with chatgpt
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    
def handle_button_press(data):
    print("data: "+ str(data))
    if int(data) == 1:
        global is_recording
        is_recording = True

 
 
test()       
#wait for button pressed to start recording.
#sensor.register_callback('button_1', handle_button_press)



