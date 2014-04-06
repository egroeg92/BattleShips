import random
class reefGeneration(object):
	def __init__(self):
		self.reef = "Reef"
	def random(self):
		tuple = ()
		x = random.randint(10,13)
		y = random.randint(3,26)
		tuple = (x,y)
		return tuple
	def randommid(self):
		tuple = ()
		x = random.randint(14,14)
		y = random.randint(3,26)
		tuple = (x,y)
		return tuple
	def randommid2(self):
		tuple = ()
		x = random.randint(15,15)
		y = random.randint(3,26)
		tuple = (x,y)
		return tuple		
	def random2(self):
		tuple = ()
		x = random.randint(16,19)	 
		y = random.randint(3,26)
		tuple = (x,y)
		return tuple		
	def reefCoordinates(self, corallist):
		corallist = []	
		#for x in range(24):
		#	coordinate = randCoord()
		#	corallist.append(coordinate)
		#return corallist
		
		i = 0
		j = 0
		k = 0
		l = 0
		while i != 11:
		    coordinate = randCoord()
		    if coordinate not in corallist:
		        corallist.append(coordinate)
		        i = i + 1 
		print "RLength of corallist is: ", len(corallist)                
		while j != 1:
			coordinate = randCoord2()
			if coordinate not in corallist:
				corallist.append(coordinate)
				j = j + 1
		print "RLength of corallist is: ", len(corallist)
		while k != 1:
			coordinate = randCoord3()
			if coordinate not in corallist:
				corallist.append(coordinate)
		        k = k + 1
		print "RLength of corallist is: ", len(corallist)
		while l != 11:
		    coordinate = randCoord4()
		    if coordinate not in corallist:
		        corallist.append(coordinate)
		        l = l + 1
		print "RLength of corallist is: ", len(corallist)		
		print "The corallist is now: ", corallist
		return corallist
#def randCoord():
#	tuple = ()
#	x = random.randint(10,20)
#	y = random.randint(3,27)
#	tuple = (x,y)
#	return tuple
def randCoord():
	tuple = ()
	x = random.randint(10,13)
	y = random.randint(3,26)
	tuple = (x,y)
	return tuple
def randCoord2():
	tuple = ()
	x = random.randint(14,14)
	y = random.randint(3,26)
	tuple = (x,y)
	return tuple		
def randCoord3():
	tuple = ()
	x = random.randint(15,15)
	y = random.randint(3,26)
	tuple = (x,y)
	return tuple
def randCoord4():
	tuple = ()
	x = random.randint(16,19)	 
	y = random.randint(3,26)
	tuple = (x,y)
	return tuple