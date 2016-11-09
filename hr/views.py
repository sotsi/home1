from django.shortcuts import render

# Create your views here.
import django
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rcParams
import matplotlib.transforms as mtransforms
from matplotlib.patches import Ellipse
from matplotlib.font_manager import FontProperties
matplotlib.rcParams.update({'font.size': 12})
matplotlib.rcParams.update({'font.family': 'Courier'})
import numpy as np
import math
import mpld3
from mpld3 import plugins, utils
# import Figure and FigureCanvas, we will use API
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# used to generate the graph
import pandas as pd
import matplotlib.pyplot as plt, mpld3
matplotlib.rc('font', family='Segoe Print')
#####################################
csfont = {'fontname':'Comic Sans MS'}
np.random.seed(0)
n_size=6
nsize=8

################# DEFINE STAR PARAMETERS ONCE MORE ################
Temperature = np.random.random(size=nsize)
Temperature[0]=12100
Temperature[1]=8525
Temperature[2]=3590
Temperature[3]=3400
Temperature[4]=25200
Temperature[5]=5777
Temperature[6]=9940
Temperature[7]=16500
#Temperature[8]=6550
#Temperature[8]=22400
## calculate the star color
N = len(Temperature)
Color = ["" for x in range(N)]
i=0
while i<N:
	if Temperature[i]>20000:
		Color[i]='royalblue'
	elif Temperature[i]>15000:
		Color[i]='dodgerblue'
	elif Temperature[i]>10000:
		Color[i]='deepskyblue'
	elif Temperature[i]>9000:
		Color[i]='cyan'
	elif Temperature[i]>8000:
		Color[i]='aquamarine'
	elif Temperature[i]>7000:
		Color[i]='lightcyan'
	elif Temperature[i]>6000:
		Color[i]='lawngreen'
	elif Temperature[i]>5500:
		Color[i]='greenyellow'
	elif Temperature[i]>5000:
		Color[i]='orange'
	elif Temperature[i]>4000:
		Color[i]='coral'
	elif Temperature[i]>3500:
		Color[i]='orangered'
	elif Temperature[i]>3000:
		Color[i]='red'
	else: Color[i]='black'
	i=i+1
	
Luminocity = np.random.random(size=nsize)
Luminocity[0]=120000
Luminocity[1]=200000
Luminocity[2]=120000
Luminocity[3]=57500
Luminocity[4]=0.056
Luminocity[5]=1
Luminocity[6]=25.4
Luminocity[7]=0.013
#Luminocity[8]=1000
#Luminocity[8]=12100

Radius = np.random.random(size=nsize)
Radius[0]=79
Radius[1]=203
Radius[2]=900
Radius[3]=883
Radius[4]=0.084
Radius[5]=1
Radius[6]=1.7
Radius[7]=0.014
#Radius[8]=70
#Radius[8]=6

i=0
while i<N:
	if Radius[i]>800:
		Radius[i]=100
	elif Radius[i]>200:
		Radius[i]=60
	elif Radius[i]>50:
		Radius[i]=50
	elif Radius[i]>30:
		Radius[i]=30
	elif Radius[i]>0.1:
		Radius[i]=15
	elif Radius[i]>0.01:
		Radius[i]=1
	else: Radius[i]=0.5
	i=i+1


Name = ["" for x in range(N)]
Name[0]='Rigel - the brightest star in Orion'
Name[1]='Deneb - the brightest star in Cygnus'
Name[2]='Betelgeuse - the 2d brightest star in Orion'
Name[3]='Antares - the brightest star in Scorpius'
Name[4]='Sirius B - the white dwarf companion of Sirius A'
Name[5]='Sun - our star which gives life to Earth'
Name[6]='Sirius A - the brightest star in our night sky'
Name[7]='40 Eridani B - the 1st discovered white dwarf'
#Name[8]='R Scuti'
#Name[8]='Bellatrix'
################# 		END OF DEFINITIONS 		   ################

def post_list(request):
	return render(request, 'blog/my_plot.html')

