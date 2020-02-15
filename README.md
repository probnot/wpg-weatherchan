# wpg-weatherchan
This creates the old-school looking weather channel that was common on Winnipeg cable TV into the 1990s.

## Usage

This was written in Python 3.x

This uses 'ECData' from env_canada to get the weather data from Environment Canada. It can be found here: (https://github.com/michaeldavie/env_canada). It also  uses the font VCR OSD Mono (https://www.dafont.com/vcr-osd-mono.font).

It was tested on a Raspberry Pi 3, but should run on other models as well. Because it uses tkinter, it must be launched from the GUI in raspbian. I recommend disabling screenblank, and turning on overscan for best results.

If you're launching this from an SSH session, I recommend doing so through a script file with the following:
>export DISPLAY=:0.0

>python3 wpg-weatherchan.py

## License

This code is available under the terms of the [MIT License]
