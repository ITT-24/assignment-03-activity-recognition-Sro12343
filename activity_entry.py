class activity_entry():
    def __init__(self, id,timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z):
        #save all the data
        self.id = id
        self.timestamp = timestamp
        self.acc_x = acc_x
        self.acc_y = acc_y
        self.acc_z = acc_z
        self.gyro_x = gyro_x
        self.gyro_y = gyro_y
        self.gyro_z = gyro_z
        pass