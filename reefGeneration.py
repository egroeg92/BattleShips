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
		#corallist = []	
		for x in range(24):
			coordinate = randCoord()
			corallist.append(coordinate)
		return corallist

def randCoord():
	tuple = ()
	x = random.randint(10,20)
	y = random.randint(3,27)
	tuple = (x,y)
	return tuple
