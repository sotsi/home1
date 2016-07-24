#from django.shortcuts import render

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

# Create your views here.
import django
import mpld3
import matplotlib
# import Figure and FigureCanvas, we will use API
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# used to generate the graph
import numpy as np
import math
import urllib2
from lxml.html import parse
import re


def mplimage_under_con(request):
	# general configurations
	user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)' # user_agent = accesses the website URL
	headers = { 'User-Agent' : user_agent } # headers = defines the url header
	url = "https://en.wikipedia.org/wiki/List_of_variable_stars" # url = the location of the website
	req = urllib2.Request(url, headers=headers) # req = the request for the specific url
	response = urllib2.urlopen(req) # response = the response of our request
	doc = parse(response).getroot() # parse = function that parses the response, 
								  # getroot = get the root of XML as seen as a hierarchical structure - tree
	table = doc.cssselect('table.wikitable')[0] # here we get any table element with class wikitable (acts like a filter)

	# python data structures that will store the data
	# example dmagnitude = 6999900000000000000\xe2\x99\xa00.90, period = 7001355358400000000\xe2\x99\xa035.53584\xc2\xa0d
	name = [] # this list will hold the name of the star
	constellation = [] # this list will hold the constellation
	type = [] # this list will hold the type of the star
	dmagnitude = [] # this list will hold the magnitude variation (max_magnitude - min_magnitude)
	period = [] # this list will hold the period of variation in days

	# fill in the empty data structures
	for row in table.cssselect('tr')[1:]: # we neglect the first and last row of the table (header & footer)
		data = row.cssselect('td') # we get all table contents
		name_ = data[0].text_content() # get the name of the star
		constellation_ = data[1].text_content() # get the name of the constellation
		type_ = data[7].text_content() # get the type of the star
		dmagnitude_ = data[5].text_content() # get the magnitude variation
		period_ = data[6].text_content() # get the period of variation
		if 'Cepheid' in type_:
			period_=period_.replace('\xe2','')
			period_=period_.replace('\x99','')
			period_=period_.replace('\xc2','')
			period_=period_.replace('\xa0d','')
			period_=period_.replace('\xa0',' ')
			period_=period_[period_.find(' ')+1:]
			period_n= float(period_)
			
			dmagnitude_=dmagnitude_.replace('\xe2','')
			dmagnitude_=dmagnitude_.replace('\x99','')
			dmagnitude_=dmagnitude_.replace('\xc2','')
			dmagnitude_=dmagnitude_.replace('\xa0',' ')
			dmagnitude_=dmagnitude_[dmagnitude_.find(' ')+1:]
			dmagnitude_n= float(dmagnitude_)
			# now we store the modified data to our lists
			name.append(str(name_))
			constellation.append(str(constellation_))
			type.append(str(constellation_))
			dmagnitude.append(float(dmagnitude_n))
			period.append(float(period_n))
		
	matplotlib.rc('font', family='Segoe Print')
	fig = Figure(figsize=(8, 6), dpi=100)
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.scatter(period, dmagnitude, s=50, c='b')
	ax.set_title("HR Diagram - Instability Strip")
	ax.set_ylabel('Luminocity (x Lsun)', size=15)
	ax.set_xlabel('Temperature (K)', size=15)
	ax.set_xlim(1000, 9000)
	ax.set_ylim(2000, 8500)
	#ax.invert_xaxis()
	i=0
	while i < len(name):
		signus = math.pow(-1,i)
		ax.annotate(name[i], xy=(period[i], dmagnitude[i]), xytext=(period[i]+8, dmagnitude[i]+8), arrowprops=dict(facecolor='magenta', arrowstyle='fancy'))
		i=i+1
	# now we can plot the data acquired from the website in a graph similar to HR diagram

	# prepare the response, setting Content-Type
	response=django.http.HttpResponse(content_type='image/png')
	# print the image on the response
	canvas.print_png(response)
	# and return it
	return response
	
