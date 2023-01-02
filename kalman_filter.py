import openmv_numpy as np

class Tracker:
    def __init__(self,A:np.array,H:np.array,Q:np.array,R:np.array,ID,lose_threshold=20,motion_trail_len=10,cls=None):
        self.A = A
        self.H = H
        self.Q = Q
        self.R = R
        self.P=np.eye(4)#误差协方差矩阵
        self.active = 0 #
        self.lose_threshold = lose_threshold#多少帧后认为目标丢失
        self.updated=False #是否在该帧已经更新了的标志位
        self.last_X_posterior=None
        self.last_position = [None,None]
        self.motion_trail_measure = []
        self.motion_trail_pre = []
        self.motion_trail_len = motion_trail_len
        self.ID=ID
        self.cls=cls
    def __call__(self, x,y,find):
        if find:
            self.add_motion_trail_measure(x,y)
            self.last_position = [x, y]
            if self.active==0:
                self.last_X_posterior = np.array([[x],
                                             [y],
                                             [0],
                                             [0]])
                self.active = self.lose_threshold
                self.updated = True
                return x,y
            else:
                dt = 1
                d_x = x - self.last_X_posterior[0][0]
                d_y = y - self.last_X_posterior[1][0]
                Z_measure = np.array([[x],
                                      [y],
                                      [d_x / dt],
                                      [d_y / dt]])

                # 先验
                self.A[0][2], self.A[1][3] = dt, dt
                X_prior = self.A * self.last_X_posterior
                # 先验误差协方差矩阵
                P_k_prior = self.A * self.P * self.A.T + self.Q
                # 卡尔曼增益
                K_k = (P_k_prior * self.H.T) * ((self.H * P_k_prior * self.H.T + self.R).inv())
                # 后验估计
                self.last_X_posterior = X_prior + K_k * (Z_measure - self.H * X_prior)
                # 更新误差协方差矩阵
                self.P = (np.eye(4) - K_k * self.H) * P_k_prior

                x_pre = int(self.last_X_posterior[0][0])
                y_pre = int(self.last_X_posterior[1][0])
                self.add_motion_trail_pre(x_pre,y_pre)
                self.active = self.lose_threshold
                self.updated = True
                return x_pre, y_pre

        else:
            self.active-=1#当active值再一次为0时，会被管理器删除
            self.last_X_posterior = self.A*self.last_X_posterior
            x_pre = int(self.last_X_posterior[0][0])
            y_pre = int(self.last_X_posterior[1][0])
            self.add_motion_trail_pre(x_pre, y_pre)
            return x_pre, y_pre
    def add_motion_trail_measure(self,x,y):
        self.motion_trail_measure.append([int(x),int(y)])
        if len(self.motion_trail_measure)>=self.motion_trail_len:
            self.motion_trail_measure.pop(0)
    def add_motion_trail_pre(self, x, y):
        self.motion_trail_pre.append([int(x), int(y)])
        if len(self.motion_trail_pre) >= self.motion_trail_len:
            self.motion_trail_pre.pop(0)
    def get_pre(self):#获得预测值用于配对，不进行更新
        pres = self.A*self.last_X_posterior
        return [int(pres[0][0]),int(pres[1][0])]
class Tracker_Manager:
    def __init__(self,match_threshold=50):
        self.trackers =[]
        self.match_threshold = match_threshold#匹配距离的阈值
        self.amount =0
    def __len__(self):
        return len(self.trackers)
    def append(self,tracker:Tracker):
        self.trackers.append(tracker)
    def match(self,x,y,A:np.array,H:np.array,Q:np.array,R:np.array,lose_threshold=20,motion_trail_len=20):
        def get_dist(tracker,x,y):
            return ((tracker.get_pre()[0]-x)**2+(tracker.get_pre()[1]-y)**2)**0.5

        dist = [get_dist(tracker,x,y) for tracker in self.trackers]
        if len(dist):
            min_dist = min(dist)
        else:
            min_dist = self.match_threshold+1
        if min_dist<=self.match_threshold:
            self.trackers[dist.index(min_dist)](x,y,True)#更新匹配成功的追踪器
        else:
            print("匹配失败")
            self.amount+=1
            new_trackers = Tracker(A,H,Q,R,self.amount,lose_threshold,motion_trail_len)#匹配失败，是新的目标，创建新的追踪器
            new_trackers(x,y,True)
            self.append(new_trackers)
    def update(self):#对该帧未检测到的追踪器进行行更新
        delate_indexs = []
        for i,tracker in enumerate(self.trackers):#更新没匹配成功的追踪器
            if tracker.updated:
                tracker.updated=False
            else:
                tracker(0,0,False)
            if tracker.active==0:#查找失效追踪器
                delate_indexs.append(i)
        del_num=0
        for index in delate_indexs:#删除失效追踪器
            self.trackers.pop(index - del_num)
            del_num += 1
    def get_positions(self):#获取后验坐标
        positions =[]
        for tracker in self.trackers:
            x,y = tracker.last_X_posterior[0][0],tracker.last_X_posterior[1][0]
            positions.append((tracker.ID,[int(x),int(y)]))
        return positions
    def get_motion_trail_measure(self):
        return [(tracker.ID,tracker.motion_trail_measure) for tracker in self.trackers]
    def get_motion_trail_pre(self):
        return [(tracker.ID,tracker.motion_trail_pre) for tracker in self.trackers]


