# encoding=utf8
# -*- coding: utf-8 -*-


import codecs
import os
import pprint
from apixu.client import ApixuClient, ApixuException
from weatherConditions import *


####################
# Variables
####################

api_key = '1a81c76803d14b50bec145925180309'
client = ApixuClient(api_key)

parsedDate = []
parsedHumidity = []
parsedMaxTemp = []
parsedMinTemp = []
parsedWeatherDesc = []
parsedShortDesc = []
parsedWeatherCode = []
parsedWeatherIcon = []
parsedMaxWind = []
parsedTotalPrecip = []
parsedUV = []
parsedSunrise = []
parsedSunset = []

pngTemplate = '/mnt/us/kindle_weather/weather_template.png'
pngTextTmp = '/mnt/us/kindle_weather/weather_text_tmp.png'
pngOutput = '/mnt/us/kindle_weather/weather_output.png'
fontDefault = '/mnt/us/kindle_weather/DejaVuSans-Bold.ttf'
iconsFolder = '/mnt/us/kindle_weather/icons'
binConvert = '/mnt/us/linkss/bin/convert'

location = 'London'
forecastDays = 4

debugMode = False


####################
# Main
####################

# Obtain forecast dictionary
parsedForecast = client.getForecastWeather(q=location, days=forecastDays)

# if debugMode:
#      pp = pprint.PrettyPrinter(indent=4)
#      pp.pprint(parsedForecast)

i = 0
for key in parsedForecast['forecast']['forecastday']:
    parsedDate.append(          parsedForecast['forecast']['forecastday'][i]['date'])
    parsedHumidity.append(parsedForecast['forecast']['forecastday'][i]['day']['avghumidity'])
    parsedWeatherCode.append(   parsedForecast['forecast']['forecastday'][i]['day']['condition']['code'])
    parsedWeatherDesc.append(   parsedForecast['forecast']['forecastday'][i]['day']['condition']['text'])
    parsedMaxTemp.append(       parsedForecast['forecast']['forecastday'][i]['day']['maxtemp_c'])
    parsedMinTemp.append(       parsedForecast['forecast']['forecastday'][i]['day']['mintemp_c'])
    parsedMaxWind.append(       parsedForecast['forecast']['forecastday'][i]['day']['maxwind_kph'])
    parsedTotalPrecip.append(   parsedForecast['forecast']['forecastday'][i]['day']['totalprecip_mm'])
    parsedUV.append(            parsedForecast['forecast']['forecastday'][i]['day']['uv'])
    parsedSunrise.append(       parsedForecast['forecast']['forecastday'][i]['astro']['sunrise'])
    parsedSunset.append(        parsedForecast['forecast']['forecastday'][i]['astro']['sunset'])
    parsedWeatherIcon.append(   iconsFolder + '/' + conditions[str(parsedWeatherCode[i])])
    parsedShortDesc.append(     shortDesc[str(parsedWeatherCode[i])])

    if debugMode:
        print('Index:', i,
              ' Date:', parsedDate[i],
              ' Humidity:', parsedHumidity[i],
              ' Weather Code:', parsedWeatherCode[i],
              ' Weather Text:', parsedWeatherDesc[i],
              ' weather shot text:', parsedShortDesc[i],
              ' Max Temp:', parsedMaxTemp[i],
              ' Min Temp:', parsedMinTemp[i],
              ' Max Wind:', parsedMaxWind[i],
              ' Total Precip:', parsedTotalPrecip[i],
              ' UV:', parsedUV[i],
              ' Sunrise:', parsedSunrise[i],
              ' Sunset:', parsedSunset[i],
              ' Icon:', parsedWeatherIcon[i])

    i+=1


####################
# Process PNG
####################

# Convert svg icons to png
#for i in *.svg ; do convert "$i" -resize 102x102 "${i%.*}_small.png" ; done

# Add icons to template
os.system(binConvert + ' ' + pngTemplate + " " + parsedWeatherIcon[0] + "_large.png" + " -geometry +396+15 -composite " + pngOutput)
os.system(binConvert + ' ' + pngOutput + " " + parsedWeatherIcon[1] + "_small.png" + " -geometry +49+210 -composite " + pngOutput)
os.system(binConvert + ' ' + pngOutput + " " + parsedWeatherIcon[2] + "_small.png" + " -geometry +249+210 -composite " + pngOutput)
os.system(binConvert + ' ' + pngOutput + " " + parsedWeatherIcon[3] + "_small.png" + " -geometry +449+210 -composite " + pngOutput)

# Add dates to template
os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 25 label:"Today ' + parsedDate[0][8:] + '/' + parsedDate[0][5:-3] + '/' + parsedDate[0][0:-6] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +20+10 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + parsedDate[1][8:] + '/' + parsedDate[1][5:-3] + '/' + parsedDate[1][0:-6] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +20+324 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + parsedDate[2][8:] + '/' + parsedDate[2][5:-3] + '/' + parsedDate[2][0:-6] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +220+324 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + parsedDate[3][8:] + '/' + parsedDate[3][5:-3] + '/' + parsedDate[3][0:-6] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +420+324 -composite " + pngOutput)

# Add weather zero
os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + parsedShortDesc[0] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +120+54 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + str(parsedMaxTemp[0]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +85+79 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + str(parsedMinTemp[0]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +85+104 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + str(parsedHumidity[0]) + '%" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +85+129 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + str(parsedMaxWind[0]) + 'kph" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +85+154 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + str(parsedTotalPrecip[0]) + 'mm" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +275+79 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + str(parsedUV[0]) + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +275+104 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + parsedSunrise[0] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +275+129 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 19 label:"' + parsedSunset[0] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +275+154 -composite " + pngOutput)

# Add weather one
os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + parsedShortDesc[1] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +20+361 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMaxTemp[1]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +80+379 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMinTemp[1]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +80+397 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedHumidity[1]) + '%" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +80+415 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMaxWind[1]) + 'kph" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +80+433 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedTotalPrecip[1]) + 'mm" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +80+451 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedUV[1]) + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +80+469 -composite " + pngOutput)

# Add weather two
os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + parsedShortDesc[2] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +220+361 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMaxTemp[2]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +280+379 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMinTemp[2]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +280+397 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedHumidity[2]) + '%" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +280+415 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMaxWind[2]) + 'kph" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +280+433 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedTotalPrecip[2]) + 'mm" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +280+451 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedUV[2]) + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +280+469 -composite " + pngOutput)

# Add weather three
os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + parsedShortDesc[3] + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +420+361 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMaxTemp[3]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +480+379 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMinTemp[3]) + '°C" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +480+397 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedHumidity[3]) + '%" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +480+415 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedMaxWind[3]) + 'kph" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +480+433 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedTotalPrecip[3]) + 'mm" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +480+451 -composite " + pngOutput)

os.system(binConvert + ' -gravity West -background "rgba(0,0,0,0.0)" -fill black -font ' + fontDefault + ' -density 96 -pointsize 15 label:"' + str(parsedUV[3]) + '" ' + pngTextTmp)
os.system(binConvert + ' ' +  pngOutput + " " + pngTextTmp + " -geometry +480+469 -composite " + pngOutput)

#y-fontSize-3
