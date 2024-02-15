# Retro Winnipeg Weather Channel
# By probnot

from tkinter import *
import time
import datetime
# from datetime import datetime
import asyncio # for env_canada
import textwrap # used to format forecast text
from env_canada import ECWeather
import feedparser # for RSS feed
import requests # for RSS feed
import json # for RSS feed
import pygame # for background music
import random # for background music
import os # for background music
import re # for word shortener

prog = "wpg-weather"
ver = "2.0.9"
# 2.0.9 [2024-02-11]
# - Fixed bug that has old blue colour upon launch (line 817), also changed blue to 0x00006D as noted in 2.0.8 but missed
# - Updated RSS section -- old code assumed at least 8 entries. new code is flexible up to max pixel size, also fixed it so it actually refreshes
# - Changed RSS scroll time to 2ms (was 5ms) to match original videon/shaw feed
# 2.0.8 [2024-01-20]
#   BUGFIX:
# - Added try functions to weather update (line 610 & 619) to prevent crashing once running - program will still crash if weather update fails on initial launch
# - Updated RSS feed URL to use CTV News (Thanks Tekhnocyte!)
# - Added code in screen 4 to avoid colour not changing if page is skipped
# - moved print/debug messages to new function debug_msg. Can enable/disable, select verbosity, add datestamp
#   IMPROVEMENT/MISC:
# - Updated channel listings on page 11 / removed pages 12 and 13
# - Increased vertical size of center page / moved text locations
# - Changed red colour from 0xBC0000 to 0x6D0000, changed blue colour from 0x0000A5 to 0x00006D (better visibility on b&w TVs)
# - Increased time between page changes to 20sec (was 10sec)
# 2.0.7 [2023-09-11]
# - Updated CityofWinnipeg RSS feed URL (old URL 404)
# 2.0.6 [2023-09-02]
# - Updated channel listings
# 2.0.5 - Skipped
# 2.0.4 [2023-06-06]
# - Line 89 humidex typo
# - Line 203 fixed high/low yesterday temp - added check for nonetype   
# 2.0.3
# - Updated channel listings
# 2.0.1
# - Changed forecast time to use current time when updating weather - the date and time from forecast_time in env_canada returns odd results
# - Changed UV INDEX to show -- instead of blank if no index is present

# DEF clock Updater
def clock():

    current = time.strftime("%-I %M %S").rjust(8," ")
    timeText.configure(text=current)
    root.after(1000, clock) # run every 1sec
    