def mplimage(request):

	fig, ax = plt.subplots(subplot_kw=dict(axisbg='gainsboro'),figsize=(18,8), dpi=40)
	N = len(Temperature)
	df = pd.DataFrame(index=range(N), columns=['Name','Temperature','Luminocity','Radius','Color'])
	font0 = FontProperties()
	font0.set_size(15)
	xy=zip(Name,Temperature,Luminocity,Radius,Color)
	i=0
	while (i<N):
		df.loc[i] = [xy[i][0],xy[i][1],xy[i][2],xy[i][3],xy[i][4]]
		i=i+1
	
	labels = []
	for c in range(N):
		label = xy[c][0]#df.ix[[c], 0].T
		#label.columns = ['Star {0}'.format(c)]
		# .to_html() is unicode; so make leading 'u' go away with str()
		labels.append(str(label))
	
	el = Ellipse((8000, 120000), 30000, 150000, facecolor='coral', angle = 0, alpha=0.2, edgecolor="#0000ff")
	ax.add_patch(el)
	el1 = Ellipse((20750, 0), 10000, 100000, facecolor='deepskyblue', angle = 0, alpha=0.2, edgecolor="#0000ff")
	ax.add_patch(el1)
	#el1 = Ellipse((8000, 22000), 15000, 5000, angle=-250 , facecolor='cyan', alpha=0.2, edgecolor="#0000ff")
	#ax.add_patch(el1)
	#ax.add_artist(el)
    #el.set_clip_box(ax.bbox)
	x = np.arange(1000, 25000, 500)
	y1 = 4.6*x - 16111#5555 #1.851
	y2 = 4.6*x - 41111#11111
	z = np.arange(5000, 9000, 100)
	y3 = -19.493*z+140000
	y4 = -19.493*z+170000
	ax.fill_between(x, y1, y2, facecolor='lawngreen', alpha=0.2)
	#ax.annotate(s='', xy=(10000,50000), xytext=(10000,100000), arrowprops=dict(arrowstyle='fancy'))
	#ax.fill_between(z, y3, y4, facecolor='orchid', alpha=0.2)
	#ax.annotate('fancy', xytext=(10000, 50000), xy=(15000, 100000),arrowprops=dict(arrowstyle='fancy'));
	bbox_props = dict(boxstyle="round,pad=0.7", fc="cyan", ec="b", lw=2)
	t = ax.text(18000, 120000, "Super Giant Region", ha="center", va="center", rotation=0, size=12, bbox=bbox_props)
	t1 = ax.text(14000, 35000, "Main Sequence", ha="center", va="center", rotation=-11, size=12, bbox=bbox_props)
	t2 = ax.text(21000, -0, "White Dwarf Region", ha="center", va="center", rotation=0, size=12, bbox=bbox_props)
	t3 = ax.text(22500, 220000, "L(xLsun) vs T(K)", ha="center", va="center", rotation=0, size=10, bbox=bbox_props)
	#t3 = ax.text(7000, 30000, "Instability Strip", ha="center", va="center", rotation=7, size=15, bbox=bbox_props)
	#ax.annotate('SuperGiant Region', xy=(11000, 120000), xytext=(10000, 120000), fontproperties=font0, arrowprops=dict(facecolor='black'),)
	#trans = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
	#theta = 50000
	#ax.axhline(theta, color='green', lw=2, alpha=0.5)
	#ax.axhline(-theta, color='red', lw=2, alpha=0.5)
	#ax.fill_between(x, 50000, 200000, facecolor='green', alpha=0.5, transform=trans)
	#ax.fill_between(x, 50000, 200000, facecolor='red', alpha=0.5, transform=trans)

	
	scatter = ax.scatter(Temperature,
						 Luminocity,
						 c=Color,
						 s=Radius*100,
						 alpha=0.7,
						 cmap=plt.cm.jet)
						 
	ax.grid(color='white', linestyle='solid')
	
	
	ax.set_xlim(500, 26000)
	ax.invert_xaxis()
	ax.set_ylim(-50000, 240000)
	ax.tick_params(axis='both', which='major', labelsize=8)
	#ax.set_xscale('log')
	#ax.set_ylim(math.pow(10,-4), math.pow(10,5))
	#ax.set_yscale('log')
	ax.set_xlabel('Temperature (K)', size=12)
	ax.set_ylabel('Luminocity (x Lsun)', size=12)
	ax.set_title("HR Diagram: The order of stars (Hover over the points to see a brief description)", size=12)
	#ax.annotate('SuperGiants', xy=(9000, 120000), xytext=(6000,200000), arrowprops=dict(facecolor='black'))
	
	#labels = ['point {0}'.format(i + 1) for i in range(N)]
	#labels.color = 'white'
		
	tooltip = mpld3.plugins.PointLabelTooltip(scatter, labels=labels)
	mpld3.plugins.connect(fig, tooltip)

	#mpld3.show()
		
	g = mpld3.fig_to_html(fig)
	mpld3.save_html(fig, "hr/templates/hr_regions.html")
	
	return django.http.HttpResponse(g)

