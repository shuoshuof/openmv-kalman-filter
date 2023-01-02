import sensor, image, time
from pyb import LED
import openmv_numpy as np
from kalman_filter import Tracker,Tracker_Manager
sensor.reset()
sensor.set_pixformat(sensor.RGB565) 
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(True)
sensor.set_auto_exposure(True)
#sensor.set_auto_exposure(False,100)


yellow_rect=(0, 100, -54, 3, 6, 127)

A = np.array([[1,0,1,0],
              [0,1,0,1],
              [0,0,1,0],
              [0,0,0,1]])


H_k = np.eye(4)

Q = np.eye(4,value=0.1)

R = np.eye(4)

B=None

Manager = Tracker_Manager()

while(True):


    img = sensor.snapshot()

    img.binary([yellow_rect])#二值化
    img.dilate(1)
    img.erode(1)

    find = 0
    for r in img.find_rects(threshold = 30000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0))
        #for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
        position_x ,position_y = int(r.x()+r.w()/2),int(r.y()+r.h()/2)
        #print(position_x,position_y)
        img.draw_cross(position_x, position_y, color = (255, 0, 0), size = 10, thickness = 2)
        #匹配
        Manager.match(position_x,position_y,A,H_k,Q,R)
    Manager.update()
    trails_pre = Manager.get_motion_trail_pre()
    for ID,trail in trails_pre:
        if len(trail):
            x,y = trail[0][0], trail[0][1]
            img.draw_string(x,y,str(ID),color=(255,0,0))