# DEF main weather pages 
def weather_page(PageColour, PageNum):

    # pull in current seconds and minutes -- to be used to cycle the middle section every 30sec
    
    time_sec = time.localtime().tm_sec
    time_min = time.localtime().tm_min
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    months = [" ", "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]    
    linebreak = ['\n']

    PageTotal = 11

    if (PageNum == 1):
        
        # ===================== Screen 1 =====================
        # Today's day/date + specific weather conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)             
        
        # get local timezone to show on screen
        local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
        
        # weather data
        temp_cur = str(ec_en_wpg.conditions["temperature"]["value"])
        temp_high = str(ec_en_wpg.conditions["high_temp"]["value"])
        temp_low = str(ec_en_wpg.conditions["low_temp"]["value"])
        humidity = str(ec_en_wpg.conditions["humidity"]["value"])
        condition = ec_en_wpg.conditions["condition"]["value"]
        pressure = str(ec_en_wpg.conditions["pressure"]["value"])   
        tendency = ec_en_wpg.conditions["tendency"]["value"]
        dewpoint = str(ec_en_wpg.conditions["dewpoint"]["value"])
        uv_index = str(ec_en_wpg.conditions["uv_index"]["value"]) if ec_en_wpg.conditions["uv_index"] and ec_en_wpg.conditions["uv_index"]["value"] != None else "--"
        pop = str(ec_en_wpg.conditions["pop"]["value"]) if ec_en_wpg.conditions["pop"] and ec_en_wpg.conditions["pop"]["value"] != None else "0"
        
        # check severity of uv index
        if ec_en_wpg.conditions["uv_index"]["value"] != None:
            if ec_en_wpg.conditions["uv_index"]["value"] <= 2:
                uv_cat = "LOW"
            elif ec_en_wpg.conditions["uv_index"]["value"] > 2 and ec_en_wpg.conditions["uv_index"]["value"] <= 5:
                uv_cat = "MODERT"
            elif ec_en_wpg.conditions["uv_index"]["value"] > 5 and ec_en_wpg.conditions["uv_index"]["value"] <= 7:
                uv_cat = "HIGH"
            elif ec_en_wpg.conditions["uv_index"]["value"] > 7 and ec_en_wpg.conditions["uv_index"]["value"] <= 10:
                uv_cat = "V.HIGH"
            elif ec_en_wpg.conditions["uv_index"]["value"] > 10:
                uv_cat = "EXTRM"
        else:
            uv_cat = ""
        
        # check if windchill or humidex is present, if neither leave area blank
        if ("value" in ec_en_wpg.conditions["wind_chill"] and ec_en_wpg.conditions["wind_chill"]["value"] != None):
            windchill = str(ec_en_wpg.conditions["wind_chill"]["value"])
            windchildex = "WIND CHILL " + windchill + " C"
        elif ("value" in ec_en_wpg.conditions["humidex"] and ec_en_wpg.conditions["humidex"]["value"] != None):
            humidex = str(ec_en_wpg.conditions["humidex"]["value"])
            windchildex = "HUMIDEX " + humidex + " C       "
        else:
            windchildex = ""
        
        # check if there is wind - if not, display NO WIND
        if ("value" in ec_en_wpg.conditions["wind_dir"] and ec_en_wpg.conditions["wind_dir"]["value"] != None):        
            wind_dir = ec_en_wpg.conditions["wind_dir"]["value"]
            wind_spd = str(ec_en_wpg.conditions["wind_speed"]["value"])
            windstr = "WIND " + wind_dir + " " + wind_spd + " KMH"
        else:
            windstr = "NO WIND"
                
        # check visibility, if no data then show --
        if ("value" in ec_en_wpg.conditions["visibility"] and ec_en_wpg.conditions["visibility"]["value"] != None):
            visibility = str(ec_en_wpg.conditions["visibility"]["value"])
            visibstr = "VISBY " + visibility.rjust(5," ") + " KM         "
        else:
            visibstr = "VISBY    -- KM         "
     
        # create 8 lines of text     
        s1 = ("WINNIPEG " + real_forecast_time + " " + str(local_tz) + "  " + real_forecast_date.upper()).center(35," ")
        s2 = "TEMP  " + temp_cur.rjust(5," ") + " C                "
        s2 = s2[0:24] + " HIGH " + temp_high.rjust(3," ") + " C"
        s3 = word_short(condition,24) + "                         "
        s3 = s3[0:24] + "  LOW " + temp_low.rjust(3," ") + " C"
        s4 = ("CHANCE OF PRECIP. " + pop + " %").center(35," ")
        s5 = "HUMID  " + humidity.rjust(5," ") + " %         "
        s5 = s5[0:18] + windstr.rjust(17," ")
        s6 = visibstr[0:18] + windchildex.rjust(17," ")
        s7 = "DEW   " + dewpoint.rjust(5," ") + " C         " 
        s7 = s7[0:18] + ("UV INDEX " + uv_index + " " + uv_cat).rjust(17," ")
        s8 = ("PRESSURE " + pressure + " KPA AND " + tendency.upper()).center(35," ")

    elif (PageNum == 2):
    
        # ===================== Screen 2 =====================
        # text forecast for 5 days - page 1 of 3
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)  

        # pull text forecasts from env_canada
        wsum_day1 = textwrap.wrap(ec_en_wpg.conditions["text_summary"]["value"].upper(), 35)
        wsum_day2 = textwrap.wrap(ec_en_wpg.daily_forecasts[1]["period"].upper() + ".." + ec_en_wpg.daily_forecasts[1]["text_summary"].upper(), 35)
        wsum_day3 = textwrap.wrap(ec_en_wpg.daily_forecasts[2]["period"].upper() + ".." + ec_en_wpg.daily_forecasts[2]["text_summary"].upper(), 35)
        wsum_day4 = textwrap.wrap(ec_en_wpg.daily_forecasts[3]["period"].upper() + ".." + ec_en_wpg.daily_forecasts[3]["text_summary"].upper(), 35)    
        wsum_day5 = textwrap.wrap(ec_en_wpg.daily_forecasts[4]["period"].upper() + ".." + ec_en_wpg.daily_forecasts[4]["text_summary"].upper(), 35)
        wsum_day6 = textwrap.wrap(ec_en_wpg.daily_forecasts[5]["period"].upper() + ".." + ec_en_wpg.daily_forecasts[5]["text_summary"].upper(), 35)   
        
        # build text_forecast string
        global text_forecast
        text_forecast = wsum_day1 + linebreak + wsum_day2 + linebreak + wsum_day3 + linebreak + wsum_day4 + linebreak + wsum_day5 + linebreak + wsum_day6
    
        # create 8 lines of text
        s1 = "WINNIPEG CITY FORECAST".center(35," ")
        s2 = (text_forecast[0]).center(35," ") if len(text_forecast) >= 1 else " "
        s3 = (text_forecast[1]).center(35," ") if len(text_forecast) >= 2 else " "
        s4 = (text_forecast[2]).center(35," ") if len(text_forecast) >= 3 else " "
        s5 = (text_forecast[3]).center(35," ") if len(text_forecast) >= 4 else " "
        s6 = (text_forecast[4]).center(35," ") if len(text_forecast) >= 5 else " "
        s7 = (text_forecast[5]).center(35," ") if len(text_forecast) >= 6 else " "
        s8 = (text_forecast[6]).center(35," ") if len(text_forecast) >= 7 else " "

    elif (PageNum == 3):
    
        # ===================== Screen 3 =====================
        # text forecast for 5 days - page 2 of 3
        # Screen 1 must run first as it sets up variables
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
        
        # create 8 lines of text
        s1 = "WINNIPEG CITY FORECAST CONT'D".center(35," ")
        s2 = (text_forecast[7]).center(35," ") if len(text_forecast) >= 8 else " "
        s3 = (text_forecast[8]).center(35," ") if len(text_forecast) >= 9 else " "
        s4 = (text_forecast[9]).center(35," ") if len(text_forecast) >= 10 else " "
        s5 = (text_forecast[10]).center(35," ") if len(text_forecast) >= 11 else " "
        s6 = (text_forecast[11]).center(35," ") if len(text_forecast) >= 12 else " "
        s7 = (text_forecast[12]).center(35," ") if len(text_forecast) >= 13 else " "
        s8 = (text_forecast[13]).center(35," ") if len(text_forecast) >= 14 else " " 

    elif (PageNum == 4):
 
        # ===================== Screen 4 =====================
        # text forecast for 5 days - page 3 of 3 -- optional
        # Screen 1 must run first as it sets up variables   
        
        # check if this page is needed
        if len(text_forecast) <= 14:
            debug_msg(("WEATHER_PAGE-display page " + str(PageNum) + " skipped!"),2)
            PageNum = PageNum + 1 #skip this page
            if (PageColour == "#0000A5"): # blue
                PageColour = "#6D0000" # red
            else:
                PageColour = "#0000A5" # blue 
        else:
            debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)   
        
            # create 8 lines of text       
            s1 = "WINNIPEG CITY FORECAST CONT'D".center(35," ")
            s2 = (text_forecast[14]).center(35," ") if len(text_forecast) >= 15 else " "       
            s3 = (text_forecast[15]).center(35," ") if len(text_forecast) >= 16 else " "        
            s4 = (text_forecast[16]).center(35," ") if len(text_forecast) >= 17 else " "
            s5 = (text_forecast[17]).center(35," ") if len(text_forecast) >= 18 else " "
            s6 = (text_forecast[18]).center(35," ") if len(text_forecast) >= 19 else " "
            s7 = (text_forecast[19]).center(35," ") if len(text_forecast) >= 20 else " "
            s8 = (text_forecast[20]).center(35," ") if len(text_forecast) >= 21 else " "                  
    
    elif (PageNum == 5):
    
        # ===================== Screen 5 =====================
        # Weather States
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)        
 
        # weather data 
        temp_cur = str(ec_en_wpg.conditions["temperature"]["value"]) 
        temp_high = str(ec_en_wpg.conditions["high_temp"]["value"])
        temp_low = str(ec_en_wpg.conditions["low_temp"]["value"])
       
        if ("value" in ec_en_wpg.conditions["high_temp_yesterday"] and ec_en_wpg.conditions["high_temp_yesterday"]["value"] != None):    
            temp_yest_high =str(round(ec_en_wpg.conditions["high_temp_yesterday"]["value"]))
        else:
            temp_yest_high = ""
        
        if ("value" in ec_en_wpg.conditions["low_temp_yesterday"] and ec_en_wpg.conditions["low_temp_yesterday"]["value"] != None):    
            temp_yest_low =str(round(ec_en_wpg.conditions["low_temp_yesterday"]["value"]))
        else:
            temp_yest_low = ""       
        
        temp_norm_high =str(ec_en_wpg.conditions["normal_high"]["value"])
        temp_norm_low =str(ec_en_wpg.conditions["normal_low"]["value"])      

        # create 8 lines of text   
        s1 = ("TEMPERATURE STATISTICS FOR WINNIPEG").center(35," ")
        s2 = "       CURRENT " + temp_cur.rjust(5," ") + " C  "
        s3 = ""
        s4 = "                 LOW    HIGH"
        s5 = "        TODAY   " + temp_low.rjust(3," ") + " C  " + temp_high.rjust(3," ") + " C"
        s6 = "    YESTERDAY   " + temp_yest_low.rjust(3," ") + " C  " + temp_yest_high.rjust(3," ") + " C"
        s7 = "       NORMAL   " + temp_norm_low.rjust(3," ") + " C  " + temp_norm_high.rjust(3," ") + " C"
        s8 = ""
    
    elif (PageNum == 6):    
    
        # ===================== Screen 6 =====================
        # Manitoba and Regional Temperatures & Conditions
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)

        day = days[datetime.datetime.today().weekday()]
        month = str(months[(ec_en_wpg.forecast_time.month)])         
        daynum = str(ec_en_wpg.forecast_time.day)
        year = str(ec_en_wpg.forecast_time.year)
 
        temp_brn = str(ec_en_brn.conditions["temperature"]["value"])
        temp_thm = str(ec_en_thm.conditions["temperature"]["value"])
        temp_tps = str(ec_en_tps.conditions["temperature"]["value"])    
        temp_fln = str(ec_en_fln.conditions["temperature"]["value"])  
        temp_chu = str(ec_en_chu.conditions["temperature"]["value"]) 
        temp_ken = str(ec_en_ken.conditions["temperature"]["value"])  
        temp_tby = str(ec_en_tby.conditions["temperature"]["value"])   

        cond_brn = (ec_en_brn.conditions["condition"]["value"]) if ("value" in ec_en_brn.conditions["condition"] and ec_en_brn.conditions["condition"]["value"] != None) else " "
        cond_thm = (ec_en_thm.conditions["condition"]["value"]) if ("value" in ec_en_thm.conditions["condition"] and ec_en_thm.conditions["condition"]["value"] != None) else " "   
        cond_tps = (ec_en_tps.conditions["condition"]["value"]) if ("value" in ec_en_tps.conditions["condition"] and ec_en_tps.conditions["condition"]["value"] != None) else " "
        cond_fln = (ec_en_fln.conditions["condition"]["value"]) if ("value" in ec_en_fln.conditions["condition"] and ec_en_fln.conditions["condition"]["value"] != None) else " "
        cond_chu = (ec_en_chu.conditions["condition"]["value"]) if ("value" in ec_en_chu.conditions["condition"] and ec_en_chu.conditions["condition"]["value"] != None) else " "
        cond_ken = (ec_en_ken.conditions["condition"]["value"]) if ("value" in ec_en_ken.conditions["condition"] and ec_en_ken.conditions["condition"]["value"] != None) else " "
        cond_tby = (ec_en_tby.conditions["condition"]["value"]) if ("value" in ec_en_tby.conditions["condition"] and ec_en_tby.conditions["condition"]["value"] != None) else " "
        
        # create 8 lines of text   
        s1=(real_forecast_date.upper()).center(35," ")
        s2="BRANDON     " + temp_brn.rjust(5," ") + " C    "
        s2= s2[0:20] + word_short(cond_brn,13)[0:13]
        s3="THE PAS     " + temp_tps.rjust(5," ") + " C     "
        s3= s3[0:20] + word_short(cond_tps,13)[0:13]
        s4="FLIN FLON   " + temp_fln.rjust(5," ") + " C     "
        s4= s4[0:20] + word_short(cond_fln,13)[0:13]
        s5="THOMPSON    " + temp_thm.rjust(5," ") + " C     "
        s5= s5[0:20] + word_short(cond_thm,13)[0:13]
        s6="CHURCHILL   " + temp_chu.rjust(5," ") + " C     "
        s6= s6[0:20] + word_short(cond_chu,13)[0:13]
        s7="KENORA      " + temp_ken.rjust(5," ") + " C     "
        s7= s7[0:20] + word_short(cond_ken,13)[0:13]
        s8="THUNDER BAY " + temp_tby.rjust(5," ") + " C     "
        s8= s8[0:20] + word_short(cond_tby,13)[0:13]

    elif (PageNum == 7):
    
        # ===================== Screen 7 =====================
        # Western Canada Temperatures & Conditions       
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2) 
        
        day = days[datetime.datetime.today().weekday()]
        month = str(months[(ec_en_wpg.forecast_time.month)])         
        daynum = str(ec_en_wpg.forecast_time.day)
        year = str(ec_en_wpg.forecast_time.year)
 
        temp_vic = str(ec_en_vic.conditions["temperature"]["value"])
        temp_van = str(ec_en_van.conditions["temperature"]["value"])
        temp_edm = str(ec_en_edm.conditions["temperature"]["value"])    
        temp_cal = str(ec_en_cal.conditions["temperature"]["value"])  
        temp_ssk = str(ec_en_ssk.conditions["temperature"]["value"])  
        temp_reg = str(ec_en_reg.conditions["temperature"]["value"])   
        temp_wht = str(ec_en_wht.conditions["temperature"]["value"]) 

        cond_vic = (ec_en_vic.conditions["condition"]["value"]) if ("value" in ec_en_vic.conditions["condition"] and ec_en_vic.conditions["condition"]["value"] != None) else " "
        cond_van = (ec_en_van.conditions["condition"]["value"])[0:13] if ("value" in ec_en_van.conditions["condition"] and ec_en_van.conditions["condition"]["value"] != None) else " "   
        cond_edm = (ec_en_edm.conditions["condition"]["value"])[0:13] if ("value" in ec_en_edm.conditions["condition"] and ec_en_edm.conditions["condition"]["value"] != None) else " "
        cond_cal = (ec_en_cal.conditions["condition"]["value"])[0:13] if ("value" in ec_en_cal.conditions["condition"] and ec_en_cal.conditions["condition"]["value"] != None) else " "
        cond_ssk = (ec_en_ssk.conditions["condition"]["value"])[0:13] if ("value" in ec_en_ssk.conditions["condition"] and ec_en_ssk.conditions["condition"]["value"] != None) else " "
        cond_reg = (ec_en_reg.conditions["condition"]["value"])[0:13] if ("value" in ec_en_reg.conditions["condition"] and ec_en_reg.conditions["condition"]["value"] != None) else " "
        cond_wht = (ec_en_wht.conditions["condition"]["value"])[0:13] if ("value" in ec_en_wht.conditions["condition"] and ec_en_wht.conditions["condition"]["value"] != None) else " "
        
        # create 8 lines of text    
        s1=(real_forecast_date.upper()).center(35," ")
        s2="VICTORIA    " + temp_vic.rjust(5," ") + " C     "
        s2= s2[0:20] + word_short(cond_vic,13)[0:13]
        s3="VANCOUVER   " + temp_van.rjust(5," ") + " C     "
        s3= s3[0:20] + word_short(cond_van,13)[0:13]
        s4="EDMONTON    " + temp_edm.rjust(5," ") + " C     "
        s4= s4[0:20] + word_short(cond_edm,13)[0:13]
        s5="CALGARY     " + temp_cal.rjust(5," ") + " C     "
        s5= s5[0:20] + word_short(cond_cal,13)[0:13]
        s6="SASKATOON   " + temp_ssk.rjust(5," ") + " C     "
        s6= s6[0:20] + word_short(cond_ssk,13)[0:13]
        s7="REGINA      " + temp_reg.rjust(5," ") + " C     "
        s7= s7[0:20] + word_short(cond_reg,13)[0:13]
        s8="WHITEHORSE  " + temp_wht.rjust(5," ") + " C     "
        s8= s8[0:20] + word_short(cond_wht,13)[0:13]
             
    elif (PageNum == 8):   
    
        # ===================== Screen 8 =====================
        # Eastern Canada Temperatures & Conditions       
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
        
        day = days[datetime.datetime.today().weekday()]
        month = str(months[(ec_en_wpg.forecast_time.month)])         
        daynum = str(ec_en_wpg.forecast_time.day)
        year = str(ec_en_wpg.forecast_time.year)
 
        temp_tor = str(ec_en_tor.conditions["temperature"]["value"])
        temp_otw = str(ec_en_otw.conditions["temperature"]["value"])
        temp_qbc = str(ec_en_qbc.conditions["temperature"]["value"])    
        temp_mtl = str(ec_en_mtl.conditions["temperature"]["value"])  
        temp_frd = str(ec_en_frd.conditions["temperature"]["value"])  
        temp_hal = str(ec_en_hal.conditions["temperature"]["value"])   
        temp_stj = str(ec_en_stj.conditions["temperature"]["value"]) 

        cond_tor = (ec_en_tor.conditions["condition"]["value"]) if ("value" in ec_en_tor.conditions["condition"] and ec_en_tor.conditions["condition"]["value"] != None) else " "
        cond_otw = (ec_en_otw.conditions["condition"]["value"]) if ("value" in ec_en_otw.conditions["condition"] and ec_en_otw.conditions["condition"]["value"] != None) else " "   
        cond_qbc = (ec_en_qbc.conditions["condition"]["value"]) if ("value" in ec_en_qbc.conditions["condition"] and ec_en_qbc.conditions["condition"]["value"] != None) else " "
        cond_mtl = (ec_en_mtl.conditions["condition"]["value"]) if ("value" in ec_en_mtl.conditions["condition"] and ec_en_mtl.conditions["condition"]["value"] != None) else " "
        cond_frd = (ec_en_frd.conditions["condition"]["value"]) if ("value" in ec_en_frd.conditions["condition"] and ec_en_frd.conditions["condition"]["value"] != None) else " "
        cond_hal = (ec_en_hal.conditions["condition"]["value"]) if ("value" in ec_en_hal.conditions["condition"] and ec_en_hal.conditions["condition"]["value"] != None) else " "
        cond_stj = (ec_en_stj.conditions["condition"]["value"]) if ("value" in ec_en_stj.conditions["condition"] and ec_en_stj.conditions["condition"]["value"] != None) else " "
        
        # create 8 lines of text    
        s1=(real_forecast_date.upper()).center(35," ")
        s2="TORONTO     " + temp_tor.rjust(5," ") + " C    "
        s2= s2[0:20] + word_short(cond_tor,13)[0:13]
        s3="OTTAWA      " + temp_otw.rjust(5," ") + " C     "
        s3= s3[0:20] + word_short(cond_otw,13)[0:13]
        s4="QUEBEC CITY " + temp_qbc.rjust(5," ") + " C     "
        s4= s4[0:20] + word_short(cond_qbc,13)[0:13]
        s5="MONTREAL    " + temp_mtl.rjust(5," ") + " C     "
        s5= s5[0:20] + word_short(cond_mtl,13)[0:13]
        s6="FREDERICTON " + temp_frd.rjust(5," ") + " C     "
        s6= s6[0:20] + word_short(cond_frd,13)[0:13]
        s7="HALIFAX     " + temp_hal.rjust(5," ") + " C     "
        s7= s7[0:20] + word_short(cond_hal,13)[0:13]
        s8="ST.JOHN'S   " + temp_stj.rjust(5," ") + " C     "
        s8= s8[0:20] + word_short(cond_stj,13)[0:13]
    
    elif (PageNum == 9):
        
        # ===================== Screen 9 =====================
        # hourly forecast
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)
 
        # get local timezone to show on screen
        local_tz = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
 
        # convert hourly forecast data in 2 hour intervals to lists
        hrly_period = [ec_en_wpg.hourly_forecasts[0]["period"], ec_en_wpg.hourly_forecasts[2]["period"], ec_en_wpg.hourly_forecasts[4]["period"], ec_en_wpg.hourly_forecasts[6]["period"],
            ec_en_wpg.hourly_forecasts[8]["period"], ec_en_wpg.hourly_forecasts[10]["period"], ec_en_wpg.hourly_forecasts[12]["period"] ]
        hrly_temp = [ec_en_wpg.hourly_forecasts[0]["temperature"], ec_en_wpg.hourly_forecasts[2]["temperature"], ec_en_wpg.hourly_forecasts[4]["temperature"], ec_en_wpg.hourly_forecasts[6]["temperature"],
            ec_en_wpg.hourly_forecasts[8]["temperature"], ec_en_wpg.hourly_forecasts[10]["temperature"], ec_en_wpg.hourly_forecasts[12]["temperature"] ]   
        hrly_cond= [str(ec_en_wpg.hourly_forecasts[0]["condition"]), str(ec_en_wpg.hourly_forecasts[2]["condition"]), str(ec_en_wpg.hourly_forecasts[4]["condition"]), 
            str(ec_en_wpg.hourly_forecasts[6]["condition"]), str(ec_en_wpg.hourly_forecasts[8]["condition"]), str(ec_en_wpg.hourly_forecasts[10]["condition"]), 
            str(ec_en_wpg.hourly_forecasts[12]["condition"]) ]              
        
        # convert period to local time
        hrly_period_local = list(map(lambda x: x.astimezone(), hrly_period))

        # convert conditions to upper caps
        # hrly_cond_cap = list(map(str.upper, hrly_cond))
        
        for i in range(len(hrly_cond)):
            hrly_cond[i] = word_short(hrly_cond[i],13)
            
        
        # create 8 lines of text           
        s1 = ("WINNIPEG HOURLY FORECAST").center(35," ")
        s2 = "" + (str(hrly_period_local[0].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[0])).rjust(3," ") + " C  " + hrly_cond[0][0:13]
        s3 = "" + (str(hrly_period_local[1].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[1])).rjust(3," ") + " C  " + hrly_cond[1][0:13]
        s4 = "" + (str(hrly_period_local[2].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[2])).rjust(3," ") + " C  " + hrly_cond[2][0:13]
        s5 = "" + (str(hrly_period_local[3].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[3])).rjust(3," ") + " C  " + hrly_cond[3][0:13]
        s6 = "" + (str(hrly_period_local[4].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[4])).rjust(3," ") + " C  " + hrly_cond[4][0:13]
        s7 = "" + (str(hrly_period_local[5].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[5])).rjust(3," ") + " C  " + hrly_cond[5][0:13]
        s8 = "" + (str(hrly_period_local[6].strftime("%-I:%M %p"))).rjust(8," ") + " " + str(local_tz) + "  " + (str(hrly_temp[6])).rjust(3," ") + " C  " + hrly_cond[6][0:13]
    
    elif (PageNum == 10):

        # ===================== Screen 10 =====================
        # preciptation page
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)        
    
        wpg_precip = (str(ec_en_wpg.conditions["pop"]["value"]) + " %") if ec_en_wpg.conditions["pop"] and ec_en_wpg.conditions["pop"]["value"] != None else "NIL"
        brn_precip = (str(ec_en_brn.conditions["pop"]["value"]) + " %") if ec_en_brn.conditions["pop"] and ec_en_brn.conditions["pop"]["value"] != None else "NIL"
        tps_precip = (str(ec_en_tps.conditions["pop"]["value"]) + " %") if ec_en_tps.conditions["pop"] and ec_en_tps.conditions["pop"]["value"] != None else "NIL"
        fln_precip = (str(ec_en_fln.conditions["pop"]["value"]) + " %") if ec_en_fln.conditions["pop"] and ec_en_fln.conditions["pop"]["value"] != None else "NIL"
        thm_precip = (str(ec_en_thm.conditions["pop"]["value"]) + " %") if ec_en_thm.conditions["pop"] and ec_en_thm.conditions["pop"]["value"] != None else "NIL"
        chu_precip = (str(ec_en_chu.conditions["pop"]["value"]) + " %") if ec_en_chu.conditions["pop"] and ec_en_chu.conditions["pop"]["value"] != None else "NIL"
        yest_precip = (str(ec_en_wpg.conditions["precip_yesterday"]["value"]) + " MM") if ec_en_wpg.conditions["precip_yesterday"] and ec_en_wpg.conditions["precip_yesterday"]["value"] != None else "0.0 MM"
    
        # create 8 lines of text   
        s1 = ("MANITOBA PRECIPITATION FORECAST").center(35," ")
        s2 = "    TODAY WINNIPEG  " + (wpg_precip).rjust(5," ")
        s3 = "          BRANDON   " + (brn_precip).rjust(5," ")
        s4 = "          THE PAS   " + (tps_precip).rjust(5," ")
        s5 = "          FLIN FLON " + (fln_precip).rjust(5," ")
        s6 = "          THOMPSON  " + (thm_precip).rjust(5," ")
        s7 = "          CHURCHILL " + (chu_precip).rjust(5," ")
        s8 = " PREV DAY WINNIPEG  " + (yest_precip).rjust(7," ")

    elif (PageNum == 11):    
        
        # ===================== Screen 11 =====================
        # custom/extra page - currently used for my channel listing
        # to disable this page, set PageTotal to 10
        debug_msg(("WEATHER_PAGE-display page " + str(PageNum)),2)         
      
        # create 8 lines of text

        s1 = "==========CHANNEL LISTING=========="
        s2 = "  2 SIMPSNS  13.1 CITY    50 SECUR"    
        s3 = "3.1 CBC FR.    14 90sTV   54 COMEDY" 
        s4 = "  6 60s/70s    16 TOONS   61 MUSIC"         
        s5 = "6.1 CBC        22 GLOBAL  64 WEATHR"
        s6 = "7.1 CTV        24 80sTV"
        s7 = "9.1 GLOBAL   35.1 FAITH"
        s8 = " 10 CBC        45 CHROMECAST" 

    # create the canvas for middle page text

    weather = Canvas(root, height=310, width=720, bg=PageColour)
    weather.place(x=0, y=85)
    weather.config(highlightbackground=PageColour)
    
    # place the 8 lines of text
    weather.create_text(80, 17, anchor='nw', text=s1, font=('VCR OSD Mono', 21, "bold"), fill="white")
    weather.create_text(80, 60, anchor='nw', text=s2, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 95, anchor='nw', text=s3, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 130, anchor='nw', text=s4, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 165, anchor='nw', text=s5, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 200, anchor='nw', text=s6, font=('VCR OSD Mono', 21,), fill="white")
    weather.create_text(80, 235, anchor='nw', text=s7, font=('VCR OSD Mono', 21,), fill="white") 
    weather.create_text(80, 270, anchor='nw', text=s8, font=('VCR OSD Mono', 21,), fill="white") 
    
    # Toggle Page Colour between Red & Blue
    if (PageColour == "#00006D"): # blue
        PageColour = "#6D0000" # red
    else:
        PageColour = "#00006D" # blue
        
    # Increment Page Number or Reset
    if (PageNum < PageTotal):
        PageNum = PageNum + 1
    elif (PageNum >= PageTotal):
        PageNum = 1
    
    root.after(20000, weather_page, PageColour, PageNum) # re-run every 20sec from program launch

