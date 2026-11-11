import numpy as np
import spatialmath as sm


#Numpy方法
p1 = np.array([[3],
              [1],
              [5]])
p2 = np.array([[2],
               [6],
               [9]])
s1 = np.sin(np.pi/6)
c2 = np.cos(np.pi/3)
p3 = s1 * p1 + c2 * p2
print("p3 = \n",p3)

v = np.array([[1],[2],[3]])
M = np.array([[1,2,3],
              [4,5,6],
              [7,8,10]])
#标量乘法
res1 = 2*v
print("res1 = \n",res1)
#矩阵*向量
res2 = M@v
print("res2 = \n",res2)
#矩阵*矩阵
res3 = M@M
print("res3 = \n",res3)

#转置
v_T = v.T
M_T = M.T
print("v_T = \n",v_T)
print("M_T = \n",M_T)

#dot product
dot = p1.T @ p2
print("dot = \n",dot)

a = np.array([1,2,3])
b = np.array([4,5,6])
dot = np.dot(a,b)
print("dot = \n",dot)
#cross product
cross = np.cross(p1,p2,axis=0)
print("cross = \n",cross)
#Inverse 
M_inv = np.linalg.inv(M)
print("M_inv = \n",M_inv)