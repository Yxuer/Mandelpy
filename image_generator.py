from PIL import Image
from fractal import Fractal
from mpmath import *

class ImageGenerator:

	"""
	This class contains everything needed to render a Mandelbrot set
	or any similar fractal as an image.
	
	Attributes
	----------
	fract: Fractal
		The fractal used for rendering
	
	Methods
	-------
	generateImage(topLeftPoint = mpc(-2,2), bottomRightPoint = mpc(2,-2), realRes = 800, imgRes = 600)
		Returns an image of the Mandelbrot set in a given area at
		a given resolution
		
	"""
	
	def __init__(self, exponent = mpf(2), max_iters = 100, threshold = mpf(2)):
		"""
		Parameters
		----------
		exponent: mpf
			The exponent of the fractal (default: 2)
		
		max_iters: int
			The maximum number of iterations to run for each point (default: 100)
		
		threshold: mpf
			The maximum number at which a point will be considered to diverge (default: 2)
		"""
		self.fract = Fractal(exponent, max_iters, threshold)
		self.max_iters = max_iters
		
	def iterationsToColor(self, iters):
		"""
		Defines how a given pixel should be colored, according to the number of iterations
		taken for it to diverge
		
		Parameters
		----------
		iterations: int
			The number of iterations for the pixel to diverge
			
		Returns
		-------
		A 3-tuple with the RGB color of the pixel, in 0-255 format
		"""
		if (iters < 0):
			return (0,0,0)
		else:
			grayScaleColor = int((1 - (iters / self.max_iters)) * 255)
			return (grayScaleColor,grayScaleColor,grayScaleColor)
	
	def generateImage(self, topLeftPoint = mpc(-2,2), bottomRightPoint = mpc(2,-2), realRes = 800, imgRes = 600):
		"""
		Returns an image of the Mandelbrot set in a given area at
		a given resolution.
		
		Parameters
		----------
		topLeftPoint
			The complex number delimiting the top-left part of the image (default: mpc(-2,2))
			
		bottomRightPoint
			The complex number delimiting the bottom-right part of the image (default: mpc(2,-2))
			
		realRes
			Number of points to sample in the real axis (default: 800)
			
		imgRes
			Number of points to sample in the real axis (default: 600)
			
		
		Raises
		------
		TypeError
			If any of these conditions are met:
				- topLeftPoint or bottomRightPoint are not mpmath mpc numbers
				- realRes or imgRes are not integers
			
		ValueError
			If any of these conditions are met:
				- The real part of bottomRightPoint is smaller or equal than the real part of topLeftPoint
				- The imaginary part of bottomRightPoint is bigger or equal than the real part of topLeftPoint
				- Either realRes or imgRes are less or equal than zero
				
		"""
		
		if ((not isinstance(topLeftPoint, mpc)) or (not isinstance(bottomRightPoint, mpc))):
			raise TypeError("The complex limits are not mpc numbers")
			
		if ((not isinstance(realRes, int)) or (not isinstance(imgRes, int))):
			raise TypeError("The image resolution is not integer")
			
		if ((bottomRightPoint.real <= topLeftPoint.real) or (bottomRightPoint.imag >= topLeftPoint.imag)):
			raise ValueError("The bottom-right point is at the top left")
			
		if ((realRes <= 0) or (imgRes <= 0)):
			raise ValueError("The image resolution is zero or negative")
			
		# Create the image which will be painted
		img = Image.new("RGB", (realRes, imgRes), color = "black")
		pixels = img.load()
		
		for i in range(img.size[1]):
			for j in range(img.size[0]):
				realOffset = (bottomRightPoint.real - topLeftPoint.real) * (j / mpf(realRes))
				imgOffset = (-(bottomRightPoint.imag - topLeftPoint.imag)) * (i / mpf(imgRes))
								
				complexPoint = mpc(topLeftPoint.real + realOffset, topLeftPoint.imag - imgOffset)
				iters = self.fract.iterations(complexPoint)
				
				pixels[j,i] = self.iterationsToColor(iters)
					
				print("\rPixel (" + str(i) + "," + str(j) + ")", end = "")
		
		print("\n\nComplete!\n")
		return img