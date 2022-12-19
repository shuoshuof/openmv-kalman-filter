import SEEKFREE_18TFT as tft18
import sensor, image, time
from machine import UART
import ruku
from pyb import LED
from rt1064_uart import uart_stx
import mtx
import openmv_numpy as np
from kalman_filter import Tracker,Tracker_Manager
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 灰度更快(160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(True)
sensor.set_auto_exposure(True)
#sensor.set_auto_exposure(False,100)
clock = time.clock()
red = LED(1)    # 定义一个LED1   红灯
green = LED(2)  # 定义一个LED2   绿灯
blue = LED(3)   # 定义一个LED3   蓝灯
white = LED(4)  # 定义一个LED4   照明灯

mat = [[4.05929371844852, -0.004330286457665396, -8.165148583410403],
[-0.2237300051478909, 4.083072593949009, -11.6898927689773],
[0.0004252518331063399, -0.001127529949685983, 1]]



W = 160
H = 120
y_b = -120
x_b = 0#横向矫正常数
yellow_rect=(0, 100, -54, 3, 6, 127)

yellow_cheku=(0, 100, -128, 10, 23, 127)



A = np.array([[1,0,1,0],
              [0,1,0,1],
              [0,0,1,0],
              [0,0,0,1]])


H_k = np.eye(4)

Q = np.eye(4,value=0.1)

R = np.eye(4)

B=None



def judge_rect(r):
    print(r.y())
    if r.h()<=50 and r.w()<=50 and r.h()>=25 and r.w()>=25 and r.y()>=40 and abs(r.w()-r.h())<=20:
        return True
    if r.h()<=40 and r.w()<=40 and r.h()>=15 and r.w()>=15 and r.y()<=40:
        return True
    return False
work_state=0
runtime=0
led_flag=0

Manager = Tracker_Manager()

while(True):

    clock.tick()
    #work_state=5

    img = sensor.snapshot()

    img.binary([yellow_rect])
    img.dilate(1)
    img.erode(1)

    find = 0
    for r in img.find_rects(threshold = 30000):
        #if r.h()<=40 and r.w()<=40 and r.h()>=15 and r.w()>=15:
        if judge_rect(r):
            img.draw_rectangle(r.rect(), color = (255, 0, 0))
            #for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))
            position_x ,position_y = int(r.x()+r.w()/2),int(r.y()+r.h()/2)
            #print(position_x,position_y)
            img.draw_cross(position_x, position_y, color = (255, 0, 0), size = 10, thickness = 2)
            Manager.match(position_x,position_y,A,H_k,Q,R)
    Manager.update()
    trails_pre = Manager.get_motion_trail_pre()
    for ID,trail in trails_pre:
        if len(trail):
            x,y = trail[0][0], trail[0][1]
            img.draw_string(x,y,str(ID),color=(255,0,0))


