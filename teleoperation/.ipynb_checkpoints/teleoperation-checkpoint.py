from jetbot import Robot
from jetbot import Camera
import cv2
import time
import math

import os, struct, array
from fcntl import ioctl

robot = Robot()
camera = Camera()

camera.start()


# Iterate over the joystick devices.
print('Available devices:')

for fn in os.listdir('/dev/input'):
    if fn.startswith('js'):
        print('  /dev/input/%s' % (fn))
#这句显示手柄在硬件中的端口位置： /dev/input/js0
# We'll store the states here.
axis_states = {}
button_states = {}


# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'rx',
    0x05 : 'ry',
   
}

buttons_name = {
    0x00 : 'a',
    0x01 : 'b',
    0x02 : 'c',
    0x03 : 'd',
    0x04 : 'e',
    0x05 : 'f',
    0x06 : 'g',
    0x07 : 'h',
}

axis_map = []
buttons_map = []

# Open the joystick device.
fn = '/dev/input/js0'
print('Opening %s...' % fn)
jsdev = open(fn, 'rb')

# # Get the device name.
buf = array.array('u', ['\0']*5)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tostring()
print('Device name: %s' % js_name)

# Get number of axes and buttons.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

# Get the axis map.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP
#
for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

print(axis_map)

img_count = 0

# Main event loop
while True:
    evbuf = jsdev.read(8)
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)
        
        if type & 0x01:
            if number == 0:
                if value == 1:
                    print("A pressed")
            if number == 1:
                if value == 1:
                    print("B pressed")
                    img_name = 'snapshots/'+str(img_count)+'.png'
                    cv2.imwrite(img_name,camera.value, [int( cv2.IMWRITE_JPEG_QUALITY), 95])
                    img_count = img_count + 1
                    
            if number == 3:
                if value == 1:
                    print("X pressed")
            if number == 4:
                if value == 1:
                    print("Y pressed")
            if number == 6:
                if value == 1:
                    print("L1 pressed")
            if number == 7:
                if value == 1:
                    print("R1 pressed")
            if number == 10:
                if value == 1:
                    print("Select pressed")
            if number == 11:
                if value == 1:
                    print("Start pressed")
                    exit(0)
                    
        
        if type & 0x02:
            axis = axis_map[number]
            if axis:
                
                #print("{}".format(axis))
                if axis=="x":
                    fvalue = value / 32767
                    print ("%s: %.3f" % (axis, fvalue))
                    if(fvalue < 0):
                        robot.left(speed=math.fabs(fvalue/3))
                    elif(fvalue > 0):
                        robot.right(speed=math.fabs(fvalue/3))
                    else:
                        robot.stop()
                    
                if axis=="y":
                    fvalue = value / 32767
                    print ("%s: %.3f" % (axis, fvalue))
                    if(fvalue < 0):
                        robot.forward(speed=math.fabs(fvalue/3))
                    elif(fvalue > 0):
                        robot.backward(speed=math.fabs(fvalue/3))
                    else:
                        robot.stop()

                    
                if axis=="rx":
                    fvalue = value / 32767
                    print ("%s: %.3f" % (axis, fvalue))

                    
                if axis=="ry":
                    fvalue = value / 32767
                    print ("%s: %.3f" % (axis, fvalue))