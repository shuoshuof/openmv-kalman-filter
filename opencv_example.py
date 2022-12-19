import cv2
import numpy as np
import time
import random
A = np.array([[1,0,1,0],
              [0,1,0,1],
              [0,0,1,0],
              [0,0,0,1]],np.float32)


H = np.eye(4)

Q = np.eye(4)*0.1

R = np.eye(4)*1

B=None

P = np.eye(4)#误差协方差矩阵

last_X_posterior = None

frame = np.zeros((800, 800, 3), np.uint8)

first_flag=0

runtime = 0
def mousemove(event, x, y, s, p):
    global frame,first_flag,last_X_posterior,P,runtime,A
    if first_flag==0:
        #状态初始化
        last_X_posterior = np.array([[x],
                                   [y],
                                   [0],
                                   [0]],np.float32)
        first_flag=1
        runtime = time.time()

    else:
        t = time.time()
        dt = t - runtime
        runtime = time.time()
        #get measurement
        print(dt)
        dt=1
        if random.random()>0.5:

            d_x = x-last_X_posterior[0][0]
            d_y = y-last_X_posterior[1][0]
            print("dx:",d_x)
            Z_measure = np.array([[x],
                                  [y],
                                  [d_x/dt],
                                  [d_y/dt]],np.float32)
            print(Z_measure)

            #先验
            A[0][2],A[1][3]=dt,dt
            X_prior = A@last_X_posterior
            #先验误差协方差矩阵
            P_k_prior = A@P@A.T+Q
            #卡尔曼增益
            K_k = (P_k_prior@H.T)@np.linalg.inv(H@P_k_prior@H.T+R)
            #后验估计
            last_X_posterior = X_prior+K_k@(Z_measure-H@X_prior)
            #更新误差协方差矩阵
            P = (np.eye(4)-K_k@H)@P_k_prior
            cv2.circle(frame,(x,y),1,(0,0,255))
            x_pre = int(last_X_posterior[0][0])
            y_pre = int(last_X_posterior[1][0])
            cv2.circle(frame,(x_pre,y_pre),1,(0,255,0))
        else:
            A[0][2],A[1][3]=dt,dt
            last_X_posterior = A@last_X_posterior

            cv2.circle(frame,(x,y),1,(0,0,255))
            x_pre = int(last_X_posterior[0][0])
            y_pre = int(last_X_posterior[1][0])
            cv2.circle(frame,(x_pre,y_pre),1,(255,0,0))



cv2.namedWindow("kalman_mouse_tracker")
cv2.setMouseCallback("kalman_mouse_tracker", mousemove)

while True:
    cv2.imshow("kalman_tracker", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
cv2.destroyAllWindows()
