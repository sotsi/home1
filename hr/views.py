from django.shortcuts import render

# Create your views here.
import django
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import mpld3
from mpld3 import plugins, utils
# import Figure and FigureCanvas, we will use API
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# used to generate the graph
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt, mpld3

#####################################
np.random.seed(0)
n_size=7
P = np.random.random(size=n_size)
P[0]=6000
P[1]=3313
P[2]=6125
P[3]=3300
P[4]=5445
#P[5]=5500
P[5]=6151
P[6]=5700
#P[7]=7000

A = np.random.random(size=n_size)
A[0]=2000
A[1]=4168
A[2]=50
A[3]=3000
A[4]=3200
#A[5]=2900
A[5]=1186
A[6]=565
#A[7]=2440
			
T = ["%.2f" % x for x in A]
T[0]='Cepheus - delta Cephei'
T[1]='Lyra - R Lyrae'
T[2]='Lyra - RR Lyrae'
T[3]='Lepus - RX Leponis'
T[4]='Dorado - beta Doradus'
#T[5]='Gemini - zeta Geminorum'
T[5]='Auriga - RT Aurigae'
T[6]='Pavo - x Pavonis'
#T[7]='Polaris - alpha Ursa Minoris'
# The period of variables
C = np.random.random(size=n_size)
C[0]=5.3
C[1]=46
C[2]=0.57
C[3]=60
C[4]=9.84
#C[5]=10.15
C[5]=3.73
C[6]=9.09
#C[7]=3.97
# The magnitude variation
D = np.random.random(size=n_size)
D[0]=1.1
D[1]=1.1
D[2]=1
D[3]=2.4
D[4]=0.6
#D[5]=0.6
D[5]=0.8
D[6]=0.9
#D[7]=0.3
	
# The magnitude mean value
E = np.random.random(size=n_size)
E[0]=3.5
E[1]=3.9
E[2]=7.06
E[3]=5
E[4]=3.46
#E[5]=3.62
E[5]=5
E[6]=3.91
#E[7]=1.86
#####################################
def post_list(request):
	return render(request, 'blog/my_plot.html')
	
def mplimage(request):

	class LinkedView(plugins.PluginBase):
		"""A simple plugin showing how multiple axes can be linked"""

		JAVASCRIPT = """
		mpld3.register_plugin("linkedview", LinkedViewPlugin);
		LinkedViewPlugin.prototype = Object.create(mpld3.Plugin.prototype);
		LinkedViewPlugin.prototype.constructor = LinkedViewPlugin;
		LinkedViewPlugin.prototype.requiredProps = ["idpts", "idline", "data"];
		LinkedViewPlugin.prototype.defaultProps = {}
		function LinkedViewPlugin(fig, props){
			mpld3.Plugin.call(this, fig, props);
		};

		LinkedViewPlugin.prototype.draw = function(){
		  var pts = mpld3.get_element(this.props.idpts);
		  var line = mpld3.get_element(this.props.idline);
		  var data = this.props.data;

		  function mouseover(d, i){
			line.data = data[i];
			line.elements().transition()
				.attr("d", line.datafunc(line.data))
				.style("stroke", this.style.fill);
		  }
		  pts.elements().on("mouseover", mouseover);
		};
		"""
		def __init__(self, points, line, linedata):
			if isinstance(points, matplotlib.lines.Line2D):
				suffix = "pts"
			else:
				suffix = None

			self.dict_ = {"type": "linkedview",
						  "idpts": utils.get_id(points, suffix),
						  "idline": utils.get_id(line),
						  "data": linedata}
	
	fig, ax = plt.subplots(2)#fig = plt.figure(figsize=(8,6))
	#plt.plot([1,2,3,4])
	fig, ax = plt.subplots(2)

	
	
	# THE VARIABLE STAR ARRAY... 
	# TITLE/TEMPERATURE/LUMINOCITY/PERIOD/MINIMUM MAGNITUDE/MAGNITUDE VARIATION
	variables_array = zip(T,P,A,C,D,E) #
	
	x = np.linspace(0, 1000, 10000)
	data = np.array([[x, Ei + Di/2 + Di * np.sin((2*math.pi*x) / Ci)]
					 for (Ei, Di, Ci) in zip(E, D, C)])
	points = ax[0].scatter(P, A, c=1/(P), s=200, alpha=0.5)
	
	# stable ax[0].annotate('(%s, %s, %s)' % xy, xy=(xy[0],xy[1]), textcoords='data')
	for xy in zip(P, A, T):                        
		ax[0].annotate('(%s)' % xy[2], xy=(xy[0]-100,xy[1]), textcoords='data')
					
	
	ax[0].set_xlabel('Temperature (K)', size=15)
	ax[0].set_ylabel('Luminocity (x Lsun)', size=15)
	ax[0].set_title('', size=0)
	ax[0].set_xlim(2000, 6500)
	ax[0].invert_xaxis()
	# create the line object
	lines = ax[1].plot(x, 0 * x, '-w', lw=3, alpha=0.5)
	ax[1].set_ylim(0, 10)
	ax[1].set_xlim(0, 60)
	ax[1].set_ylabel('Absolute Magnitude', size=15)
	ax[1].set_xlabel('Time (days)', size=15)
	ax[0].set_title("HR Diagram - Instability Strip (Hover over points to see magnitude variation)")
	#ax[1].invert_yaxis()
	
	# transpose line data and add plugin
	linedata = data.transpose(0, 2, 1).tolist()
	plugins.connect(fig, LinkedView(points, lines[0], linedata))
		
	g = mpld3.fig_to_html(fig)
	mpld3.save_html(fig, "hr/templates/inst_strip.html")
	
	return django.http.HttpResponse(g)
	
