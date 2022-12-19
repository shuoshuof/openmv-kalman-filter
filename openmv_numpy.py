import math
import time
class array:
    def __init__(self,M:list):
        self.M= M
        self.shape = self.get_shape()
    def __len__(self):
        return len(self.M)
    def __getitem__(self, *args):
        if isinstance(args[0],tuple):
            assert len(args[0]) <= len(self.shape), 'out'
            indexs =list(args[0])
            def get_value(a,num):
                if len(indexs)-1==num:
                    return a[indexs[num]]
                return get_value(a[indexs[num]],num+1)
            return get_value(self.M,0)
        elif isinstance(args[0],int):
            return self.M[args[0]]
    def get_shape(self):
        shape = []
        def get_len(a):
            try:
                shape.append(len(a))
                get_len(a[0])
            except:
                pass
        get_len(self.M)
        return tuple(shape)
    @property
    def T(self):
        shape = self.shape
        assert len(shape)==2
        r, w = shape
        B = array([[self[j][i] for j in range(r)] for i in range(w)])
        return B
    def __add__(self, other):
        A_shape = self.shape
        B_shape = other.shape
        assert len(A_shape) == 2 and len(B_shape) == 2 and A_shape == B_shape
        r, w = A_shape
        return array([[self[i][j] + other[i][j] for j in range(w)] for i in range(r)])
    def __sub__(self, other):
        A_shape = self.shape
        B_shape = other.shape
        assert len(A_shape) == 2 and len(B_shape) == 2 and A_shape == B_shape
        r, w = A_shape
        return array([[self[i][j] - other[i][j] for j in range(w)] for i in range(r)])
    def __mul__(self, other):
        A_shape = self.shape
        B_shape = other.shape
        assert len(A_shape) == 2 and len(B_shape) == 2
        r_a, w_a = A_shape
        r_b, w_b = B_shape
        assert w_a == r_b, '无法相乘'
        def l(i, j):
            return sum([self[i][t] * other[t][j] for t in range(r_a)])
        # return array([[l(i, j) for j in range(w_b)] for i in range(r_a)])
        return array([[l(i, j) for j in range(w_b)] for i in range(r_a)])
    @staticmethod
    def A_yu(A, I, J):
        r = len(A[0])
        M = []
        for i in range(r):
            if i != I:
                row = []
                for j in range(r):
                    if j != J:
                        row.append(A[i][j])
                M.append(row)
        return array(M)
    # def det(self):#递归太慢，弃用
    #     assert len(self.shape) == 2 and self.shape[0] == self.shape[1], '非方阵'
    #     if len(self) == 1:
    #         return self[0][0]
    #     ans = 0
    #     r = len(self[0])
    #     for t in range(r):
    #         M = self.A_yu(self.M, 0, t)
    #         ans += (-1) ** (1 + t + 1) * self[0][t] * M.det()
    #     return ans
    def det(self):
        shape = self.shape
        assert len(shape) == 2 and shape[0] == shape[1], '非方阵'
        r, c = shape
        m = [[self.M[i][j] for j in range(c)] for i in range(r)]
        ans=1
        for col in range(c):
            v = [math.fabs(row[col]) for row in m[col:]]
            zhu_yuan = max(v)
            if zhu_yuan==0:
                return 0
            zhu_yuan_index = v.index(zhu_yuan)+col
            zhu_yuan = m[zhu_yuan_index][col]
            zhu_row = [x / zhu_yuan for x in m[zhu_yuan_index]]
            ans=ans*zhu_yuan
            if zhu_yuan_index!=col:
                temp = m[col]
                m[col]=zhu_row
                m[zhu_yuan_index] =temp
                ans*=-1#互换行列式两行，需要变号
            else:
                m[col] = zhu_row

            for i in range(col+1,r):
                k = m[i][col]
                m[i] = [ m[i][j]-k*zhu_row[j] for j in range(c)]
        return ans
    def inv(self):
        shape = self.shape
        assert self.det()!=0,'方阵不可逆'
        r, c = shape
        # for row in range(r):
        m = [[self.M[i][j] for j in range(c)] for i in range(r)]
        I = [[1 if i==j else 0 for i in range(r)] for j in range(r)]
        ans=1
        for col in range(c):
            v = [math.fabs(row[col]) for row in m[col:]]
            zhu_yuan = max(v)
            if zhu_yuan==0:
                return 0
            zhu_yuan_index = v.index(zhu_yuan)+col
            zhu_yuan = m[zhu_yuan_index][col]
            zhu_row = [x / zhu_yuan for x in m[zhu_yuan_index]]
            I_zhu_row = [x/zhu_yuan for x in I[zhu_yuan_index]]
            ans=ans*zhu_yuan
            if zhu_yuan_index!=col:
                temp = m[col]
                m[col]=zhu_row
                m[zhu_yuan_index] =temp

                I_temp = I[col]
                I[col] = I_zhu_row
                I[zhu_yuan_index]=I_temp

                ans*=-1#互换行列式两行，需要变号
            else:
                m[col] = zhu_row
                I[col] = I_zhu_row
            for i in range(r):
                if i!=col:
                    k = m[i][col]
                    m[i] = [ m[i][j]-k*zhu_row[j] for j in range(c)]
                    I[i] = [I[i][j]-k*I[col][j]for j in range(c)]
            # for i in range(col+1,r):
            #     k = m[i][col]
            #     m[i] = [ m[i][j]-k*zhu_row[j] for j in range(c)]
            #     I[i] = [I[i][j] - k * I[col][j] for j in range(c)]
            # print(m)
        return array(I)
    # def inv(self):
    #     assert len(self.shape) == 2 and self.shape[0] == self.shape[1], '非方阵'
    #     assert self.det()!=0,'方阵不可逆'
    #     A_star = []
    #     r, w = self.shape
    #     c = self.det()
    #     for i in range(r):
    #         row = []
    #         for j in range(w):
    #             row.append((-1) ** (i + j) * self.A_yu(self, i, j).det()/c)
    #         A_star.append(row)
    #     A_inv = array(A_star).T
    #     return A_inv
    def __str__(self):
        return str(self.M)
def eye(size,value=1):
    M = [[value if i==j else 0 for i in range(size)] for j in range(size)]
    return array(M)

def full(shape:tuple,value):
    def add(m,index):
        if index<0:
            return m
        M=[]
        for _ in range(shape[index]):
            M.append(m)
        return add(M,index-1)

    M = add([value for _ in range(shape[-1])],len(shape)-1-1)
    return array(M)

def zeros(shape:tuple):
    return full(shape,0)

def ones(shape:tuple):
    return full(shape,1)

if __name__ =='__main__':
    A = [[1,3],
         [1,2]]
    B = [[2,1],
         [1,1]]
    A0 = [[4,1,2,3],
          [4,5,4,2],
          [1,3,3,4],
          [1,3,2,5]]
    #
    # print(ones((1,3)))
    
    A= array(A0)
    print(A[0,0])

    # t1 = time.clock()
    # print(A.inv())
    # t2 = time.clock()
    # print(f"time:{t2-t1}")
    # #
    # import numpy as np
    # t3 = time.clock()
    # print(np.linalg.inv(np.array(A0)))
    # t4=time.clock()
    # print(f"time:{t4-t3}")