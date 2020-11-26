def alternating(lt):
	if lt==[]:
		return True
	el = lt[1]
	fl = (lt[0]>=lt[1])
	for i in range(2,len(lt)):
		if((el>=lt[i])==fl):
			return False
		el = lt[i]
		fl = not fl
	return True