#!/bin/bash

# if the Kindle is not being used as clock, then just quit
test -f /mnt/us/kindle_weather/clockisticking || exit


# find the current minute of the day
MinuteOTheDay="$(env TZ=UTC-1 date -R +"%H%M")";

# check if there is at least one image for this minute 
lines="$(find /mnt/us/kindle_weather/clock_images/quote_$MinuteOTheDay* 2>/dev/null | wc -l)"
if [ $lines -eq 0 ]; then
	echo 'no images found for '$MinuteOTheDay
	exit
else
	echo $lines' files found for '$MinuteOTheDay
fi


# randomly pick a png file for that minute (since we have multiple for some minutes)
ThisMinuteImage=$( find /mnt/us/kindle_weather/clock_images/quote_$MinuteOTheDay* 2>/dev/null | python -c "import sys; import random; print(''.join(random.sample(sys.stdin.readlines(), int(sys.argv[1]))).rstrip())" 1)

echo $ThisMinuteImage > /mnt/us/kindle_weather/clockisticking

# Merge ThisMinuteImage to weather image
#/mnt/us/linkss/bin/convert  /mnt/us/client_weather/weather_output.svg -resize 600x400 /mnt/us/client_weather/weather_output.png
/mnt/us/linkss/bin/convert -append $ThisMinuteImage /mnt/us/kindle_weather/weather_output.png  /mnt/us/kindle_weather/final.png

# clear the screen
eips -c

# show that image
eips -g /mnt/us/kindle_weather/final.png
