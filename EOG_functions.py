import threading
import serial
import time
import matplotlib.pyplot as plt 
import numpy as np
import pigpio

pi = pigpio.pi()

connected = False
port = '/dev/ttyACM0' #human spikerbox usbc
baud = 230400

writeInteger=[]
cBufTail = 0
time_buffer=[]
input_buffer = []
recording_length = 5 #how many seconds
sample_buffer = []
recording = []
trigger_rec=[]
trigger_buf=[]
time_rec=[]
threshold=8500
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
