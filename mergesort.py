def merge(A,B):
	(C,m,n) = ([],len(A),len(B))
	(i,j) = (0,0)   #current positions in A,B
	
	while i+j <m+n :    #i+j is number of elements merged so far
		if i==m:
			C.append(B[j])
			j=j+1
		elif j==n:
			C.append(A[i])
			i=i+1
		elif A[i]<=B[j]:
			C.append(A[i])
			i=i+1
		elif A[i]>B[j]:
			C.append(B[j])
			j=j+1
	return (C)

def mergesort(A,left,right):
	if right-left<=1 : 
		return (A[left:right])
	
	if right-left>1:
		mid=(left+right)//2
		
		L=mergesort(A,left,mid)
		R=mergesort(A,mid,right)
		
		return (merge(L,R))