P = np.random.random(size=n_size)
P[0]=6000
P[1]=3313
P[2]=6125
P[3]=3300
P[4]=5445
#P[5]=5500
P[5]=6151
#P[6]=5700
#P[7]=7000

N = len(P)
CL = ["" for x in range(N)]
i=0
while i<N:
	if P[i]>7000:
		CL[i]='violet'
	elif P[i]>6500:
		CL[i]='magenta'
	elif P[i]>6000:
		CL[i]='springgreen'
	elif P[i]>5500:
		CL[i]='greenyellow'
	elif P[i]>5000:
		CL[i]='yellow'
	elif P[i]>4000:
		CL[i]='coral'
	elif P[i]>3000:
		CL[i]='red'
	else: CL[i]='black'
	i=i+1
	
A = np.random.random(size=n_size)
A[0]=2000
A[1]=4168
A[2]=50
A[3]=3000
A[4]=3200
#A[5]=2900
A[5]=1186
#A[6]=565
#A[7]=2440
			
T = ["%.2f" % x for x in A]
T[0]='Cepheus - delta Cephei'

T[1]='Lyra - R Lyrae'
T[2]='Lyra - RR Lyrae'
#T[3]='Lepus - RX Leponis'
T[3]='Dorado - beta Doradus'
T[4]='Gemini - zeta Geminorum'
T[5]='Auriga - RT Aurigae'
#T[6]='Pavo - x Pavonis'
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
#C[6]=9.09
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
#D[6]=0.9
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
#E[6]=3.91
#E[7]=1.86
#####################################

def mplimageN(request):

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
	
	# FILL IN COLOR TABLE BASED ON TEMPERATURE
	N = len(P)
	CL = ["" for x in range(N)]
	i=0
	while i<N:
		if P[i]>7000:
			CL[i]='violet'
		elif P[i]>6500:
			CL[i]='magenta'
		elif P[i]>6000:
			CL[i]='springgreen'
		elif P[i]>5500:
			CL[i]='greenyellow'
		elif P[i]>5000:
			CL[i]='yellow'
		elif P[i]>4000:
			CL[i]='coral'
		elif P[i]>3000:
			CL[i]='red'
		else: CL[i]='black'
		i=i+1
			
	
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
	
	df = pd.DataFrame(index=range(N), columns=['Name','Temperature','Luminocity','Period','Magnitude Variation','Color'])

	xy=zip(T,P,A,C,D,CL)
	i=0
	while (i<N):
		#df.loc[i] = [star_array[i][0],star_array[i][1],star_array[i][2]]
		df.loc[i] = [xy[i][0],xy[i][1],xy[i][2],xy[i][3],xy[i][4],xy[i][5]]
		i=i+1

	labels = []
	for c in range(N):
		label = df.ix[[c], :].T
		label.columns = ['Star {0}'.format(c)]
		# .to_html() is unicode; so make leading 'u' go away with str()
		labels.append(str(label.to_html()))
		

	#df.at[0,'A'] // points = ax.plot(df.Temperature, df.Luminocity, 'o', color=( 1.0, 1.0, 1.0 ), mec='k', ms=15, mew=1, alpha=.6)
	points = ax.plot(df.Temperature, df.Luminocity, '*', color='red', mec='k', ms=20, mew=1, alpha=.6)
	#for j in range(N):
	#	points = ax.plot(5000 + 100*j, 100 + 10*j, '*', color=(j/15,j/25,j/100), mec='k', ms=20, mew=1, alpha=.6)

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