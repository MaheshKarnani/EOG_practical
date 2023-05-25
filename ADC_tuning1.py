from ADC_EOG1_functions import *
#########
####################
#BEGIN STUDENT PART#########
#####################################
#################################################
# start recording! ##########################################
##############################################################################

print('start TUNING')
time1=int(round(time.time()*1000)) #save start time in variable 'time1'
t_start=pi.get_current_tick() #hardware time

while True:
    #read in a sample
    sample=ads.readADCSingleEnded()
    print("{:.0f} mV mesuré sur AN0".format(sample))
    
    #append sample to trace and check if the threshold was crossed
    if not stop_flag:                          
        recording=np.append(recording,sample)
        time_rec=np.append(time_rec,pi.get_current_tick())
    now=int(round(time.time()*1000)) #get current time
    timer1=now-time1                 #calculate time since start    
    #########################################
    #recording over, plot the result!
    if not stop_flag and timer1>recording_length*1000:
        stop_flag=True
        yi = recording.copy()
        xi = time_rec.copy()-t_start
        yii = [threshold, threshold]
        xii = [0, xi[-1]]
        plt.ylim(0, 500)
        plt.plot(xi, yi, linewidth=1, color='royalblue')
        plt.plot(xii, yii, linewidth=2, color='black')
        print('done')
        plt.show()
        break
