from Tkinter import *

master = Tk()

def callback():
    print "click!"
    master.destroy()
def never():
	print "never!"
	master.destroy()
def button():

	b = Button(master, text="OK", command=callback)
	n = Button(master,text="NEVER!", command = never)
	b.pack(fill=BOTH,expand=1)
	n.pack(fill=BOTH,expand =1)
	master.mainloop()
	
if __name__ == '__main__':
	
	button()
