Porpose: print on Kindle 3's screen a png with clock and weather information.


INSTALLATION:

Step 1: Copy kindle_weather folder in kindle's folder /mnt/us.

Step 2: To start the displaying of the clock and weather, create a file named "start_kindle_weather.ini" inside folder /mnt/us/launchpad. Write this text inside:

[Actions]
C = !sh /mnt/us/kindle_weather/start_stop.sh &

Step 3: Setup cron to parse the weather every 6h and update the screen every 1m. Append the following lines to /etc/crontab/root:

* * * * * sh /mnt/us/kindle_weather/time_update.sh
0 */6 * * * /mnt/us/python/bin/python2.7 /mnt/us/kindle_weather/get_weather.py

Step 4: login to www.apixu.com and optain a free api key. Add the api key to line 16 of file get_weather.py.

Step 5: Change weather location editing line 40 of file get_weather.py. Check on apixu websize for possilbe options as city or postcode.

step 6: run the following command from terminal (in my case a restart was required due to cron)
/etc/init.d/cron restart
/etc/init.d/launchpad restart

HOW TO USE:

Press shift + c to start the scripts and hope for the best.
