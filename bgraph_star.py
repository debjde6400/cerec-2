n = int(input("Size ? : 3"))
arr = []

for i in range(n):
  arr.append(int(input("Enter : ")))

for num in arr:
  print("*" * num)