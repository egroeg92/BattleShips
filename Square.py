class Square(object):
	def __init__(self, objectOn, position):
		self.objectOn = objectOn
		self.position = position
		self.visible = False
		self.activeRange = False
	
	def getObjectOn(self):
		return self.objectOn

	def getPosition(self):
		return self.position

	def setObjectOn(self, type):
		self.objectOn = type

	def setPosition(self, position):
		self.position = position

	def setVisible(self, visibility):
		self.visible = visibility
		
	def isVisible(self):
		return self.visible
	
	def setActiveRange(self, a):
		self.activeRange = a
	def isActiveRange(self):
		return self.activeRange