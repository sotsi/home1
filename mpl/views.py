#from django.shortcuts import render

# Create your views here.
import django
import mpld3
# import Figure and FigureCanvas, we will use API
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# used to generate the graph
import numpy as np
def mplimage(request):
	# do the plotting
	fig = Figure()
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	x = np.arange(-2,1.5,.01)
	y = np.sin(np.exp(3*x))
	ax.plot(x, y)
	# prepare the response, setting Content-Type
	response=django.http.HttpResponse(content_type='image/png')
	# print the image on the response
	canvas.print_png(response)
	# and return it
	return response