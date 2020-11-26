def gcd(m,n):
   #assume m>=n
   if m<n :
     (m,n) = (n,m)
   if (m%n)==0:
      return n
   else :
      diff = m-n
      #diff>n ? possible!
      return gcd(max(n,diff),min(n,diff))

ip1 = int(input('1 : '))
ip2 = int(input('2 : '))
print('\n', gcd(ip1,ip2)) 