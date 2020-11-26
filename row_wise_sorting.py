values = [[3, 4, 5, 1 ], [33, 6, 1, 2]]
for row in values:
  row.sort()
  for element in row:
    print(element, "", end="")
  print()
