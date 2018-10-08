

def extrLst2(stiv) :
	if(len(stiv)/2<len(stiv)):
		return stiv[len(stiv)/2:len(stiv):1]

def extrLst1(stiv) :
	if(0<len(stiv)/2):
		return stiv[0:len(stiv)/2:1]
a = [1,2,3,4 ,5, 6, 7, 8, 9, 10, 11, 12]
	
stiv=[a]
while (stiv):
	ar=stiv.pop()
	if((((extrLst2(ar))) != None) and len(extrLst1(ar))==1) :
		print(extrLst1(ar)) 

	
	if((((extrLst2(ar))) != None) and len(extrLst2(ar))==1) :
		print(extrLst2(ar)) 


	if(len(extrLst1(ar))>1) :
		stiv.append(extrLst1(ar))
	if(len(extrLst2(ar))>1) :
		stiv.append(extrLst2(ar))


		









