import avl_tree as AVL

class Point:
  def __init__(self, x, y, ptype=0):
    self.x = x
    self.y = y
    self.ptype = ptype    #0 : left, 1 : right
    self.other_end = None
    self.order = 0
  
  def subtract(self, p):
    return Point(self.x - p.x, self.y - p.y)
  
  def __repr__(self):
    return '({}, {})'.format(self.x, self.y)

  def __lt__(self, other):
    '''if self.x < other.x:
      return True
    elif self.x > other.x:
      return False

    else:
      if self.ptype == other.ptype:
        if self.y < other.y:
          return True
        else:
          return False
      
      else:
        if self.ptype == 0:
          return True
        else:
          return False'''

    if self.order < other.order:
      return True
    else:
      return False

  def __gt__(self, other):
    '''if self.x > other.x:
      return True
    elif self.x < other.x:
      return False

    else:
      if self.ptype == other.ptype:
        if self.y > other.y:
          return True
        else:
          return False
      
      else:
        if self.ptype == 1:
          return True
        else:
          return False'''
    
    if self.order > other.order:
      return True
    else:
      return False

  def __eq__(self, other):
    if self.order == other.order:
      return True
    else:
      return False

  def set_other_end(self, oe):
    self.other_end = oe

def cross_product(p1, p2):
    return p1.x * p2.y - p2.x * p1.y

def direction(p1, p2, p3):
  return cross_product(p3.subtract(p1), p2.subtract(p1))

def left(p1, p2, p3):
  return direction(p1, p2, p3) < 0

def right(p1, p2, p3):
  return direction(p1, p2, p3) > 0

def collinear(p1, p2, p3):
  return direction(p1, p2, p3) == 0

def on_segment(p1, p2, p):
  return min(p1.x, p2.x) <= p.x <= max(p1.x, p2.x) and min(p1.y, p2.y) <= p.y <= max(p1.y, p2.y)

def intersect(p1, p2, p3, p4):
  d1 = direction(p3, p4, p1)
  d2 = direction(p3, p4, p2)
  d3 = direction(p1, p2, p3)
  d4 = direction(p1, p2, p4)

  if((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
    return True

  elif d1 == 0 and on_segment(p3, p4, p1):
    return True
  
  elif d2 == 0 and on_segment(p3, p4, p2):
    return True

  elif d3 == 0 and on_segment(p1, p2, p3):
    return True

  elif d4 == 0 and on_segment(p1, p2, p4):
    return True
  
  else:
    return False

def compare(p1, p2):
  if p1.x < p2.x:
    return -1
  elif p1.x > p2.x:
    return 1

  else:
    if p1.ptype == p2.ptype:
      if p1.y < p2.y:
        return -1
      else:
        return 1
    
    else:
      if p1.ptype == 0:
        return -1
      else:
        return 1

def any_segments_intersect(S):
  T = AVL.avl_tree()

  sortedS = sorted(S)
  #print([str(p) for p in sortedS])
  print(sortedS)
  i = 0

  for point in sortedS:
    i += 1
    if point.ptype == 0:
      point.order = i
      T.insert_node(point)
      prd = T.predecessor(point)
      if prd and intersect(point, point.other_end, prd.data, prd.data.other_end):
        #return True

        print("Line segments : {} and {} intersect".format(point, prd.data))
        swap_order(T, point, prd.data)
        prd1 = T.predecessor(prd.data)
        if prd1 and intersect(prd.data, prd.data.other_end, prd1.data, prd1.data.other_end):
          print("Line segments : {} and {} intersect".format(point, prd))
          #swap_order(T, prd.data, prd1.data)

      ssc = T.successor(point)
      if ssc and intersect(point, point.other_end, ssc.data, ssc.data.other_end):
        return True
      
      if point.ptype == 1:
        prd = T.predecessor(point)
        ssc = T.successor(point)

        if prd and ssc:
          if intersect(prd.data, prd.data.other_end, ssc.data, ssc.data.other_end):
            return True
        T.delete_a_node(point)
  
  # return False

def swap_order(T, p1, p2):
  # swap order
  #print(type(p2))
  (p1.order, p2.order) = (p2.order, p1.order)
  print(p1.order)
  #T.delete_a_node(p1)
  #T.insert_node(p1)

p1 = Point(4,2)
p2 = Point(2,5)
p3 = Point(-2,22)

p4 = Point(8, 25, 1)
p5 = Point(8, -2, 1)
p6 = Point(1, 2, 1)

p1.set_other_end(p4)
p2.set_other_end(p5)
p3.set_other_end(p6)

s1 = [p1, p2, p3, p4, p5, p6]
print(any_segments_intersect(s1))