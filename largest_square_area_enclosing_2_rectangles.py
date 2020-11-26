# Given the length L and breadth B of two identical rectangles, the task is to find the minimum area of a square in which the two identical rectangles with dimensions L × B can be embedded

def areaSquare(l, b):
  large = max(l, b)  # Larger side of rectangle
  small = min(l, b)  # Smaller side of rectangle

  if(large >= 2 * small):
    return large ** 2

  else:
    return (2 * small) ** 2

print("\nRectangle details -->")
l = int(input("Enter length: "))
b = int(input("Enter breadth: "))

print("\nRequired square area : ", areaSquare(l, b))