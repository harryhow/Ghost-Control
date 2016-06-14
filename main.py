from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
# import serial
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import watchdog.events



# ser = serial.Serial('/dev/tty.usbmodem1421', 9600)

m = PyMouse()
k = PyKeyboard()

#while True:
    # ser.write('hello from Ghost\n')
    # time.sleep(1)

class Handler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.lenna'],
            ignore_directories=True, case_sensitive=False)

    def on_modified(self, event):
        if event.src_path.lower().endswith('.lenna'):
                self.process(event)
                print "some one modify lenna, read file"
                move_mouse.typeup()



    def process(self, event):
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug


    on_created = on_modified


###################################
# move mouse
###################################

class MoveMouse():
    x_dim, y_dim = m.screen_size()
    print "screen size X:", x_dim
    print "screen size Y:", y_dim


    def typeup(self):
        snippet_a = ['//Sketch A','float increment = 0.01;\r\n','float zoff = 0.0;\r\n','float zincrement = 0.02;\r\n']
        for index, val in enumerate(snippet_a):
            yloc = 100+index*25
            print "yloc:",yloc
            m.click(80, yloc, 1)
            #m.move(80, yloc)
            #k.press_key('function')
            k.type_string(val)
            time.sleep(1)

    m.click(80, 100, 1)
    k.press_keys(['Command','R'])

    def typebottom(self):
        snippet_b = ['float zoff = 0.0;\r\n','float zincrement = 0.2;\r\n','float increment = 0.1;\r\n', '//Sketch B']
        time.sleep(2)
        for index, val in enumerate(snippet_b):
            m.click(80, 650, 1)
            yloc = 400+index*20
            print "yloc:",yloc
            m.click(80, yloc, 1)
            m.move(80, yloc)
            k.type_string(val)
            time.sleep(1)

        m.click(80, 650, 1)
        k.press_keys(['Command','R'])






logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
path = '.'
event_handler = Handler()
move_mouse = MoveMouse()
observer = Observer()
observer.schedule(event_handler, path, recursive=True)
observer.start()
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    observer.stop()
observer.join()


