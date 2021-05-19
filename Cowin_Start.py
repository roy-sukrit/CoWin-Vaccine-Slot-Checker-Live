import requests
import schedule 
from datetime import datetime, timedelta
import pandas as pd
import platform
import subprocess
import os

class Cowin_Slot:

    def __init__(self,data):

        self.district = data      

    def alarm(self):

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


    def check_slot(self):               

        week=[0,1,2,3,4,5,6,7,8,9,10]

        for limit in week:
            # print(limit)
            
            # district =725
            date = datetime.now()
            today = date.strftime("%d-%m-%Y")
            days_limit = (date + timedelta(days=limit)).strftime("%d-%m-%Y")

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(self.district, days_limit)

            header = {"accept": "application/json",'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'} 

            result = requests.get(URL, headers=header)

            if(result.status_code == 200):
                result_Cowin = result.json()
                
            #^<------------Init------------------------>
                Name = []
                Age = []
                Vaccine = []
                Available_Capacity =[]
                Dose_1 = []
                Dose_2 = []
                Date_today = []
                info = []
                info=result_Cowin["sessions"]
            #^<------------Init------------------------>

                for y in info:
                    try:
                        Name.append(y["name"])
                    except:
                        Name.append(None)    
                    try:                            
                        Age.append(y["min_age_limit"])                        
                    except:
                        Age.append(None)    
                    
                    try:
                        Vaccine.append(y["vaccine"])
                    except:
                        Vaccine.append(None) 

                    try:   
                        Available_Capacity.append(y["available_capacity"])

                    except:
                        Available_Capacity.append(None)

                    try:
                        Dose_1.append(y["available_capacity_dose1"])

                    except:
                        Dose_1.append(None)
                        
                    try:
                        Dose_2.append(y["available_capacity_dose2"])
                    except: 
                        Date_today.append(None) 
                
                    try:
                         Date_today.append(y["date"])
                    except:
                         Date_today.append(None)                 
                   

                data_set = {
                    'Name':Name,
                    'Age' : Age,
                    'Vaccine': Vaccine,
                    'Available-Capacity':Available_Capacity,
                    "Dose-1" : Dose_1,
                    "Dose-2" : Dose_2,
                    "Date" : Date_today
                }
                if(Name == []):
                    
                    print("No Slots on " ,days_limit )
                else:
                    self.alarm()
                    
                    print("SLOT AVAILABLE GO TO THE COWIN Site NOW!!!!!")
                    print(pd.DataFrame(data_set))


            else:
                print("Error")


#^Init the object

def start_script():
    

    try:
        t = open('./district_id.txt')
        your_district_id = t.read()
        start_Cowin = Cowin_Slot(your_district_id)
        print("Running Script ")
        start_Cowin.check_slot()
        end = datetime.now()
        print("Execution Complete \n Last Execution on {}".format(end))   

    except:   
        print("Invalid Id in text file start again")


start_script()
schedule.every(2).minutes.do(start_script)
while True:
    schedule.run_pending()  




