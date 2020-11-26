def factors(m,n) :
   cf = []
   for i in range(1,min(m,n)+1) :
       if (m%i)==0 and (n%i) ==0:
           cf.append(i)
   print('Factors : ',cf)

def gcd(m,n):
   i = min(m,n)
   while i>0 :
      if (m%i)==0 and (n%i)==0 :
          return i
      else :
          i=i-1

ip1 = int(input('1st no. : '))
ip2 = int(input('2nd no. : '))
print('GCD : ',gcd(ip1,ip2))