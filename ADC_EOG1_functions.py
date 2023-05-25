import time
import matplotlib.pyplot as plt 
import numpy as np
import pigpio
import ADS1115

pi = pigpio.pi()
ads = ADS1115.ADS1115()

recording_length = 5 #how many seconds
recording = [] #append to this list
time_rec=[]    #append to this list
trigger_rec=[] #append to this list
threshold=100
led1 = 17#11
led2 = 18#12
led3 = 27#13
pi.set_mode(led1, pigpio.OUTPUT)
pi.write(led1, 0)
pi.set_mode(led2, pigpio.OUTPUT)
pi.write(led2, 0)
pi.set_mode(led3, pigpio.OUTPUT)
pi.write(led3, 0)
flag=True
flag2=True
stop_flag=False