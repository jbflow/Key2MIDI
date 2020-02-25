# Key2MIDI
A small Python application for converting keystrokes (a-h) into MIDI CC or Note messages and sending them into a designated MIDI port, this message can also be triggered by a GUI button. I originally created this to test some MIDI remote scripts I've been writing for Ableton Live. It enables testing without needing to plug a MIDI controller in, using a simple python script over IAC instead. It can also be used for mapping or testing just about anything to do with MIDI. 

I decided to build a GUI for it using tkinter, this was my first attempt at this to learn how to do the process, as well as packaging python programs using py2app. There is a packaged .app file that's been tested on Sierra and newer.

At the moment it is macOS only but I will be making it compatible for Windows fairly soon.

The python script requires rtmidi with "pip install python-rtmidi".

I was using pynput and keyboard modules to listen for global keyboard events but this caused issues when converting to an app due it needing to be run with root permissions. The keyboard events are being handled using tkinter bind methods in this version.

## To Do:
1. Port to Windows
2. Add/Remove message rows
3. Add Program Change and SysEx functionality
4. Find a way of getting input monitoring permissions (for pynput)
5. Find a better way of writing GUI's (tkinter is simple and fast, but colour issues are frustrating)
