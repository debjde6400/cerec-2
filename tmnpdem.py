import time
import numpy as np
sz = 1000

def pure_pyv():
   t1=time.time()
   x=range(sz)
   y=range(sz)
   z=[]
   for i in range(len(x)):
       z.append(x[i]+y[i])
   return time.time()-t1

def numpyv():
   t1 = time.time()
   x=np.arange(sz)
   y=np.arange(sz)
   z=x+y
   return time.time()-t1

t1=pure_pyv()
t2=numpyv()

print(t1,t2)
print('Difference : '+str(t1-t2))