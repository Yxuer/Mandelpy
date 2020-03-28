from image_generator import ImageGenerator
from tkinter import *
from mpmath import *
from PIL import Image, ImageTk

class Visualizer:
	"""This class contains the attributes and methods needed to
	render a fractal in a TKInter window
	
	Attributes
	----------
	gui: Tk
		The window in which the canvas containing the fractal will
		be drawn
		
	canvas: Canvas
		The region which will contain the drawn fractal
		
	generator: ImageGenerator
		The fractal image generator
		
	topLeftPoint: mpc
		The top-left complex number in the drawing canvas
		
	bottomRightPoint: mpc
		The bottom-right complex number in the drawing canvas
		
	realRes: int
		The number of points to sample in the horizontal axis (real axis)
		
	imgRes: int
		The number of points to sample in the vertical axis (imaginary axis)
		
	Methods
	-------
	draw()
		Draws the fractal in the canvas of the main window
	
	"""
	
	def __init__(self, exponent = mpf(2), max_iters = 100, threshold = mpf(2)):
		"""Initialises the GUI and the canvas in which to draw
		the fractal, apart from initializing the drawing limits
		and resolution parameters
		
		Parameters
		-------------
		exponent: mpf
			The exponent of the fractal (default: 2)
		
		max_iters: int
			The maximum number of iterations to run for each point (default: 100)
		
		threshold: mpf
			The maximum number at which a point will be considered to diverge (default: 2)
		
		"""
		
		self.gui = Tk()
		self.gui.geometry("800x800")
		self.canvas = Canvas(self.gui, width = 800, height = 800)
		self.canvas.pack()
		self.generator = ImageGenerator(exponent, max_iters, threshold)
		
		self.topLeftPoint = mpc(-2,2)
		self.bottomRightPoint = mpc(2,-2)
		self.realRes = 800
		self.imgRes = 800
		
	def draw(self):
		"""Draws the fractal in the canvas of the main window
		
		Parameters
		----------
		None
		
		"""
		#image = self.generator.generateImage(self,topLeftPoint,
		#									 self.bottomRightPoint,
		#									 self.realRes,
		#									 self.imgRes)

		image = Image.open("test.png")
		
		image = ImageTk.PhotoImage(image)
		
		currentImage = self.canvas.create_image(int(self.realRes / 2), 
										   int(self.imgRes / 2), 
										   image = image)
		
		self.gui.mainloop()
		

if (__name__ == "__main__"):
	
	window = Visualizer()
	window.draw()
		
		
	