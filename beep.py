import platform
import subprocess
import os

 
if platform.system() == 'Darwin':
    os.system("afplay " + 'alarm.wav')
elif platform.system() == 'Linux':
    subprocess.call(["aplay", "alarm.wav"])
elif platform.system() == 'Windows':
    import winsound
    duration = [200,500,200,500,200,500,200,500] 
    freq = 440  
    for x in duration:    
        winsound.Beep(freq, x)