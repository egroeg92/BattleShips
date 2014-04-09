from Tkinter import Tk
from tkFileDialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

if(filename[-4]+filename[-3]+filename[-2]+filename[-1] == '.bsh'):
	print(filename)