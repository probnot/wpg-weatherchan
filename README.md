# wpg-weatherchan
This creates the old-school looking weather channel that was common on Winnipeg cable TV into the 1990s.

![Example of the result, captured from the analog video output](https://github.com/probnot/wpg-weatherchan/blob/master/example1.jpg?raw=true)
![Example of the result, captured from the analog video output](https://github.com/probnot/wpg-weatherchan/blob/master/example2.jpg?raw=true)

## Usage

This was written in Python 3.x

This uses 'ECData' from env_canada to get the weather data from Environment Canada. It can be found here: (https://github.com/michaeldavie/env_canada). 
It also uses the fonts VCR OSD Mono (https://www.dafont.com/vcr-osd-mono.font) and 7-Segment Normal (https://blogfonts.com/7-segment-normal.font).

It was tested on a Raspberry Pi 3 running Raspberry Pi OS (full w/desktop). I recommend the model 3 or higher. Because it uses tkinter, it must be launched from the GUI in raspbian. I recommend disabling screenblank, and turning on overscan for best results.

The Composite video output in the Raspberry Pi runs at 720x480, so I recommend setting the display to this and not 640x480 (which added a black bar on the side for me).

If you're launching this from an SSH session, I recommend doing so through a script file with the following:
>export DISPLAY=:0.0
>
>python3 wpg-weatherchan.py

To launch automatically, create a file in /etc/xdg/autostart/ called "display.desktop" with the following contents (replace my filepath with whatever your location is):
>[Desktop Entry]
>
>Name=WeatherPi
>
>Exec=/usr/bin/python3 /home/probnot/WeatherPi/wpg-weatherchan.py

## License

This code is available under the terms of the [MIT License]
