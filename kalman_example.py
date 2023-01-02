import cv2
import openmv_numpy as np
import numpy as np1
from kalman_filter import Tracker_Manager
import random
import math
A = np.array([[1,0,1,0],
              [0,1,0,1],
              [0,0,1,0],
              [0,0,0,1]])


H = np.eye(4)

Q = np.eye(4,value=0.1)

R = np.eye(4)

B=None

Manager = Tracker_Manager()
frame = np1.zeros((800, 800, 3), np1.uint8)
def draw(x,y,pre):
    global frame
    if pre:
        cv2.circle(frame, (x, y), 1, (255, 0, 0))
    else:
        cv2.circle(frame, (x, y), 1, (0, 0, 255))
def draw_motion_trail(motion_trail,pre):
    for position in motion_trail:
        draw(position[0],position[1],pre)
#轨迹
class trail_creater:
    def __init__(self,px,py,r):
        self.px = px
        self.py = py
        self.r = r
        self.t = 0
    def __call__(self):
        theta = (self.t%360/360)*2*math.pi
        self.t+=1
        x = self.r*math.cos(theta)+self.px
        y = self.r*math.sin(theta)+self.py
        return int(x),int(y)
#轨迹管理器
class trail_creater_Manager:
    def __init__(self):
        self.creaters=[]
    def __len__(self):
        return len(self.creaters)
    def append(self,creater:trail_creater):
        self.creaters.append(creater)
    def update(self)->list:
        all_positions = []
        for creater in self.creaters:
            x,y = creater()
            if random.random()<0.5:
                all_positions.append([x,y])
        return all_positions

trail_1 = trail_creater(100,100,50)
trail_2 = trail_creater(150,100,0)
creater_Manager = trail_creater_Manager()
creater_Manager.append(trail_1)
creater_Manager.append(trail_2)
while True:
    frame = np1.zeros((800, 800, 3), np1.uint8)
    for pos in creater_Manager.update():
        cv2.circle(frame, (pos[0], pos[1]), 1, (0, 0, 255))
        Manager.match(pos[0], pos[1], A, H, Q, R)
    Manager.update()
    trails_pre = Manager.get_motion_trail_pre()
    for ID,trail in trails_pre:
        if len(trail):
            cv2.putText(frame,str(ID),(trail[0][0],trail[0][1]),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        draw_motion_trail(trail,True)
    # for ID,pos in Manager.get_positions():
    #     x,y=pos
    #     cv2.putText(frame,str(ID),(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.imshow("kalman_tracker", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    # frame = np1.zeros((800, 800, 3), np1.uint8)
    # Manager.update()
    # trails_measure = Manager.get_motion_trail_measure()
    # for trail in trails_measure:
    #     draw_motion_trail(trail,False)
    # trails_pre = Manager.get_motion_trail_pre()
    #
    # for trail in trails_pre:
    #     draw_motion_trail(trail,True)
    # print(len(Manager))

cv2.destroyAllWindows()
