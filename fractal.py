from mpmath import *

class Fractal:

	"""
	This class contains all the variables and methods needed to
	calculate if a given complex number belongs to a point in a
	Mandelbrot set or any fractal with a different exponent
	
	...
	
	Attributes
	----------
	
	exponent: mpf
		The exponent of the fractal (default: 2)
		
	max_iters: int
		The maximum number of iterations to run for each point (default: 100)
		
	threshold: mpf
		The maximum number at which a point will be considered to diverge (default: 2)
	
	Methods
	-------
	iterations(point = None)
		Returns the number of iterations for the point to diverge,
		or -1 if it doesn't diverge
		

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
		
		Raises
		------
		TypeError
			If the exponent or the threshold are not mpmath mpf numbers
			
		"""
				
		if ((not isinstance(exponent, mpf)) or (not isinstance(threshold, mpf))):
			raise TypeError("Both the exponent and the threshold must be mpf numbers")
		
		self.exponent = exponent
		self.max_iters = max_iters
		self.threshold = threshold
		
	def iterations(self, point = None):
		"""
		Returns the number of iterations for the given "point" to diverge,
		or -1 if it doesn't diverge in the limit of iterations specified by
		"max_iters". The point is considered to diverge if, at any given 
		iteration, the absolute value of the number exceeds "threshold".
		
		Parameters
		----------
		point: mpc
			The complex point to test (default: None)
			
		Raises
		------
		TypeError
			If the complex point is not passed as a mpmath mpc
			
		"""
		
		if (not isinstance(point, mpc)):
			raise TypeError("The complex point must be a mpc number")
		
		sequence_value = mpc(0,0)
		
		for i in range(self.max_iters):
			sequence_value = (sequence_value ** self.exponent) + point
			if (fabs(sequence_value) > self.threshold):
				return i
		
		return -1