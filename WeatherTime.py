import requests
import json
import os
import astral
from astral import LocationInfo
from astral.sun import sun
import datetime
from datetime import date
import datetime
import time
import re
import ctypes
import sys
from suntime import Sun, SunTimeException
#from uncertainties import ufloat
latitude = 38.9893#51.21
longitude = -77.158611#21.01
sun = Sun(latitude, longitude)
todayD=date.today()
todayT=datetime.datetime.now() #Must be repeated        
abd = datetime.date(todayD.year, todayD.month, todayD.day)
abd_sr = sun.get_local_sunrise_time(abd)
abd_ss = sun.get_local_sunset_time(abd)

SR_Hour=abd_sr.hour
SR_Min=abd_sr.minute
SS_Hour=abd_ss.hour
SS_Min=abd_ss.minute
#get Daylight
if SR_Min<30:
    SR_Min=00
elif SR_Min>=30:
    SR_Min=00
    SR_Hour+=1

if SS_Min<30:
    SS_Min=00
elif SS_Min>=30:
    SS_Min=00
    SS_Hour+=1
s1=str(SR_Hour)+":"+str(SR_Min)+":00"
s2=str(SS_Hour)+":"+str(SS_Min)+":00"
FMT = '%H:%M:%S'
tdelta = datetime.datetime.strptime(s2, FMT) - datetime.datetime.strptime(s1, FMT)

DLTBB=datetime.timedelta(seconds=tdelta.seconds)
DayLightTime=re.split('[-:]', str(DLTBB))
DatLightTimeStr=str(DayLightTime[0])+":"+str(DayLightTime[1])


##CALC Solar Noon
##
SRStr=str(SR_Hour)+":"+str(SR_Min)
SSStr=str(SS_Hour)+":"+str(SS_Min)
FMT_SNCALC = '%H:%M'
SS_Num=datetime.datetime.strptime(SSStr, FMT_SNCALC)
SR_Num=datetime.datetime.strptime(SRStr, FMT_SNCALC)

SN_T_Hour=SR_Num.hour+SS_Num.hour
SN_T_Min=SR_Num.minute+SS_Num.minute




if(SN_T_Min%2==0): #Easily Divisible  Min
    SN_Min=SN_T_Min/2
else: #Not, just round up lol
    SN_Min=SN_T_Min/2+0.5
    

if(SN_T_Hour%2==0): #Easily Divisible  Hour
    SN_Hour=SN_T_Hour/2
else:
    SN_Hour=SN_T_Hour/2-.5 #NOW ADD 30 Minutes
    SN_Min+=30
    if(SN_Min>=60):#Add 1 to Hour
        SN_Min-=60
        SN_Hour+=1
SN_Min=int(SN_Min)
SN_Hour=int(SN_Hour)
if(SN_Min<10):
    SN_MinP='0'+str(SN_Min)#ADD LEADING 0 In If Needed
else:
    SN_MinP=SN_Min
    

TWC=[['']*2 for _ in range(7)]
TWC[0]=['00:00',
str(SR_Hour-2)+":"+str(SR_Min)]

TWC[1]=[str(SR_Hour-2)+":"+str(SR_Min),
str(SR_Hour)+":"+str(SR_Min)]

TWC[2]=[str(SR_Hour)+":"+str(SR_Min),
str(SN_Hour)+":"+str(SN_MinP)]

TWC[3]=[str(SN_Hour)+":"+str(SN_Min),
str(SS_Hour-3)+":"+str(SS_Min)]

TWC[4]=[str(SS_Hour-3)+":"+str(SS_Min),
str(SS_Hour) +":"+str(SS_Min)]

TWC[5]=[str(SS_Hour-3)+":"+str(SS_Min),
str(SS_Hour) +":"+str(SS_Min)]

