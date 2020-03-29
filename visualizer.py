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
	
	def __init__(self, exponent = mpf(2), max_iters = 100, threshold = mpf(2), resolution = (800,800)):
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
		
		resolution: tuple(int,int)
			The width and height of the render space
		
		"""
		
		self.gui = Tk()
		self.gui.geometry("" + str(resolution[0]) + "x" + str(resolution[1]))
		self.canvas = Canvas(self.gui, width = resolution[0], height = resolution[1])
		self.canvas.pack()
		self.generator = ImageGenerator(exponent, max_iters, threshold)
		
		self.topLeftPoint = mpc(-2,2)
		self.bottomRightPoint = mpc(2,-2)
		self.realRes = resolution[0]
		self.imgRes = resolution[1]
		
		def center_image_callback(event):
			"""Callback for clicking somewhere inside the fractal image.
			This will set the center to wherever the click was made
			"""
			
			# Calculate the complex number corresponding to the point that was clicked
			realRelativePos = mpf(event.x) / mpf(self.realRes)
			imgRelativePos = mpf(event.y) / mpf(self.imgRes)
			realOffset = realRelativePos * (self.bottomRightPoint.real - self.topLeftPoint.real)
			imgOffset = imgRelativePos * -(self.bottomRightPoint.imag - self.topLeftPoint.imag)
			realNewCenter = self.topLeftPoint.real + realOffset
			imgNewCenter = self.topLeftPoint.imag - imgOffset
			
			# Calculate the current center and apply the (new - current) transform to the corners
			realCurrentCenter = (self.bottomRightPoint.real + self.topLeftPoint.real) / 2
			imgCurrentCenter = (self.bottomRightPoint.imag + self.topLeftPoint.imag) / 2
			absoluteDisplacement = mpc(realNewCenter, imgNewCenter) - mpc(realCurrentCenter, imgCurrentCenter)
			self.topLeftPoint = self.topLeftPoint + absoluteDisplacement
			self.bottomRightPoint = self.bottomRightPoint + absoluteDisplacement
			self.draw()
		
		self.canvas.bind("<Button-1>", center_image_callback)
		
		
	def draw(self):
		"""Draws the fractal in the canvas of the main window
		
		Parameters
		----------
		None
		
		"""
		image = self.generator.generateImage(self.topLeftPoint,
											 self.bottomRightPoint,
											 self.realRes,
											 self.imgRes)
		
		image = ImageTk.PhotoImage(image)
		
		currentImage = self.canvas.create_image(int(self.realRes / 2), 
										   int(self.imgRes / 2), 
										   image = image)
		
		self.gui.mainloop()
		

if (__name__ == "__main__"):
	
	window = Visualizer(max_iters = 5, resolution = (400,400))
	window.draw()
		
		
	