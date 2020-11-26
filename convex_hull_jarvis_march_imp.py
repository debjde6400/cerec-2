import matplotlib.pyplot as plt

def orientation(p, q, r):
    return ((q[0] - p[0])*(r[1] - p[1])) - ((q[1] - p[1])*(r[0] - p[0]))

def right_index(pt):
  rt = 0

  for i in range(1, len(pt)):
    if pt[i][0] < pt[rt][0]:
      rt = i

    elif pt[i][0] == pt[rt][0]:
      if pt[i][1] > pt[rt][1]:
        rt = i
  
  return rt

def jarvis_march(pt):
  hull = []
  n = len(pt)
  right_most = right_index(pt)
  p = right_most
  r = 0

  while True:
    hull.append(pt[p])
    r = (p + 1) % n

    for q in range(n):
      if(q != p and q != r and orientation(pt[p], pt[q], pt[r]) > 0):
        r = q
    
    p = r
    if(p == right_most):
      break

  #print(right_most)
  return hull

points = [(8,5), (7,3), (6,1), (6,6), (5,8), (4,4), (3,1), (3,5), (2,2), (2,6), (1,4)]
plt.scatter(*zip(*points))

convex_hull = jarvis_march(points)

print("\nFinal Hull : ", convex_hull)
plt.fill(*zip(*convex_hull), fill=False)
plt.show()