# DEF update weather for all cities
def weather_update(group):

        global real_forecast_time
        global real_forecast_date
        global real_forecast_month
        global real_forecaste_year

        # used to calculate update time
        t1 = datetime.datetime.now().timestamp() # record current timestamp
        timechk = t1 - updt_tstp[group] # compare timestamp vs last update time -- not used for group 0 (initialize mode)
        
        if (timechk  > 1800) or (group == 0): #check if 30min has elapsed since last group update, but always allow group 0 updates (initial refresh)
            # update weather for cities, depending on group number requested. 0 == initial refresh on launch
            if (group == 0 or group == 1):
                asyncio.run(ec_en_wpg.update())
                asyncio.run(ec_en_brn.update()) 
                asyncio.run(ec_en_thm.update()) 
                asyncio.run(ec_en_tps.update()) 
                asyncio.run(ec_en_fln.update()) 
                asyncio.run(ec_en_chu.update()) 
                asyncio.run(ec_en_ken.update()) 
                asyncio.run(ec_en_tby.update())
                real_forecast_time = time.strftime("%-I %p") # this is used as the forecast time when showing the weather. for some reason the dictionary was always reporting 22:00 for forecast time
                if real_forecast_time == "12 PM": 
                    real_forecast_time = "NOON" # just to add some fun
                real_forecast_date = datetime.datetime.now().strftime("%a %b %d/%Y")# this is used as the forecast time when showing the weather. dictionary from env_canada reports weird (GMT maybe?)
                    
                if group == 0:
                    updt_tstp[1] = datetime.datetime.now().timestamp() # record timestamp to update
                    updt_tstp[2] = datetime.datetime.now().timestamp() # record timestamp to update
                    updt_tstp[3] = datetime.datetime.now().timestamp() # record timestamp to update
                else:
                    updt_tstp[group] = datetime.datetime.now().timestamp() # record timestamp to update
                
            if (group == 0 or group == 2):
                asyncio.run(ec_en_vic.update()) 
                asyncio.run(ec_en_van.update()) 
                asyncio.run(ec_en_edm.update()) 
                asyncio.run(ec_en_cal.update()) 
                asyncio.run(ec_en_ssk.update()) 
                asyncio.run(ec_en_reg.update()) 
                asyncio.run(ec_en_wht.update()) 
                real_forecast_date = datetime.datetime.now().strftime("%a %b %d/%Y")# this is used as the forecast time when showing the weather. dictionary from env_canada reports weird (GMT maybe?)
                if group == 0:
                    updt_tstp[1] = datetime.datetime.now().timestamp() # record timestamp to update
                    updt_tstp[2] = datetime.datetime.now().timestamp() # record timestamp to update
                    updt_tstp[3] = datetime.datetime.now().timestamp() # record timestamp to update
                else:
                    updt_tstp[group] = datetime.datetime.now().timestamp() # record timestamp to update
        
            if (group == 0 or group == 3):
                asyncio.run(ec_en_tor.update()) 
                asyncio.run(ec_en_otw.update()) 
                asyncio.run(ec_en_qbc.update()) 
                asyncio.run(ec_en_mtl.update()) 
                asyncio.run(ec_en_frd.update()) 
                asyncio.run(ec_en_hal.update()) 
                asyncio.run(ec_en_stj.update()) 
                real_forecast_date = datetime.datetime.now().strftime("%a %b %d/%Y")# this is used as the forecast time when showing the weather. dictionary from env_canada reports weird (GMT maybe?)
                if group == 0:
                    updt_tstp[1] = datetime.datetime.now().timestamp() # record timestamp to update
                    updt_tstp[2] = datetime.datetime.now().timestamp() # record timestamp to update
                    updt_tstp[3] = datetime.datetime.now().timestamp() # record timestamp to update
                else:
                    updt_tstp[group] = datetime.datetime.now().timestamp() # record timestamp to update

            # calculate time it took to update
            t = datetime.datetime.now().timestamp() - t1 # used to report how long update took for debug print lines
            debug_msg(("WEATHER_UPDATE-weather group " + str(group) + " updated in " + str(round(t,2)) + " seconds"),1)
        else:
            debug_msg(("WEATHER_UPDATE-weather group " + str(group) + " not updated. only ~" + str(round(timechk//60)) + " minutes elapsed out of required 30"),1)

# DEF bottom marquee scrolling text
def bottom_marquee(grouptotal):

    group = 1

    # scrolling text canvas
    marquee = Canvas(root, height=120, width=580, bg="green")
    marquee.config(highlightbackground="green")
    marquee.place(x=80, y=400)

    # read in RSS data and prepare it
    width = 35
    pad = ""
    for r in range(width): #create an empty string of 35 characters
        pad = pad + " " 

    url = "https://winnipeg.ctvnews.ca/rss/winnipeg"
    wpg = feedparser.parse(url)
    debug_msg("BOTTOM_MARQUEE-RSS feed refreshed",1)

    # Add first entry to string without padding
    wpg_desc = pad + wpg.entries[0]["description"]
    
    # Append all other RSS entry descriptions, with 35 character padding in between
    for n in range(len(wpg.entries)):
        if (n == 0) or ((len(wpg_desc + pad + wpg.entries[n]["description"]) * 24) >= 31000): # avoid duplicate first entry / check if string will be max pixels allowed
            n = n + 1
        else:
            wpg_desc = wpg_desc + pad + wpg.entries[n]["description"]
    
    # convert to upper case
    mrq_msg = wpg_desc.upper()

    # use the length of the news feeds to determine the total pixels in the scrolling section
    marquee_length = len(mrq_msg)
    pixels = marquee_length * 24 # roughly 24px per char

    # setup scrolling text
    text = marquee.create_text(1, 2, anchor='nw', text=pad + mrq_msg + pad, font=('VCR OSD Mono', 25,), fill="white")

    restart_marquee = True # 
    while restart_marquee:
        restart_marquee = False
        debug_msg("BOTTOM_MARQUEE-starting RSS display",1)
        for p in range(pixels+730):
            marquee.move(text, -1, 0) #shift the canvas to the left by 1 pixel
            marquee.update()
            time.sleep(0.002) # scroll every 2ms
            if (p == pixels+729): # once the canvas has finished scrolling
                restart_marquee = True
                marquee.move(text, pixels+729, 0) # reset the location
                if (group <= grouptotal):
                    debug_msg("BOTTOM_MARQUEE-launching weather update",1)
                    try:
                        weather_update(group) # update weather information between RSS scrolls
                        debug_msg("BOTTOM_MARQUEE-weather info refreshed",1)
                        group = group + 1
                    except:
                        debug_msg("BOTTOM_MARQUEE-ENV_CANADA_ERROR! weather info NOT refreshed",1)
                else:
                    debug_msg("BOTTOM_MARQUEE-launching weather update",1)
                    group = 1
                    try:
                        weather_update(group) # update weather information between RSS scrolls
                        debug_msg("BOTTOM_MARQUEE-weather info refreshed",1)
                        group = group + 1
                    except:
                        debug_msg("BOTTOM_MARQUEE-ENV_CANADA_ERROR! weather info NOT refreshed",1)
                    
                p = 0 # keep the for loop from ending
                wpg = feedparser.parse(url)
                debug_msg("BOTTOM_MARQUEE-RSS feed refreshed",1)

# DEF generate playlist from folder
def playlist_generator(musicpath):

    # this code from https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    # create a list of file and sub directories 
    # names in the given directory 

    debug_msg("PLAYLIST_GENERATOR-searching for music files...",1)
    filelist = os.listdir(musicpath)
    allFiles = list()
    # Iterate over all the entries    
    for entry in filelist:
        # Create full path
        fullPath = os.path.join(musicpath,entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + playlist_generator(fullPath)
        else:
            allFiles.append(fullPath)
    debug_msg(("PLAYLIST_GENERATOR-found " + str(len(allFiles))),1)
    return allFiles

# DEF play background music
def music_player(songNumber, playlist, musicpath):

    # make sure musicpath ONLY contains playable mp3 files. this does not check if files are valid and will crash if it tries to play something else

    if ((pygame.mixer.music.get_busy() == False) and (songNumber < len(playlist))):
        debug_msg(("MUSIC_PLAYER-playing song " + playlist[songNumber]),1)
        pygame.mixer.music.load(playlist[songNumber])
        pygame.mixer.music.play(loops = 0)
        songNumber = songNumber + 1
    elif ((pygame.mixer.music.get_busy() == False) and (songNumber >= len(playlist))):
        debug_msg("MUSIC_PLAYER-playlist complete,re-shuffling... ",1)
        songNumber = 0
        random.shuffle(playlist)   

    root.after(2000, music_player, songNumber, playlist, musicpath) # re-run every 2sec from program launch

# DEF Word Shortner 5000 
def word_short(phrase, length):
    
    # dictionary of shortened words
    dict = {                    
        "BECOMING" : "BCMG",
        "SCATTERED" : "SCTD",
        "PARTLY" : "PTLY",
        "SHOWER" : "SHWR",
        "CLOUDY" : "CLDY",
        "DRIZZLE" : "DRZLE",
        "FREEZING" : "FRZG",
        "THUNDERSHOWER" : "THNDSHR",
        "THUNDERSTORM" : "THNDSTM",
        "PRECIPITATION" : "PRECIP",
        "CHANCE" : "CHNCE",
        "DEVELOPING" : "DVLPNG",
        "WITH" : "W",
        "SHOWER" : "SHWR",
        "LIGHT" : "LT",
        "HEAVY" : "HVY",
        "BLOWING" : "BLWNG"
    }
    
    phrase = phrase.upper() # convert to upper case for convenience and for later
    
    if len(phrase) > length:    # check if phrase is too long
        
        if phrase == "A MIX OF SUN AND CLOUD":  # just for this specific condition
            phrase = "SUN CLOUD MIX"
        
        for key, value in dict.items():     # replace words using dictionary dict
            phrase = (re.sub(key, value, phrase))  
        
        debug_msg(("WORD_SHORT-phrase shortened to " + phrase),2)        
        return phrase
        
    else:
        return phrase       # if length is fine, do nothing and send it back

# DEF debug messenger
def debug_msg(message, priority):

    debugmode = 1;
    # 0 = disabled
    # 1 = normal (priority 1)
    # 2 = verbose (priority 2)
    
    timestamp = 2;
    # 0 = no date/time - Why would you ever want this? Enjoy!
    # 1 = time only
    # 2 = date & time
    
    # date/time string data
    if (timestamp == 1):
        timestr = time.strftime("%H:%M.")
    elif (timestamp == 2):
        timestr = time.strftime("%Y%m%d-%H:%M.")
    else:
        timestr = ""
        
    # print debug message based on debug mode
    if ((debugmode > 0) and (priority <= debugmode)):
        print(timestr + prog + "." + ver + "." + message)

# ROOT main stuff

# setup root
root = Tk()
root.attributes('-fullscreen',True)
root.geometry("720x480") # this must be 720x480 for a proper filled out screen on composite output. 640x480 will have black bar on RH side. use 720x576 for PAL.
root.config(cursor="none", bg="green")
root.wm_title("wpg-weatherchan")

# Clock - Top RIGHT
# this got complicated due to the new font (7-Segment Normal), which doesn't have proper colon(:) char, 
# so I've removed the colon from the time string and added them on top using VCR OSD Mono
debug_msg("ROOT-placing clock",1)
timeText = Label(root, text="", font=("7-Segment Normal", 22), fg="white", bg="green")
timeText.place(x=403, y=40)
timeColon1 = Label(root, text=":", font=("VCR OSD Mono", 32), fg="white", bg="green")
timeColon1.place(x=465, y=36)
timeColon2 = Label(root, text=":", font=("VCR OSD Mono", 32), fg="white", bg="green")
timeColon2.place(x=560, y=36)
debug_msg("ROOT-launching clock updater",1)
clock()

# Title - Top LEFT
debug_msg("ROOT-placing Title Text",1)
Title = Label(root, text="ENVIRONMENT CANADA", font=("VCR OSD Mono", 22, "bold"), fg="white", bg="green")
Title.place(x=80, y=40)

# use ECWeather to gather weather data, station_id is from the csv file provided with ECDada -- homepage: https://github.com/michaeldavie/env_canada

# group 1
ec_en_wpg = ECWeather(station_id='MB/s0000193', language='english')
ec_en_brn = ECWeather(station_id='MB/s0000492', language='english')
ec_en_thm = ECWeather(station_id='MB/s0000695', language='english')
ec_en_tps = ECWeather(station_id='MB/s0000644', language='english')
ec_en_chu = ECWeather(station_id='MB/s0000779', language='english')
ec_en_fln = ECWeather(station_id='MB/s0000015', language='english')
ec_en_ken = ECWeather(station_id='ON/s0000651', language='english')
ec_en_tby = ECWeather(station_id='ON/s0000411', language='english')

# group 2
ec_en_vic = ECWeather(station_id='BC/s0000775', language='english')
ec_en_van = ECWeather(station_id='BC/s0000141', language='english')
ec_en_edm = ECWeather(station_id='AB/s0000045', language='english')
ec_en_cal = ECWeather(station_id='AB/s0000047', language='english')
ec_en_ssk = ECWeather(station_id='SK/s0000797', language='english')
ec_en_reg = ECWeather(station_id='SK/s0000788', language='english')
ec_en_wht = ECWeather(station_id='YT/s0000825', language='english')

# group 3
ec_en_tor = ECWeather(station_id='ON/s0000458', language='english')
ec_en_otw = ECWeather(station_id='ON/s0000430', language='english')
ec_en_mtl = ECWeather(station_id='QC/s0000635', language='english')
ec_en_qbc = ECWeather(station_id='QC/s0000620', language='english')
ec_en_frd = ECWeather(station_id='NB/s0000250', language='english')
ec_en_hal = ECWeather(station_id='NS/s0000318', language='english')
ec_en_stj = ECWeather(station_id='NL/s0000280', language='english')

# total number of groups broken up to update sections of weather data, to keep update time short
grouptotal = 3 

# create time check updated list for weather_udpdate
updt_tstp = [0,0,0,0]

# create string to store hour that weather was updated. Use this to show "forecast time" since ec_en_wpg.forecast_time always reports the same time!! Date is also weird
real_forecast_time = ""
real_forecast_date = ""

# Update Weather Information
debug_msg("ROOT-launching weather update",1)
weather_update(0) # update all cities

# Middle Section (Cycling weather pages, every 30sec)
debug_msg("ROOT-launching weather_page",1)
PageColour = "00006D" # blue
PageNum = 1
weather_page(PageColour, PageNum)

# Generate background music playlist
debug_msg("ROOT-launching playlist generator",1)
musicpath = "/home/probnot/WeatherPi/music" # must show full path
playlist = playlist_generator(musicpath) # generate playlist array
random.shuffle(playlist) # shuffle playlist

# Play background music on shuffle using pygame
debug_msg("ROOT-launching background music",1)
songNumber = 1
pygame.mixer.init()
music_player(songNumber, playlist, musicpath)

# Bottom Scrolling Text (City of Winnipeg RSS Feed)
debug_msg("ROOT-launching bottom_marquee",1)
bottom_marquee(grouptotal)

# loop program  
root.mainloop()