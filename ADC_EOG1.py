from ADC_EOG1_functions import *

#################################################
# acquire baseline to subtract from samples #################
##############################################################################
baseline=ads.readADCSingleEnded(pga=6144,sps=860)
print("{:.0f} mV bsl".format(baseline))

#################################################
# start recording! ##########################################
##############################################################################
print('start rec')
time1=int(round(time.time()*1000))        #save start time in variable 'time1'
t_start=pi.get_current_tick() #hardware time

while True:
    #read in a sample
    sample=ads.readADCSingleEnded(pga=6144,sps=860)-baseline
    
    #append sample to trace and check if the threshold was crossed
    if not stop_flag:                          
        recording=np.append(recording,sample)
        if flag and sample>threshold: #did last sample cross the threshold?
            t2=pi.get_current_tick()
            pi.write(led3, 1)             #yes--change target LED
            pi.write(led2, 0)             #yes--change target LED
            flag=False
        if flag:
            trigger = 0
        else:
            trigger = 1     
        trigger_rec=np.append(trigger_rec,trigger)
        time_rec=np.append(time_rec,pi.get_current_tick())
        
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
        pi.write(led1, 0) 
        stop_flag=True
        yi = recording.copy()
        xi = time_rec.copy()-t_start
        yii=trigger_rec.copy()*10000
        yiii=(time_rec.copy()-t_start)/(pi.get_current_tick()-t_start)*(threshold+300-threshold-200)+threshold-200
        plt.ylim(threshold-300, threshold+600)
        plt.plot(xi, yi, linewidth=1, color='royalblue')
        plt.plot(xi, yii, linewidth=1, color='black')
#         plt.plot(xi, yiii, linewidth=1, color='green')
        print('reaction time to first target in microseconds')
#         print(pigpio.tickDiff(t1, t2))
        print('done')
        plt.show()
        break