def mplimage(request):
	# general configurations
	user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)' # access the website URL
	headers = { 'User-Agent' : user_agent } # define the url header
	url = "http://sotsiv.pythonanywhere.com/post/4/" # the location of the website
	req = urllib2.Request(url, headers=headers) # request for the specific url
	response = urllib2.urlopen(req) # the response of our request
	doc = parse(response).getroot() # parses the response
	table = doc.cssselect('table.var_table')[0] # here we filter any table element with class var_table
	# python data structures that will store the data
	name = [] # this list will hold the name of the star
	constellation = [] # this list will hold the constellation
	type = [] # this list will hold the type of star
	dmagnitude = [] # this list will hold magnitude variation
	period = [] # this list will hold the period of variation in days

	# fill in the empty data structures
	for row in table.cssselect('tr')[1:]: # we neglect the first row of the table (header)
		data = row.cssselect('td') # we get all table contents
		name_ = data[0].text_content() # get the name of the star
		constellation_ = data[1].text_content() # get the name of the constellation
		type_ = data[2].text_content() # get the type of the star
		dmagnitude_ = data[3].text_content() # get the magnitude variation
		period_ = data[4].text_content() # get the period of variation
		# now we store the modified data to our lists
		name.append(str(name_))
		constellation.append(str(constellation_))
		type.append(str(type_))
		dmagnitude.append(float(dmagnitude_))
		period.append(float(period_))
		
	matplotlib.rc('font', family='Segoe Print')
	fig = Figure(dpi=100)
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.scatter(period, dmagnitude, s=60, c='b')
	ax.set_title("Period - Magnitude Variation Diagram (Instability Strip)")
	ax.set_ylabel('Magnitude Variation', size=15)
	ax.set_xlabel('Period (days)', size=15)
	ax.set_xlim(0, 11)
	ax.set_ylim(0, 1.7)
	i=0
	while i < len(name):
		full_desc = name[i] # we could define: full_desc = name[i]+', '+type[i]+', '+constellation[i]
		ax.annotate(full_desc, xy=(period[i], dmagnitude[i]), xytext=(period[i]+0.5, dmagnitude[i]+0.3), arrowprops=dict(facecolor='magenta', arrowstyle='fancy'))
		i=i+1
	response=django.http.HttpResponse(content_type='image/png')
	canvas.print_png(response)
	return response
	
def mplimage3(request):
	# general configurations
	user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)' # user_agent = accesses the website URL
	headers = { 'User-Agent' : user_agent } # headers = defines the url header
	url = "https://en.wikipedia.org/wiki/List_of_variable_stars" # url = the location of the website
	req = urllib2.Request(url, headers=headers) # req = the request for the specific url
	response = urllib2.urlopen(req) # response = the response of our request
	doc = parse(response).getroot() # parse = function that parses the response, 
								  # getroot = get the root of XML as seen as a hierarchical structure - tree
	table = doc.cssselect('table.wikitable')[0] # here we get any table element with class wikitable (acts like a filter)

	# python data structures that will store the data
	name = [] # this list will store the name of the star
	constellation = [] # this list will store the name of constellation
	star_type = [] # this list will store the type of the star, for example classical cepheid
	min_magnitude = [] # this will store the minimum apparent magnitude of the star
	range_of_magnitude = [] # this list will store the range of magnitude
	period = [] # this list will store the period ind days

	# fill in the empty data structures
	for row in table.cssselect('tr')[1:]: # we neglect the first and last row of the table (header & footer)
		data = row.cssselect('td') # we get all table contents
		name_ = data[0].text_content() # get the name of the star
		constellation_ = data[1].text_content() # get the name of the constellation
		star_type_ = data[7].text_content() # get the name of the constellation
		min_magnitude_ = data[4].text_content() # get the minimum apparent magnitude value
		range_of_magnitude_ = data[5].text_content() # get the magnitude variation value
		period_ = data[6].text_content() # get the period value
		if 'year' not in period_:
			#period_ = period_[:4] # clean the temperature value to get a number
			#period_ = period_.replace('[[]()~d ]', '')
			# just in case we want periods > 1 year...
			#period_ = period_.replace('years', '')
			#period_ = float(period_)
			#period_ = 365*period_
			# now we store the modified data to our lists
			period__ = re.findall("\d+\.\d+", period_)
			name.append(str(name_))
			constellation.append(str(constellation_))
			star_type.append(str(star_type_))
			range_of_magnitude.append(float(range_of_magnitude_))
			#period.append(float(period__[0]))
			
	matplotlib.rc('font', family='Segoe Print')
	fig = Figure()
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.scatter(range_of_magnitude, range_of_magnitude, s=50, c='b')
	ax.set_title("Magnitude - Period Relation (Instability Strip)")
	ax.set_ylabel('Period (days)', size=15)
	ax.set_xlabel('Magnitude Variation', size=15)
	ax.set_xlim(0, 60)
	ax.set_ylim(0, 60)
	#ax.invert_xaxis()
	i=0
	while (i < len(name)) and (period[i] < 51):
		signus = math.pow(-1,i)
		full_descr = name[i] + ' - ' + constellation[i] + ' - ' + star_type[i]
		ax.annotate(full_descr, xy=(range_of_magnitude[i], range_of_magnitude[i]), xytext=(period[i]+800, range_of_magnitude[i]+800), arrowprops=dict(facecolor='magenta', arrowstyle='fancy'))
		i=i+1
	# now we can plot the data acquired from the website in a graph similar to HR diagram

	# prepare the response, setting Content-Type
	response=django.http.HttpResponse(content_type='image/png')
	# print the image on the response
	canvas.print_png(response)
	# and return it
	return response

	
