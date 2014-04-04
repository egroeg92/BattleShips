class Square(object):
	def __init__(self, objectOn, position):
		self.objectOn = objectOn
		self.position = position
		self.visible = False
		self.activeRange = False
		self.sonarVisible = False
	
	def getObjectOn(self):
		return self.objectOn

	def getPosition(self):
		return self.position

	def setObjectOn(self, type):
		self.objectOn = type

	def removeObjectOn(self):
		self.objectOn = None

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

	def isSonarVisible(self):
		return self.sonarVisible

	def setSonarVisible(self, visibility):
		self.sonarVisible = visibility
		