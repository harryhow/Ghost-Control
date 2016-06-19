from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import serial
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
import watchdog.events
from threading import Timer
import os
import os.path
import threading
import pathlib

try:
    ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
except:
    e = sys.exc_info()[0]
    print e

m = PyMouse()
k = PyKeyboard()

x_dim, y_dim = m.screen_size()
print "screen size X:", x_dim
print "screen size Y:", y_dim

current_window_ctr_x = 0
current_window_ctr_y = 0
prt_dialog_x_pos = 1140 #@1920
prt_dialog_y_pos = 400 #@1080
current_window = 0
current_window_ctr_x = 0
current_window_ctr_y = 0
prevPrinted = "output.pdf"
# pdfpath = './output.pdf'


class LennaTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False



class Handler(watchdog.events.PatternMatchingEventHandler):


    def __init__(self):
        print "watch dog init"
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.lenna'],ignore_directories=True, case_sensitive=False)


    def on_modified(self, event):
        print "on_modified..."
        if event.src_path.lower().endswith('.lenna'):
            self.process(event)
            print "some one modify lenna, read file"
            # move_mouse.clickPrinterDialog()
            timer.stop()
            try:
                ser.write('HIT\n')
            except:
                e = sys.exc_info()[0]
                print e

            # time.sleep(10) #
            with open('printit.lenna') as f:
                content = f.readlines()

            try:
			    fileprinted = content[0]
            except IndexError:
                fileprinted = 'null'
            
            # print "file name: ", content[0]
            # fileprinted = content[0]
            fileprinted = os.getcwd() + "/" + fileprinted

            # this will stop the timer
            time.sleep(2) #

            print "check existing file? ", fileprinted
            # p = pathlib.Path(fileprinted)

            # try:
            # 	with p.open() as f:
            # 		print "printing PDF"
            # except OSError:
            # 	print('err...')	
            

            # if p.is_file():
            # 	print "printing PDF"
            #     #os.system("lpr -P HP_ENVY_7640_series -o page-border=none output.pdf") # TODO: borderless option
            #     m.click(x_dim/2, y_dim/2, 1)
            #     k.press_keys(['Command','Q'])
            #     time.sleep(2) #
            # else:
            # 	 print "no PDF!"


            if os.path.isfile(fileprinted):
                print "printing PDF"
                #os.system("lpr -P HP_ENVY_7640_series -o page-border=none output.pdf") # TODO: borderless option
                m.click(x_dim/2, y_dim/2, 1)
        
                global prevPrinted
                if prevPrinted != fileprinted:
                    # lprcmd = "lpr -P HP_ENVY_7640_series -o fit-to-page" + " " + fileprinted
                    os.system(lprcmd) # TODO: borderless option
        
                prevPrinted = fileprinted
                # k.press_keys(['Command','q'])
                # time.sleep(2) #
            else:
                print "no PDF!"

            timer.start()


    def process(self, event):
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug


    on_created = on_modified



###################################
# move mouse
###################################

class MoveMouse():

    def clickPrinterDialog(self):
        print "click printer dialog...", prt_dialog_x_pos, prt_dialog_y_pos
        m.click(prt_dialog_x_pos, prt_dialog_y_pos, 1)

    def typenrun(self):
        print "move to window: ", current_window
        print "window center is: ", current_window_ctr_x, "and ", current_window_ctr_y
    # def typenrun(self):
    #     snippet_a = ['//Sketch A','float increment = 0.01;\r\n','float zoff = 0.0;\r\n','float zincrement = 0.02;\r\n']
    #     for index, val in enumerate(snippet_a):
    #         #m.click(current_window_ctr_x, current_window_ctr_y, 1)
    #         #m.move(80, yloc)
    #         #k.press_key('function')
    #         k.type_string(val)
    #         time.sleep(1)
    #
        # m.click(current_window_ctr_x, current_window_ctr_y, 1)
        # k.press_keys(['Command','r'])


def moveToNextProcessingWindow(name):
    print "+ Move to next"
    global current_window
    global current_window_ctr_x
    global current_window_ctr_y

    if (current_window < 4):
        if (current_window == 0):
            current_window_ctr_x = 0.25 * x_dim
            current_window_ctr_y = 0.25 * y_dim
        if (current_window == 1):
            current_window_ctr_x = 0.75 * x_dim
            current_window_ctr_y = 0.25 * y_dim
        if (current_window == 2):
            current_window_ctr_x = 0.25 * x_dim
            current_window_ctr_y = 0.75 * y_dim
        if (current_window == 3):
            current_window_ctr_x = 0.75 * x_dim
            current_window_ctr_y = 0.75 * y_dim
    else:
        current_window = 0

    move_mouse.typenrun()
    current_window = current_window + 1



move_mouse = MoveMouse()
event_handler = Handler()
timer = LennaTimer(30, moveToNextProcessingWindow, "noname") # it auto-starts, no need of rt.start(), 5 min interval


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = '.'

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    timer.start()
