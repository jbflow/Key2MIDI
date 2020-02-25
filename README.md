# Key2MIDI
A small Python application for converting keystrokes (a-h) into MIDI CC or Note messages and sending them into a designated MIDI port, this message can also be triggered by a button. I originally created to test some MIDI remote scripts I've been writing for Ableton Live, without needing to plug a controller or other software in it was much simpler to just use a simple python script to send MIDI over IAC, but it can also be used for mapping or testing just about anything to do with MIDI. 

I decided to build a GUI for it using tkinter, this was my first attempt at this to learn how to do it, as well as packaging pythong programs using py2app. There is a packaged .app file that's been test on Sierra and newer.

At the moment it's macOS only but I will be making it compatible for Windows.

The python script requires rtmidi with "pip install python-rtmidi".

I was using pynput and keyboard modules to listen for global keyboard events but this caused issues when converting to an app due it needing to be run with root permissions. The keyboard events are being handled using tkinter bind methods in this version.

## To Do:
1. Port to Windows
2. Add/Remove message rows
3. Add Program Change and SysEx functionality
4. Find a way of getting input monitoring permissions (for pynput)
5. Find a better way of writing GUI's (tkinter is simple and fast, but colour issues are frustrating)
