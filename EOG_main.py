# Electro-oculogram close loop experiment based on code written by Stanislav Mircic
# Backyard Brains Sep. 2019
# Made for python 3
# First install serial library
# Install numpy, pyserial, matplotlib
# pip3 install pyserial
#
# Code will read, parse and display data from BackyardBrains' serial devices
#
# Written by Stanislav Mircic
# stanislav@backyardbrains.com

from EOG_functions import *

global connected
global input_buffer
global sample_buffer
global time_buffer
global cBufTail
global trigger_buf
global writeInteger
serial_port = serial.Serial(port, baud, timeout=0)
time.sleep(1)

def checkIfNextByteExist():
        global cBufTail
        global input_buffer
        tempTail = cBufTail + 1
        if tempTail==len(input_buffer): 
            return False
        return True
def checkIfHaveWholeFrame():
        global cBufTail
        global input_buffer
        tempTail = cBufTail + 1
        while tempTail!=len(input_buffer): 
            nextByte  = input_buffer[tempTail] & 0xFF
            if nextByte > 127:
                return True
            tempTail = tempTail +1
        return False;
def areWeAtTheEndOfFrame():
        global cBufTail
        global input_buffer
        tempTail = cBufTail + 1
        nextByte  = input_buffer[tempTail] & 0xFF
        if nextByte > 127:
            return True
        return False
def numberOfChannels():
    return 1
def handle_data(data):
    global input_buffer
    global cBufTail
    global sample_buffer
    if len(data)>0:
        cBufTail = 0
        haveData = True
        weAlreadyProcessedBeginingOfTheFrame = False
        numberOfParsedChannels = 0   
        while haveData:
            MSB  = input_buffer[cBufTail] & 0xFF
            if(MSB > 127):
                weAlreadyProcessedBeginingOfTheFrame = False
                numberOfParsedChannels = 0
                if checkIfHaveWholeFrame():
                    while True:
                        MSB  = input_buffer[cBufTail] & 0xFF
                        if(weAlreadyProcessedBeginingOfTheFrame and (MSB>127)):
                            #we have begining of the frame inside frame
                            #something is wrong
                            break #continue as if we have new frame
                        MSB  = input_buffer[cBufTail] & 0x7F
                        weAlreadyProcessedBeginingOfTheFrame = True
                        cBufTail = cBufTail +1
                        LSB  = input_buffer[cBufTail] & 0xFF
                        if LSB>127:
                            break #continue as if we have new frame
                        LSB  = input_buffer[cBufTail] & 0x7F
                        MSB = MSB<<7
                        writeInteger = LSB | MSB
                        numberOfParsedChannels = numberOfParsedChannels+1
                        if numberOfParsedChannels>numberOfChannels():
                            #we have more data in frame than we need
                            #something is wrong with this frame
                            break #continue as if we have new frame
                        sample_buffer = np.append(sample_buffer,writeInteger-512)
                        if areWeAtTheEndOfFrame():
                            break
                        else:
                            cBufTail = cBufTail +1
                else:
                    haveData = False
                    break
            if(not haveData):
                break
            cBufTail = cBufTail +1
            if cBufTail==len(input_buffer):
                haveData = False
                break
def read_from_port(ser):
    global connected
    global input_buffer
    while not connected:
        connected = True
        while True:       
           reading = ser.read(1024)
           if(len(reading)>0):
                reading = list(reading)         
                input_buffer = reading.copy()
                handle_data(reading)       
           time.sleep(0.001)
           
thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()
t_start=pi.get_current_tick() #hardware time

#########
####################
#BEGIN STUDENT PART#########
#####################################
#################################################
# start recording! ##########################################
##############################################################################

print('start rec')
time1=int(round(time.time()*1000))        #save start time in variable 'time1'

while True:
    #read in a sample
    sample=sample_buffer.copy()
    
    #append sample to trace and check if the threshold was crossed
    if not stop_flag and (len(sample)>0):                          
        recording=np.append(recording,np.mean(sample))
        sample_buffer=[]
        if flag and sample[-1]>threshold: #did last sample cross the threshold?
            t2=pi.get_current_tick()
            pi.write(led3, 1)             #yes--change target LED
            pi.write(led2, 0)             #yes--change target LED
            flag=False
        if flag:
            trigger_buf = 0
        else:
            trigger_buf = 1     
        trigger_rec=np.append(trigger_rec,trigger_buf)
        time_rec=np.append(time_rec,pi.get_current_tick())
        trigger_buf=[]
        time.sleep(0.001)
        
    #time control of experiment LEDs
    now=int(round(time.time()*1000)) #get current time
    timer1=now-time1                 #calculate time since start
    if timer1<2000:
        pi.write(led1, 1)            #led1 on for first 2000ms
    if flag and flag2 and timer1>2000:
        pi.write(led1, 0)            #change to target LED after 2s
        pi.write(led2, 1)            #change to target LED
        t1=pi.get_current_tick()     #store current hardware time in t1
        flag2=False                  #don't come here again
    if timer1>4000:
        pi.write(led1, 1)            #back to start after 4s
        pi.write(led2, 0)
        pi.write(led3, 0)
        
    #########################################
    #recording over, plot the result!
    if not stop_flag and timer1>recording_length*1000:
        stop_flag=True
        yi = recording.copy()
        xi = time_rec.copy()-t_start
        yii=trigger_rec.copy()*10000
        yiii=(time_rec.copy()-t_start)/(pi.get_current_tick()-t_start)*(11000-7000)+7000
        plt.ylim(5000, 11000)
        plt.plot(xi, yi, linewidth=1, color='royalblue')
        plt.plot(xi, yii, linewidth=1, color='black')
#         plt.plot(xi, yiii, linewidth=1, color='green')
        print('reaction time to first target')
        print(pigpio.tickDiff(t1, t2))
        print('done')
        plt.show()
        break
