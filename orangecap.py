def orangecap(d):
  plst =[]
  high = ['',0]
  for mts in d.values():
    for pls in mts.keys():
       if pls not in plst:
          plst.append(pls)
          plst.append(mts[pls])
       else:
       	  plst[plst.index(pls)+1] += mts[pls]
    for tr in range(1,len(plst),2):
       if plst[tr]>high[1]:
          high[0] = plst[tr-1]
          high[1] = plst[tr]
  return (high[0],high[1])
