CORAL = (242, 186, 111)
class Coral:
	def __init__(self):
		self.color = CORAL

	def getColor(self):
		return self.color

	def getClassName(self):
		return self.__class__.__name__