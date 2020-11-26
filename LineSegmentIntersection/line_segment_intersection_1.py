import matplotlib.pyplot as plt
import avl_tree

class LineSegment:
  def __init__(self, p1, p2, name):
    self.end_points = [p1, p2]
    self.name = name
    self.end_points.sort()
    self.sweep_line_y = None

  def print_points(self):
    print("Line segment ", self.name, " starts from ", self.end_points[0], " and ends at ", self.end_points[1])
  
  def get_coefficients(self):
    m = (self.end_points[1][1] - self.end_points[0][1]) / (self.end_points[1][0] - self.end_points[0][0])
    c = self.end_points[0][1] - m * self.end_points[0][0]
    return (m, c)

  def get_line(self):
    m, c = self.get_coefficients()
    return lambda x : m * x + c

  def plot_points(self):
    plt.plot(*zip(*self.end_points), marker='o')

  def set_sweep_line_value(self, sweep_line_x):
    if(sweep_line_x >= self.end_points[0][0] and sweep_line_x <= self.end_points[1][0]): 
      self.sweep_line_y = self.get_line()(sweep_line_x)
      plt.plot(sweep_line_x, self.sweep_line_y, marker='o', color='m')

ls1 = LineSegment((8,25), (4,2), "ls1")
ls2 = LineSegment((2,5), (8,-2), "ls2")
ls3 = LineSegment((-2,22), (1,2), "ls3")

ls1.print_points()
ls1_m = ls1.get_coefficients()[0]

print("Slope of ls1 : ", ls1_m)
print(ls1.get_line()(8))
ls1.plot_points()
ls2.plot_points()
ls3.plot_points()

sweep_line_x = 6

plt.axvline(x = sweep_line_x, ls='--', color='m')
ls1.set_sweep_line_value(sweep_line_x)
ls2.set_sweep_line_value(sweep_line_x)
ls3.set_sweep_line_value(sweep_line_x)

plt.show()

'''t1 = (3, 5)
t2 = (3, 2)

if (t1 < t2):
  print(t1)
else:
  print(t2)

event_queue = []

def remove_min(p_queue):
  min_el = min(p_queue)
  p_queue.remove(min_el)

q = [6, 9, 1, 43, 76]
remove_min(q)
print(q)'''