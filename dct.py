def dictgen(num):
    dict_nm = {}
    for i in range(1,num+1):
        for j in range(i-1,0,-1):
            if(i%j==0):
                dict_nm[i]=j
                break
    return dict_nm

def getprim(dict_nm):
    prim=[]
    for no in dict_nm:
       if dict_nm[no]==1 :
          prim.append(no)
    print(prim.sort())
	
def getcpd2r(dict_nm):
    cpd2r =[]
    for no in dict_nm:
        if dict_nm[dict_nm[no]]!=1 :
          cpd2r.append(no)
    print(cpd2r.sort())

print(dictgen(10))