TWC[6]=[str(SS_Hour)+":"+str(SS_Min),
"23:59"]
def TimesWhereChanged(doPrint=True):
    
    #Post_Night (Still night, no light but new day): 12:00 - (Sunrise-2 hours)  [night-normal]
    #   0-1
    #Pre_Night  (More Light: (Sunrise-2 Hours) - Sunrise)                       [evening-normal]
    #   2-3
    #Morning    (Morning: Sunrise - SolarNoon)                                  [morning-normal]
    #   4-5
    #Afternoon  (regular Daylight: SolarNoon - Sunset-3 Hours)                  [day-normal]
    #   6-7
    #Evening    (Darker:      Sunset-3 Hours - Sunset)                          [evening-normal]
    #   8-9
    #Night       (Night:   Sunset - Next Day (11:59)                            [night-normal]
    #   10-11
    
    
    if(doPrint==True):
        print("Post_Night :  12:00"+                            " - " +str(SR_Hour-2)+":"+str(SR_Min))
        
        print("Pre_Night  :  "+str(SR_Hour-2)+":"+str(SR_Min) + " - " + str(SR_Hour)+":"+str(SR_Min))
        
        print("Morning    :  "+str(SR_Hour)+":"+str(SR_Min) +   " - " + str(SN_Hour)+":"+str(SN_MinP))
        
        print("Afternoon  :  "+str(SN_Hour)+":"+str(SN_MinP) +   " - " + str(SS_Hour-3)+":"+str(SS_Min))
        
        print("Evening    :  "+str(SS_Hour-3)+":"+str(SS_Min) + " - " + str(SS_Hour) +":"+str(SS_Min))
        
        print("Night      :  "+str(SS_Hour)+":"+str(SS_Min)+    " - " + "23:59")

        print("\n\n\n----------------------------------\n")
        print(TWC)
        adadada=datetime.datetime.now()
        print("\n\n\n\n"+str(adadada.hour)+":"+str(adadada.minute))
TimesWhereChanged(False)
#todayT=datetime.datetime.now()
RN_Hour=todayT.hour
RN_Min=todayT.minute
#s = sun(city.observer, date=datetime.date(today.year, today.month, today.day))


#while(not time.sleep(60)): #update every n Seconds (Def=60)
todayT=datetime.datetime.now()
RN_Hour=todayT.hour
RN_Min=todayT.minute
SPI_SETDESKWALLPAPER = 0x14     #which command (20)
src=''
SPIF_UPDATEINIFILE   = 0x2 #forces instant update

url='https://api.openweathermap.org/data/2.5/weather?q=Bethesda,us&APPID=59eda94cb4ca5583dd5549ebdeea6a41'
json_data = requests.get(url).json()
mainWeather_Unformatted=json_data['weather'][0]['main']
mainWeatherFRMT = ''
#time.sleep(2)
def convWeather(UnformatWeather):
    global mainWeatherFRMT
    if(UnformatWeather=='Thunderstorm'):
        mainWeatherFRMT='thunder'
        #print('thunder')

    elif(UnformatWeather=='Drizzle' or UnformatWeather=='Rain'):
        mainWeatherFRMT='rain'
        #print('rain')

    elif(UnformatWeather=='Snow'):
        mainWeatherFRMT='snow'
        #print('snow')

    elif(UnformatWeather=='Mist' or UnformatWeather=='Smoke' or UnformatWeather=='Haze' or UnformatWeather=='Dust' or UnformatWeather=='Fog' or UnformatWeather=='Sand' or UnformatWeather=='Dust' or UnformatWeather=='Ash' or UnformatWeather=='Squall' or UnformatWeather=='Tornado'):
        mainWeatherFRMT='normal'
        #print('normal')

    elif(UnformatWeather=='Clear'):
        mainWeatherFRMT='normal'
        #print('normal')

    elif(UnformatWeather=='Clouds'):
        mainWeatherFRMT='cloudy'
        #print('cloudy')
        
    else:
        #print('Issue Converting Weather, resorting to normal')
        mainWeatherFRMT='normal'

def nightWall():
    src = r""+os.getcwd()+"\night-"+mainWeatherFRMT+".jpg"
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))


def eveningWall():
    src = r""+os.getcwd()+"\evening-"+mainWeatherFRMT+".jpg"
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))


def dayWall():
    src = r""+os.getcwd()+"\day-"+mainWeatherFRMT+".jpg"
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))


def morningWall():
    src = r""+os.getcwd()+"\morning-"+mainWeatherFRMT+".jpg"
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))





