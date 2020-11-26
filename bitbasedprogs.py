def computeXOR(n):
  if(n % 4 == 0):
    return n
  elif (n % 4 == 1):
    return 1
  elif (n % 4 == 2):
    return n + 1
  else:
    return 0

def  setBit(n, pos):
  return n | (1 << pos)

def  unsetBit(n, pos):
  return n & ~(1 << pos)

def countSetBits(n):
  c = 0
  while(n != 0):
    n &= (n - 1)
    c += 1
  return c

print(computeXOR(99))
print(setBit(4,1))
print(unsetBit(7,1))
print(countSetBits(17))
