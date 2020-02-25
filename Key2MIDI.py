import string, json
import rtmidi
from functools import partial
from tkinter import *
from tkinter.ttk import *

# Here we define some global variables for the path.

PATH = '/Applications/Key2MIDI.app/Contents/Resources/save.json'

# This loads the saved values.
with open(PATH, 'r') as f:
    INPUT = json.load(f)

# Here we set up the MIDI functionality, and get the ports for the menu.

MIDI_OUT = rtmidi.MidiOut()
PORTS = MIDI_OUT.get_ports()
PORTS.insert(0, 'Select MIDI Output Port')

# This creates variables used to generate the GUI later.
ROWS = 8
OBJECTS = {}
VARIABLES = {}
CHARS = list(string.ascii_lowercase)


def set_message(row):
    # This function creates the message from the objects on the row, then sends them to the send message function.
    msg_type, channel_num, note_num, value_num = OBJECTS['select_type{0}'.format(row)].current(), int(
        OBJECTS['channel{0}'.format(row)].get()), int(OBJECTS['note{0}'.format(row)].get()), int(
        OBJECTS['value{0}'.format(row)].get())
    send_message(msg_type, channel_num, note_num, value_num)


def send_message(msg_type, channel_num, note_num, value_num):
    # This function opens the selected MIDI port, then creates either a CC or Note message, and sends it out the port.
    port = select_port.current()
    if msg_type == 0:
        byte1 = 0xB0 + channel_num
    elif msg_type == 1:
        byte1 = 0x90 + channel_num
    MIDI_OUT.open_port(port - 1)
    message = [byte1, note_num, value_num]
    MIDI_OUT.send_message(message)
    MIDI_OUT.close_port()


def save_values(data):
    # This function is for storing the values to the JSON file, so they are recalled on loading.
    output = {}
    output['select_port'] = select_port.current()
    for key, value in data.items():
        if 'channel' in key or 'note' in key or 'value' in key:
            output[key] = int(value.get())

        elif 'select_type' in key:
            output[key] = (value.current())
    with open(PATH, 'w') as f:
        json.dump(output, f)


def create_rows():
    # This function creates all the objects in a loop, using the global dictionaries defined earlier.
    global ROWS
    global window
    for row in range(1, ROWS + 1):
        OBJECTS['select_type{0}'.format(row)] = Combobox(window, state='readonly', values=('CC', 'Note'), width=5)
        OBJECTS['select_type{0}'.format(row)].grid(column=0, row=row + 1, sticky=W)
        VARIABLES['channel{0}'.format(row)] = IntVar()
        VARIABLES['note{0}'.format(row)] = IntVar()
        VARIABLES['value{0}'.format(row)] = IntVar()
        if 'channel{0}'.format(row) in INPUT.keys():
            OBJECTS['select_type{0}'.format(row)].current(INPUT['select_type{0}'.format(row)])
            VARIABLES['channel{0}'.format(row)].set(INPUT['channel{0}'.format(row)])
            VARIABLES['note{0}'.format(row)].set(INPUT['note{0}'.format(row)])
            VARIABLES['value{0}'.format(row)].set(INPUT['value{0}'.format(row)])
        else:
            OBJECTS['select_type{0}'.format(row)].current(0)
            VARIABLES['channel{0}'.format(row)].set(0)
            VARIABLES['note{0}'.format(row)].set(0)
            VARIABLES['value{0}'.format(row)].set(0)
        OBJECTS['channel{0}'.format(row)] = Spinbox(window, from_=0, to=15, width=3,
                                                    textvariable=VARIABLES['channel{0}'.format(row)])
        OBJECTS['channel{0}'.format(row)].grid(column=0, row=row + 1)
        OBJECTS['note{0}'.format(row)] = Spinbox(window, from_=0, to=127, width=3,
                                                 textvariable=VARIABLES['note{0}'.format(row)])
        OBJECTS['note{0}'.format(row)].grid(column=1, row=row + 1, sticky=W)
        OBJECTS['value{0}'.format(row)] = Spinbox(window, from_=0, to=127, width=3,
                                                  textvariable=VARIABLES['value{0}'.format(row)])
        OBJECTS['value{0}'.format(row)].grid(column=3, row=row + 1, sticky=W)
        OBJECTS['send{0}'.format(row)] = Button(window, text='Char: ' + CHARS[row - 1],
                                                command=partial(set_message, row))
        OBJECTS['send{0}'.format(row)].grid(column=4, row=row + 1, sticky=W)


def key_pressed(event):
    # This function is called when a key is pressed, it also handles Errors.
    char = event.char
    try:
        row = CHARS.index(char) + 1
        set_message(row)

    except:
        return


# Here we create everything that will be displayed in the window, including calling some of the functions above
# The final thing to do is start the mainloop() function which generates the window and keeps it open.
window = Tk()
window.title("Key2MIDI")
window.bind_all('<Key>', key_pressed)
window.configure(bg='#ececec')
select_port = Combobox(window, state='readonly', values=PORTS)
select_port.current(INPUT['select_port'])
select_port.grid(column=0, row=0)
chan_lbl = Label(window, text="Type:", width=6)
chan_lbl.grid(column=0, row=1, sticky=W)
chan_lbl = Label(window, text="Chan:", width=6)
chan_lbl.grid(column=0, row=1)
note_lbl = Label(window, text="Num:", width=6)
note_lbl.grid(column=1, row=1, sticky=W)
value_lbl = Label(window, text="Value:", width=6)
value_lbl.grid(column=3, row=1, sticky=W)
value_lbl = Label(window, text="Key:", width=6)
value_lbl.grid(column=4, row=1, sticky=W)
save = Button(window, text='Save', command=partial(save_values, OBJECTS))
save.grid(column=4, row=0)
create_rows()
window.mainloop()
