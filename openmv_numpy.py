import math
import time
class array:
    def __init__(self,M:list):
        self.M= M
        self.shape = self.get_shape()
        self.ndim = len(self.shape)
    def __len__(self):
        return len(self.M)
    def __getitem__(self, *args):
        if isinstance(args[0],tuple):
            assert len(args[0]) <= self.ndim, 'out'
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

    def __add__(self, other):
        assert self.ndim == 2 and other.ndim == 2 and self.shape == other.shape
        r, w = self.shape
        return array([[self[i][j] + other[i][j] for j in range(w)] for i in range(r)])
    def __sub__(self, other):
        assert self.ndim == 2 and other.ndim == 2 and self.shape == other.shape
        r, w = self.shape
        return array([[self[i][j] - other[i][j] for j in range(w)] for i in range(r)])
    def __mul__(self, other):
        if isinstance(other,(int,float)):
            other = eye(self.shape[1],other)
        assert self.ndim == 2 and other.ndim == 2
        r_a, w_a = self.shape
        r_b, w_b = other.shape
        assert w_a == r_b, '无法相乘'
        def l(i, j):
            return sum([self[i][t] * other[t][j] for t in range(w_a)])
        return array([[l(i, j) for j in range(w_b)] for i in range(r_a)])
    
    @property
    def T(self):
        assert self.ndim==2
        r, w = self.shape
        B = array([[self[j][i] for j in range(r)] for i in range(w)])
        return B
    def det(self):
        shape = self.shape
        assert self.ndim==2 and shape[0] == shape[1], '非方阵'
        r, c = shape
        m = [[self.M[i][j] for j in range(c)] for i in range(r)]
        ans=1
        for col in range(c):
            v = [math.fabs(row[col]) for row in m[col:]]
            pivot = max(v)
            if pivot==0:
                return 0
            pivot_index = v.index(pivot)+col
            pivot = m[pivot_index][col]
            pivot_row = [x / pivot for x in m[pivot_index]]
            ans=ans*pivot
            if pivot_index!=col:
                temp = m[col]
                m[col]=pivot_row
                m[pivot_index] =temp
                ans*=-1#互换行列式两行，需要变号
            else:
                m[col] = pivot_row

            for i in range(col+1,r):
                k = m[i][col]
                m[i] = [ m[i][j]-k*pivot_row[j] for j in range(c)]
        return ans
    def inv(self):
        shape = self.shape
        assert self.det()!=0,'方阵不可逆'
        r, c = shape
        m = [[self.M[i][j] for j in range(c)] for i in range(r)]
        I = [[1 if i==j else 0 for i in range(r)] for j in range(r)]
        for col in range(c):
            v = [math.fabs(row[col]) for row in m[col:]] #选出从第col行开始的第col列
            pivot = max(v)
            if pivot==0:
                return 0
            pivot_index = v.index(pivot)+col
            pivot = m[pivot_index][col]
            pivot_row = [x/pivot for x in m[pivot_index]]
            I_pivot_row = [x/pivot for x in I[pivot_index]]
            if pivot_index!=col:#行互换
                temp = m[col]
                m[col]=pivot_row
                m[pivot_index] =temp

                I_temp = I[col]
                I[col] = I_pivot_row
                I[pivot_index]=I_temp
            else:
                m[col] = pivot_row
                I[col] = I_pivot_row
            for i in range(r):
                if i!=col:
                    k = m[i][col]
                    #对应行相减
                    m[i] = [ m[i][j]-k*pivot_row[j] for j in range(c)]
                    I[i] = [I[i][j]-k*I[col][j]for j in range(c)]
        return array(I)
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

#解线性方程组
def solve(A:array,B:array)->array:
    if A.det()==0:
        raise ValueError("无解")
    assert B.ndim==2 and B.shape[0]==A.shape[0] and B.shape[1]==1
    r, c = A.shape
    m = [[A.M[i][j] for j in range(c)] for i in range(r)]
    b = [[B.M[i][0]] for i in range(r)]
    for col in range(c):
        v = [math.fabs(row[col]) for row in m[col:]] #选出从第col行开始的第col列
        pivot = max(v)
        if pivot==0:
            return 0
        pivot_index = v.index(pivot)+col
        pivot = m[pivot_index][col]
        pivot_row = [x/pivot for x in m[pivot_index]]
        b_pivot_row = [x/pivot for x in b[pivot_index]]
        if pivot_index!=col:#行互换
            temp = m[col]
            m[col]=pivot_row
            m[pivot_index] =temp

            b_temp = b[col]
            b[col] = b_pivot_row
            b[pivot_index]=b_temp

        else:
            m[col] = pivot_row
            b[col] = b_pivot_row
        for i in range(r):
            if i!=col:
                k = m[i][col]
                #对应行相减
                m[i] = [ m[i][j]-k*pivot_row[j] for j in range(c)]
                b[i] = [b[i][0]-k*b[col][0]]
    return array(b)

if __name__ == '__main__':
    print("")