def mplimage1(request):

	# Define some CSS to control our custom labels
	css = """
	table
	{
	  border-collapse: collapse;
	}
	th
	{
	  color: #ffffff;
	  background-color: #000000;
	}
	td
	{
	  background-color: #cccccc;
	}
	table, th, td
	{
	  font-family:Terminal, Arial, Helvetica, sans-serif;
	  border: 2px solid black;
	  text-align: right;
	}
	"""
	
	np.random.seed(0)
		
	P = np.random.random(size=9)
	P[0]=6000
	P[1]=3313
	P[2]=6125
	P[3]=3300
	P[4]=5445
	P[5]=5500
	P[6]=6151
	P[7]=5700
	P[8]=7000

	A = np.random.random(size=9)
	A[0]=2000
	A[1]=4168
	A[2]=50
	A[3]=3000
	A[4]=3200
	A[5]=2900
	A[6]=1186
	A[7]=565
	A[8]=2440
				
	T = ["%.2f" % x for x in A]
	T[0]='Cepheus - delta Cephei'
	T[1]='Lyra - R Lyrae'
	T[2]='Lyra - RR Lyrae'
	T[3]='Lepus - RX Leponis'
	T[4]='Dorado - beta Doradus'
	T[5]='Gemini - zeta Geminorum'
	T[6]='Auriga - RT Aurigae'
	T[7]='Pavo - x Pavonis'
	T[8]='Polaris - alpha Ursa Minoris'
	# The period of variables
	C = np.random.random(size=9)
	C[0]=5.3
	C[1]=46
	C[2]=0.57
	C[3]=60
	C[4]=9.84
	C[5]=10.15
	C[6]=3.73
	C[7]=9.09
	C[8]=3.97
	# The magnitude variation
	D = np.random.random(size=9)
	D[0]=1.1
	D[1]=1.1
	D[2]=1
	D[3]=2.4
	D[4]=0.6
	D[5]=0.6
	D[6]=0.8
	D[7]=0.9
	D[8]=0.3
		
	# The magnitude mean value
	E = np.random.random(size=9)
	E[0]=3.5
	E[1]=3.9
	E[2]=7.06
	E[3]=5
	E[4]=3.46
	E[5]=3.62
	E[6]=5
	E[7]=3.91
	E[8]=1.86
	
	fig, ax = plt.subplots()

	########### INSTABILITY AREA ###########
	# scatter periods and amplitudes
	
	######## END OF INSTABILITY AREA #######

	ax.grid(True, alpha=0.3)

	star_array = [  
					['Sirius B', 25200, 0.056], 
					['Procyon B', 7740, 0.00049],
					['LP 145-141', 8500, 0.0005],
					['Van Maanen 2', 6220, 0.00017],
				 ]
	#N = len(star_array)
	N = len(P)
	df = pd.DataFrame(index=range(N), columns=['Name','Temperature','Luminocity','Period','Magnitude Variation'])

	xy=zip(T,P,A,C,D)
	i=0
	while (i<N):
		#df.loc[i] = [star_array[i][0],star_array[i][1],star_array[i][2]]
		df.loc[i] = [xy[i][0],xy[i][1],xy[i][2],xy[i][3],xy[i][4]]
		i=i+1

	labels = []
	for c in range(N):
		label = df.ix[[c], :].T
		label.columns = ['Star {0}'.format(c)]
		# .to_html() is unicode; so make leading 'u' go away with str()
		labels.append(str(label.to_html()))
		

	#df.at[0,'A'] // points = ax.plot(df.Temperature, df.Luminocity, 'o', color=( 1.0, 1.0, 1.0 ), mec='k', ms=15, mew=1, alpha=.6)
	points = ax.plot(df.Temperature, df.Luminocity, 'o', color=( 1.0, 0.0, 0.0 ), mec='k', ms=15, mew=1, alpha=.6)


	#ax.set_xscale('log')
	ax.set_xlim(3000, 7100)
	ax.invert_xaxis()
	ax.set_xlabel('Temperature', size=15)
	#ax.set_yscale('log')
	ax.set_ylabel('Luminocity', size=15)
	ax.set_title('', size=0)
	ax.set_ylim(3-1000, 5000)
	#ax.text(9000, 0.01, 'Instability Strip', style='italic', bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
	ax.set_title("HR Diagram - Instability Strip (Hover over points to see characteristics)")

	tooltip = plugins.PointHTMLTooltip(points[0], labels, voffset=10, hoffset=10, css=css)
	plugins.connect(fig, tooltip)
		
	g = mpld3.fig_to_html(fig)
	mpld3.save_html(fig, "hr/templates/hr_full.html")
	
	return django.http.HttpResponse(g)