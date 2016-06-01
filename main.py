from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import serial

ser = serial.Serial('/dev/tty.usbmodem1421', 9600)

m = PyMouse()
k = PyKeyboard()

while True:
    ser.write('hello from Ghost\n')
    time.sleep(1)


x_dim, y_dim = m.screen_size()
print "screen size X:", x_dim
print "screen size Y:", y_dim
snippet_a = ['//Sketch A','float increment = 0.01;\r\n','float zoff = 0.0;\r\n','float zincrement = 0.02;\r\n']
snippet_b = ['float zoff = 0.0;\r\n','float zincrement = 0.2;\r\n','float increment = 0.1;\r\n', '//Sketch B']


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
