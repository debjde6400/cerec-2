import matplotlib.pyplot as plt

def orientation(p, q, r):
    return ((q[0] - p[0])*(r[1] - p[1])) - ((q[1] - p[1])*(r[0] - p[0]))

def grahams_scan(pt):
  hull = []
  hull.append(pt[0])
  hull.append(pt[1])
  top = 1

  for i in range(2, len(pt)):
    while((len(hull) > 2) and (orientation(pt[i], hull[top], hull[top-1]) < 0)):
      hull.pop()
      top -= 1

    hull.append(pt[i])
    top += 1

  return hull

points = [(8,5), (7,3), (6,1), (6,6), (5,8), (4,4), (3,1), (3,5), (2,2), (2,6), (1,4)]
plt.scatter(*zip(*points))

all_ys= list(zip(*points))[1]
mid_y = (max(all_ys) - min(all_ys)) // 2

upper_set = sorted([(x, y) for (x, y) in points if y > mid_y ])
lower_set = sorted([(x, y) for (x, y) in points if y <= mid_y ], reverse=True)

print(lower_set)
print(upper_set)

upper_hull = grahams_scan(upper_set)
lower_hull = grahams_scan(lower_set)

convex_hull = upper_hull + lower_hull

print("\nFinal Hull : ", convex_hull)
plt.fill(*zip(*convex_hull), fill=False)
plt.show()