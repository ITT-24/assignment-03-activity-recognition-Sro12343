# this program gathers sensor data
import time
from time import sleep
import csv
from datetime import datetime


from DIPPID import SensorUDP
#from DIPPID import SensorSerial
#from DIPPID import SensorWiimote

# use UPD (via WiFi) for communication
PORT = 5700
sensor = SensorUDP(PORT)



#setup global variables
id_counter = 0
activity_list = [["id","timestamp","acc_x","acc_y","acc_z","gyro_x","gyro_y","gyro_z"]]
time_stamp = 0
is_recording= True
interval = 1/100
number_of_entries = 1000
recording_num = 0

# Get recording name from user input
print("enter name")
recording_name = input()



# Record sensor data and write to CSV
def record():
    global is_recording
    global id_counter
    global recording_num 
    while(is_recording == True):
        start_time = time.time()
        
        #check if recording is full
        if id_counter < number_of_entries:
            if(sensor.has_capability('accelerometer') and sensor.has_capability('gyroscope')):
                # Get sensor data
                time_stamp = datetime.now()
                acc_x = sensor.get_value('accelerometer')['x']
                acc_y = sensor.get_value('accelerometer')['y']
                acc_z = sensor.get_value('accelerometer')['z']
                gyro_x = sensor.get_value('gyroscope')['x']
                gyro_y = sensor.get_value('gyroscope')['y']
                gyro_z = sensor.get_value('gyroscope')['z']
                
                #create and print entry
                new_entry = [id_counter,time_stamp,acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z]
                print(new_entry)
                activity_list.append(new_entry)
                id_counter +=1
        else: 
            #end recording
            is_recording = False
               
        elapsed_time = time.time() - start_time
        
        #Make certain the recording is at 100Hz
        sleep_time = interval - elapsed_time
        if sleep_time > 0:
            sleep(sleep_time)
    print("end")
    write_to_csv(activity_list)
    recording_num +=1
    id_counter = 0
        
#Write activity_list into csv
def write_to_csv(data):
    print("write")
    file_path = "./data/"+recording_name+".csv"
    #this was done with chatgpt
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

#Start recording
record()       


