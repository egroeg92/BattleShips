class Weapon(object):
	def __init__(self, damage, rangeX, rangeY):
		self.damage = damage
		self.rangeX = rangeX
		self.rangeY = rangeY
		self.selected = False

	# Gets the class name
	def getName(self):
		return self.__class__.__name__
	
	def getDamage(self):
		return self.damage
	
	def getRangeX(self):
		return self.rangeX
	
	def getRangeY(self):
		return self.rangeY

class Cannon(Weapon):
	def __init__(self, damage, rangeX, rangeY):
		Weapon.__init__(self, damage, rangeX, rangeY)
		
	def getClass(self):
		return "cannon"

class Explosive(Weapon):
	def __init__(self, damage, rangeX, rangeY):
		Weapon.__init__(self, damage, rangeX, rangeY)
	def getClass(self):
		return "explosive"
	
class HeavyCannon(Weapon):
	def __init__(self, damage, rangeX, rangeY):
		Weapon.__init__(self, damage, rangeX, rangeY)
	def getClass(self):
		return "heavycannon"
	
class Torpedo(Weapon):
	def __init__(self, damage, rangeX, rangeY):
		Weapon.__init__(self, damage, rangeX, rangeY)
	def getClass(self):
		return "torpedo"
class Mine(Weapon):
	def __init__(self, damage, rangeX, rangeY, position):
		Weapon.__init__(self, damage, rangeX, rangeY)	
		self.position = position
	def getClass(self):
		return "mine"
	def getPosition(self):
		return self.position