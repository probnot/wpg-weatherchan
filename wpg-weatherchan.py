# Retro Winnipeg Weather Channel
# By probnot
# code is scrounged together, please be kind

from tkinter import *
import time
import datetime
from env_canada import ECData
import feedparser

# clock Updater

def clock():
    current = time.strftime("%I:%M:%S")
    timeText.configure(text=current)
    root.after(1000, clock) # run every 1sec
    
# main weather pages
    
def weather_page():
    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min
       
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    months = [" ", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    if time_sec < 30:
        weathercol = "Blue"
        if (time_min % 2) == 0: # screen 1 -- today's forecast in text + start of tomorrow's forecast
            text_sum = ec_en.conditions["text_summary"]["value"] 
            s = text_sum.upper()
            tomorrow =  ec_en.daily_forecasts[2]["text_summary"]
            t = tomorrow.upper()
            s1 = s[:35]
            s2 = s[35:70]
            s3 = s[70:105]
            s4 = s[105:140]
            s5 = s[140:175]
            s6 = " "
            s7 = "TOMORROW. " + t[:25]
            s8 = t[25:60]
        else: # screen 3 -- Today's day/date + specific weather conditions
            day = datetime.datetime.today().weekday()
            month = datetime.datetime.today().month
            tendency = ec_en.conditions["tendency"]["value"]
            TENDENCY = tendency.upper()
            s1 = " WINNIPEG - " + days[day] + ", " + months[month] + ". " + datetime.datetime.now().strftime("%d/%Y")
            s2 = " "
            s3 = "TEMP " + ec_en.conditions["temperature"]["value"] + "C (FEELS LIKE " + ec_en.conditions["wind_chill"]["value"] + "C)"
            s4 = ".. AND " + TENDENCY
            s5 = "HIGH OF " + ec_en.conditions["high_temp"]["value"] + "C     " + "LOW OF " + ec_en.conditions["low_temp"]["value"] + "C"
            s6 = "WIND " + ec_en.conditions["wind_dir"]["value"] + " " + ec_en.conditions["wind_speed"]["value"] + " KMH   VISIBILITY " + ec_en.conditions["visibility"]["value"] + "KM"
            s7 = "HUMIDITY " + ec_en.conditions["humidity"]["value"] + "%    DEWPOINT " + ec_en.conditions["dewpoint"]["value"] + "C"
            s8 = "PRESSURE " + ec_en.conditions["pressure"]["value"] + "KPA"
    if time_sec >= 30:
        weathercol = "Red"
        if (time_min % 2) == 0: # screen 2 -- next day forecast cont'd + 3rd day
            tomorrow =  ec_en.daily_forecasts[2]["text_summary"] # this is the forecast for the nex day (2nd total)
            t = tomorrow.upper()
            nday = ec_en.daily_forecasts[3]["text_summary"] # this is the forecast 2 days from now (3rd total)
            n = nday.upper()
            nper = ec_en.daily_forecasts[3]["period"] # this is the day of the forecast 2 days from now (3rd total)
            np = nper.upper()
            s1 = t[60:95]
            s2 = t[95:130]
            s3 = t[130:165]
            s4 = t[165:200]
            s5 = " "
            s6 = np + ". " + n[:24]
            s7 = n[24:59]
            s8 = n[60:95]
        else:  # screen 4 -- this can be used for more weather data, or just a static message
            s1 = "          CHANNEL LISTING "
            s2 = "================================== "
            s3 = "3.1 CBWFT (SRC)  DT   18  SECURITY "
            s4 = "6.1 CBWT (CBC)  DT    20  SEINFELD "
            s5 = "7.1 CKY (CTV)  DT     22  WEATHER "
            s6 = "9.1 CKND (GLOBAL) DT "
            s7 = "14  THE SIMPSONS "
            s8 = "16  **RESERVED**"

    # create the canvas for middle page text

    weather = Canvas(root, height=270, width=720, bg=weathercol)
    weather.place(x=0, y=100)
    weather.config(highlightbackground=weathercol)
    
    # place the 8 lines of text
    weather.create_text(85, 15, anchor='nw', text=s1, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 45, anchor='nw', text=s2, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 75, anchor='nw', text=s3, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 105, anchor='nw', text=s4, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 135, anchor='nw', text=s5, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 165, anchor='nw', text=s6, font=('VCR OSD Mono', 20, "bold"), fill="white")
    weather.create_text(85, 195, anchor='nw', text=s7, font=('VCR OSD Mono', 20, "bold"), fill="white") 
    weather.create_text(85, 225, anchor='nw', text=s8, font=('VCR OSD Mono', 20, "bold"), fill="white") 
    
    root.after(30000, weather_page) # re-run every 30sec from program launch

# setup main stuff

root = Tk()
root.attributes('-fullscreen',True)
root.geometry("720x480")
root.config(cursor="none", bg="green")
root.wm_title("wpg-weatherchan_V0.0.12")

# Clock - Top RIGHT

timeText = Label(root, text="", font=("VCR OSD Mono", 36), fg="white", bg="green")
timeText.place(x=425, y=40)
clock()

# Title - Top LEFT

Title = Label(root, text="ENVIRONMENT CANADA", font=("VCR OSD Mono", 22), fg="white", bg="green")
Title.place(x=80, y=55)

# use ECData to gather weather data, station_id is from the csv file provided with ECDada -- homepage: https://github.com/michaeldavie/env_canada

ec_en = ECData(station_id='MB/s0000193', language='english')
ec_en.update()

# Middle Section (Cycling weather pages, every 30sec)

weather_page()

# scrolling text canvas

marquee = Canvas(root, height=120, width=580, bg="green")
marquee.config(highlightbackground="green")
marquee.place(x=80, y=375)

# read in RSS data and prepare it

width = 35
pad = ""
for r in range(width): #create an empty string of 35 characters
    pad = pad + " " 

url = "https://winnipeg.ca/interhom/RSS/RSSNewsTopTen.xml"
wpg = feedparser.parse(url)

# use the first 8 entries on the wpg news RSS feed
wpg_desc = wpg.entries[0]["description"] + pad + wpg.entries[1]["description"] + pad + wpg.entries[2]["description"] + pad + wpg.entries[3]["description"] + pad + wpg.entries[4]["description"] + pad + wpg.entries[5]["description"] + pad + wpg.entries[6]["description"] + pad + wpg.entries[7]["description"]
mrq_msg = wpg_desc.upper()

# use the length of the news feeds to determine the total pixels in the scrolling section
marquee_length = len(mrq_msg)
pixels = marquee_length * 24 # roughly 24px per char

# setup scrolling text

text = marquee.create_text(1, 2, anchor='nw', text=pad + mrq_msg + pad + pad, font=('VCR OSD Mono', 25,), fill="white")

restart_marquee = True # 
while restart_marquee:
    restart_marquee = False
    for p in range(pixels+601):
        marquee.move(text, -1, 0) #shift the canvas to the left by 1 pixel
        marquee.update()
        time.sleep(0.005) # scroll every 5ms
        if p == pixels+600: # once the canvas has finished scrolling
            restart_marquee = True
            marquee.move(text, pixels+600, 0) # reset the location
            p = 0 # keep the for loop from ending
    
root.mainloop()