def mplimage4(request):
	user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	url = "http://192.168.91.106:8081/matplotlib/index_beta.php"
	# prepare the request and open the url
	req = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(req)
	# we parse the webpage, getroot() return the document root
	doc = parse(response).getroot()
	# find the data table, using css elements
	table = doc.cssselect('table.wikitable')[0]
	# prepare data structures, will contain actual data
	foreas = []
	orio = []
	orio1 = []
	for row in table.cssselect('tr')[1:]:
		# get the row cell (we will use only the first two)
		data = row.cssselect('td')
		# the first cell is the year
		tmp_foreas = data[0].text_content()
		tmp_foreas=tmp_foreas.encode('utf-8')
		# cleanup for cases like 'YYYY[N]' (date + footnote link)
		#tmp_years = re.sub('\[.\]', '', tmp_years)
		# the second cell is the population count
		tmp_orio = data[3].text_content()
		# cleanup from '.', used as separator
		tmp_orio = tmp_orio.replace(',', '')
		tmp_orio1 = data[4].text_content()
		# cleanup from '.', used as separator
		tmp_orio1 = tmp_orio1.replace(',', '')
		# append current data to data lists, converting to integers
		foreas.append(int(tmp_foreas))
		orio.append(int(tmp_orio))
		orio1.append(int(tmp_orio1))
	n_size=len(orio)
	explode=[0,0,0,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7]
	#########################
	# -*- coding: UTF-8 -*-
	import matplotlib.pyplot as plt
	import numpy as np
	data1 = 10*np.random.rand(5)
	data2 = 10*np.random.rand(5)
	data3 = 10*np.random.rand(5)
	e2 = 0.5 * np.abs(np.random.randn(len(data2)))
	locs = np.arange(1, len(data1)+1)
	width = 0.27
	#########################
	fig = Figure(figsize=(9, 6), dpi=100, facecolor='w', edgecolor='m')
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.bar(foreas, orio, width=width);
	#ax.bar(foreas+width, orio1, yerr=e2, width=width,color='red');
	#ax.bar(locs+2*width, data3, width=width, color='green') ;
	#ax.xticks(locs + width*1.5, locs);
	#ax.bar(foreas,orio)
	#ax.xticks(range(min(years), max(years), 10))
	#ax.grid()
	#ax.annotate("2001 Census", xy=(1012900, people[years.index(1012900)]),
	#		xytext=(1012900, 54.5*10**6),
	#		arrowprops=dict(arrowstyle='fancy'))
	# prepare the response, setting Content-Type
	response=django.http.HttpResponse(content_type='image/png')
	# print the image on the response
	canvas.print_png(response)
	# and return it
	return response
	
	
def mplimage2(request):
	user_agent = 'Mozilla/5.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	url = "http://192.168.91.106:8081/matplotlib/index_beta.php"
	# prepare the request and open the url
	req = urllib2.Request(url, headers=headers)
	response = urllib2.urlopen(req)
	# we parse the webpage, getroot() return the document root
	doc = parse(response).getroot()
	# find the data table, using css elements
	table = doc.cssselect('table.wikitable')[0]
	# prepare data structures, will contain actual data
	foreas = []
	orio = []
	for row in table.cssselect('tr')[1:]:
		# get the row cell (we will use only the first two)
		data = row.cssselect('td')
		# the first cell is the year
		tmp_foreas = data[0].text_content()
		tmp_foreas=tmp_foreas.encode('utf-8')
		# cleanup for cases like 'YYYY[N]' (date + footnote link)
		#tmp_years = re.sub('\[.\]', '', tmp_years)
		# the second cell is the population count
		tmp_orio = data[3].text_content()
		# cleanup from '.', used as separator
		tmp_orio = tmp_orio.replace(',', '')
		# append current data to data lists, converting to integers
		foreas.append(str(tmp_foreas))
		orio.append(float(tmp_orio))
	n_size=len(orio)
	explode=[0,0,0,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.7]
	#i=0 
	#while i < 14:
	#	pie_expand.append(i/n_size)
	#	i=i+1/n_size
	# do the plotting 
	fig = Figure(figsize=(5, 6), dpi=150, facecolor='w', edgecolor='m')
	canvas = FigureCanvas(fig)
	ax = fig.add_subplot(111)
	ax.pie(orio, labels=foreas, explode=explode, autopct='%1.1f%%')
	#ax.bar(foreas,orio)
	#ax.xticks(range(min(years), max(years), 10))
	ax.grid()
	#ax.annotate("2001 Census", xy=(1012900, people[years.index(1012900)]),
	#		xytext=(1012900, 54.5*10**6),
	#		arrowprops=dict(arrowstyle='fancy'))
	# prepare the response, setting Content-Type
	response=django.http.HttpResponse(content_type='image/png')
	# print the image on the response
	canvas.print_png(response)
	# and return it
	return response
	
def mplimage23(request):
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