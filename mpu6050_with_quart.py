from vpython import *
import time
import serial
import numpy as np
import math
ad = serial.Serial('com3', 115200)
sleep(1)

len = 5
wid = 0.5
thick = 8

toRad = 2*np.pi/360
toDeg = 1/toRad

scene.forward = vector(-1, -1, -1)
scene.width = 600
scene.height = 600
scene.range = 5

board = box(pos=vector(0, 0, 0), size=vector(
    len, wid, thick), color=vector(1, 1, 1), opacity=0.2)
xarrow = arrow(lenght=2, shaftwidth=.1,
               color=color.red, axis=vector(1, 0, 0))
yarrow = arrow(lenght=4, shaftwidth=.1,
               color=color.green, axis=vector(0, 1, 0))
zarrow = arrow(lenght=2, shaftwidth=.1,
               color=color.blue, axis=vector(0, 0, 1))
frontArrow = arrow(length=4, shaftwidth=.1,
                   color=color.purple, axis=-vector(1, 0, 0))
upArrow = arrow(length=1, shaftwidth=.1,
                color=color.magenta, axis=-vector(0, 1, 0))
sideArrow = arrow(length=2, shaftwidth=.1,
                  color=color.orange, axis=-vector(0, 0, 1))


mpu = box(size=vector(1.5, 0.2, 1.75), pos=vector(
    0, 0, 2), opacity=0.8, color=color.white)

myObj = compound([board, mpu])
while (True):
    while (ad.inWaiting() == 0):
        pass
    junk = ad.readline()
    dataPacket = ad.readline()
    dataPacket = str(dataPacket, 'utf-8')
    splitPacket = dataPacket.split(",")
    q0 = float(splitPacket[0])
    q1 = float(splitPacket[1])
    q2 = float(splitPacket[2])
    q3 = float(splitPacket[3])
    roll = atan2(2*(q0*q1+q2*q3), 1-2*(q1*q1+q2*q2))
    pitch = -asin(2*(q0*q2-q3*q1))
    yaw = -atan2(2*(q0*q3+q1*q2), 1-2*(q2*q2+q3*q3))
    print("Roll=", roll*toDeg, " Pitch=", pitch*toDeg, "Yaw=", yaw*toDeg)
    rate(50)
    k = vector(cos(yaw)*cos(pitch), sin(pitch), sin(yaw)*cos(pitch))
    y = vector(0, 1, 0)
    s = cross(k, y)
    v = cross(s, k)
    vrot = v*cos(roll)+cross(k, v)*sin(roll)

    frontArrow.axis = k
    sideArrow.axis = cross(k, vrot)
    upArrow.axis = vrot
    myObj.axis = k
    myObj.up = vrot
    sideArrow.length = 2
    frontArrow.length = 4
    upArrow.length = 1