#mainWeather Possiblilies:
# Thunderstorm -> thunder
# Drizzle -> rain
# Rain -> rain
# Snow -> snow
# Mist,Smoke,Haze,Dust,Fog,Sand,Dust,Ash,Squall,Tornado -> normal
# Clear -> normal
# Clouds -> cloudy

#format_add = json_data['base']
#print(format_add)
#print(json.dumps(json_data, indent=4))

#naming:
#day-
#evening-
#morning-
#night-

# cloudy
# normal
# rain
# snow
# thunder
# wind

timeOfDay=''
def timeIfWall():
    
    global timeOfDay,RN_Min,RN_Hour,TWC
    todayT=datetime.datetime.now()
    RN_Hour=todayT.hour
    RN_Min=todayT.minute
    if(0<=RN_Hour<int(re.split('[-:]',TWC[0][1])[0])): #Midnight to 2H before Sunrise
    #if(RN_Min>=int(re.split('[-:]',TWC[0][1])[1])): #minutes
        print("night. Currently " + str(RN_Hour)+":"+str(RN_Min))
        timeOfDay='night'
        return('night')
        #nightWall()


    elif(int(re.split('[-:]',TWC[1][0])[0])<=RN_Hour<int(re.split('[-:]',TWC[1][1])[0])):#2 before sun- sunrise
        #if(RN_Min>=int(re.split('[-:]',TWC[1][1])[1])):#minutes
        timeOfDay='evening'
        return('evening')
        #eveningWall()


    elif(int(re.split('[-:]',TWC[2][0])[0])<=RN_Hour<int(re.split('[-:]',TWC[2][1])[0])):  #Sunrise to Noon
        #if(int(re.split('[-:]',TWC[2][0])[1])<=RN_Min): #minute
        timeOfDay='morning'
        return('morning')
        #morningWall()


    elif(int(re.split('[-:]',TWC[3][0])[0])<=RN_Hour<int(re.split('[-:]',TWC[3][1])[0])):  #Noon to Sunset-3
        #if(int(re.split('[-:]',TWC[3][0])[1])<=RN_Min): #minute
        timeOfDay='day'
        return('day')
        #dayWall()

    elif(int(re.split('[-:]',TWC[4][0])[0])<=RN_Hour<int(re.split('[-:]',TWC[4][1])[0])):  #Sunset-3-sunset
        #if(int(re.split('[-:]',TWC[4][0])[1])<=RN_Min): #minute
        timeOfDay='evening'
        return('evening')
        #eveningWall()


    elif(int(re.split('[-:]',TWC[6][0])[0])<=RN_Hour):#<int(re.split('[-:]',TWC[6][1])[0])):  #Sunset to midnight
        #if(int(re.split('[-:]',TWC[6][0])[1])<=RN_Min): #minute
        timeOfDay='night'
        return('night')
        #nightWall()

convWeather(mainWeather_Unformatted)
timeIfWall()
timeOfDay=timeIfWall()
def UpdateWallpaper(timeOD,mainWEATH):
    SPI_SETDESKWALLPAPER = 0x14     #which command (20)
    SPIF_UPDATEINIFILE   = 0x2 #forces instant update
    src = r""+os.getcwd()+"\\"+ timeOD +"-"+mainWEATH+".jpg"
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))

UpdateWallpaper(timeOfDay,mainWeatherFRMT)
    
#if(not(src=='')):
#print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, src, SPIF_UPDATEINIFILE))



#os.system('RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters')
"""
    if(RN_Hour<SR_Hour and RN_Min<SR_Min):
        print('Night')
    if((RN_Hour>=SR_Hour and RN_Min>=SR_Min) and (RN_Hour>=SR_Hour and RN_Min>=SR_Min)):
        pass
    

    if((RN_Min==0 or RN_Min==15 or RN_Min==30 or RN_Min==45)):#RN_Min%15==0):
        print("on the 15th")
    elif(RN_Hour==SR_Hour):
        print('SUNRISE')
    elif(RN_Hour==SS_Hour-12):
        print('SUNSET')
    """
#reg query "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper

