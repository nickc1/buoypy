"""
By Nick Cortale
nickc1.github.io

Functions to query the NDBC (http://www.ndbc.noaa.gov/).

The realtime data for all of their buoys can be found at:
http://www.ndbc.noaa.gov/data/realtime2/

Info about all of noaa data can be found at:
http://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf

What all the values mean:
http://www.ndbc.noaa.gov/measdes.shtml

Each buoy has the data:

File                    Parameters
----                    ----------
.data_spec         Raw Spectral Wave Data
.ocean             Oceanographic Data
.spec              Spectral Wave Summary Data
.supl              Supplemental Measurements Data
.swdir             Spectral Wave Data (alpha1)
.swdir2            Spectral Wave Data (alpha2)
.swr1              Spectral Wave Data (r1)
.swr2              Spectral Wave Data (r2)
.txt               Standard Meteorological Data



Example:
import buoypy as bp

# Get the last 45 days of data
rt = bp.realtime(41013) #frying pan shoals buoy
ocean_data = rt.get_ocean()  #get Oceanographic	data

wave_data.head()

Out[7]:
					WVHT	SwH SwP	WWH	WWP	SwD	WWD	STEEPNESS	APD	MWD
2016-02-04 17:42:00	1.6		1.3	7.1	0.9	4.5	S	S	STEEP		5.3	169
2016-02-04 16:42:00	1.7		1.5	7.7	0.9	5.0	S	S	STEEP		5.4	174
2016-02-04 15:41:00	2.0		0.0	NaN	2.0	7.1	NaN	S	STEEP		5.3	174
2016-02-04 14:41:00	2.0		1.2	7.7	1.5	5.9	SSE	SSE	STEEP		5.5	167
2016-02-04 13:41:00	2.0		1.7	7.1	0.9	4.8	S	SSE	STEEP		5.7	175



TODO:
Make functions with except statements always spit out the same 
column headings.

"""

import pandas as pd
import numpy as np
import urllib2
from sqlalchemy import create_engine # database connection
import datetime

class realtime:

	def __init__(self, buoy):
		self.buoy = buoy

	def get_data_spec(self):
		"""
		Get the raw spectral wave data from the buoy. The seperation
		frequency is dropped to keep the data clean.

		Parameters
		----------
		buoy : string
			Buoy number ex: '41013' is off wilmington, nc

		Returns
		-------
		df : pandas dataframe (date, frequency)
			data frame containing the raw spectral data. index is the date
			and the columns are each of the frequencies

		"""

		params = 'data_spec'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link,delim_whitespace=True,skiprows=1,header=None,
			parse_dates=[[0,1,2,3,4]], index_col=0)


		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		specs = df.iloc[:,1::2]
		freqs = df.iloc[0,2::2]

		specs.columns=freqs

		#remove the parenthesis from the column index
		specs.columns = [cname.replace('(','').replace(')','') 
			for cname in specs.columns]

		return specs


	def get_ocean(self):
		"""
		Retrieve oceanic data. For the buoys explored,
		O2%, O2PPM, CLCON, TURB, PH, EH were always NaNs


		Returns
		-------
		df : pandas dataframe
			Index is the date and columns are:
			DEPTH	m
			OTMP	degc
			COND	mS/cm 
			SAL 	PSU
			O2%		%
			02PPM	ppm
			CLCON	ug/l
			TURB	FTU
			PH 		-
			EH 		mv

		"""

		params = 'ocean'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link, delim_whitespace=True, na_values='MM', 
			parse_dates=[[0,1,2,3,4]], index_col=0)

		#units are in the second row drop them
		df.drop(df.index[0], inplace=True)

		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		#convert to floats
		cols = ['DEPTH','OTMP','COND','SAL']
		df[cols] = df[cols].astype(float)

		
		return df


	def get_spec(self):
		"""
		Get the spectral wave data from the ndbc. Something is wrong with
		the data for this parameter. The columns seem to change randomly.
		Refreshing the data page will yield different column names from
		minute to minute.

		parameters
		----------
		buoy : string
			Buoy number ex: '41013' is off wilmington, nc

		Returns
		-------
		df : pandas dataframe
			data frame containing the spectral data. index is the date
			and the columns are:

			HO, SwH, SwP, WWH, WWP, SwD, WWD, STEEPNESS, AVP, MWD

			OR

			WVHT  SwH  SwP  WWH  WWP SwD WWD  STEEPNESS  APD MWD


		"""

		params = 'spec'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link, delim_whitespace=True, na_values='MM', 
		parse_dates=[[0,1,2,3,4]], index_col=0)

		try:
			#units are in the second row drop them
			#df.columns = df.columns + '('+ df.iloc[0] + ')'
			df.drop(df.index[0], inplace=True)

			#convert the dates to datetimes
			df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

			#convert to floats
			cols = ['WVHT','SwH','SwP','WWH','WWP','APD','MWD']
			df[cols] = df[cols].astype(float)
		except:

			#convert the dates to datetimes
			df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

			#convert to floats
			cols = ['H0','SwH','SwP','WWH','WWP','AVP','MWD']
			df[cols] = df[cols].astype(float)
			

		return df



	def get_supl(self):
		"""
		Get supplemental data

		Returns
		-------
		data frame containing the spectral data. index is the date
		and the columns are:

		PRES		hpa
		PTIME		hhmm
		WSPD		m/s
		WDIR		degT
		WTIME		hhmm


		"""
		params = 'supl'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link, delim_whitespace=True, na_values='MM',
			parse_dates=[[0,1,2,3,4]], index_col=0)

		#units are in the second row drop them
		df.drop(df.index[0], inplace=True)

		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		#convert to floats
		cols = ['PRES','PTIME','WSPD','WDIR','WTIME']
		df[cols] = df[cols].astype(float)

		return df


	def get_swdir(self):
		"""
		Spectral wave data for alpha 1.

		Returns
		-------

		specs : pandas dataframe
			Index is the date and the columns are the spectrum. Values in
			the table indicate how much energy is at each spectrum.
		"""


		params = 'swdir'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link,delim_whitespace=True,skiprows=1,na_values=999,
			header=None, parse_dates=[[0,1,2,3,4]], index_col=0)

		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		specs = df.iloc[:,0::2]
		freqs = df.iloc[0,1::2]

		specs.columns=freqs

		#remove the parenthesis from the column index
		specs.columns = [cname.replace('(','').replace(')','') 
			for cname in specs.columns]

		return specs

	def get_swdir2(self):
		"""
		Spectral wave data for alpha 2.

		Returns
		-------

		specs : pandas dataframe
			Index is the date and the columns are the spectrum. Values in
			the table indicate how much energy is at each spectrum.
		"""
		params = 'swdir2'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link,delim_whitespace=True,skiprows=1,
			header=None, parse_dates=[[0,1,2,3,4]], index_col=0)

		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		specs = df.iloc[:,0::2]
		freqs = df.iloc[0,1::2]

		specs.columns=freqs

		#remove the parenthesis from the column index
		specs.columns = [cname.replace('(','').replace(')','') 
			for cname in specs.columns]

		return specs

	def get_swr1(self):
		"""
		Spectral wave data for r1.

		Returns
		-------

		specs : pandas dataframe
			Index is the date and the columns are the spectrum. Values in
			the table indicate how much energy is at each spectrum.
		"""


		params = 'swr1'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link,delim_whitespace=True,skiprows=1,
			header=None, parse_dates=[[0,1,2,3,4]], index_col=0)

		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		specs = df.iloc[:,0::2]
		freqs = df.iloc[0,1::2]

		specs.columns=freqs

		#remove the parenthesis from the column index
		specs.columns = [cname.replace('(','').replace(')','') 
			for cname in specs.columns]

		return specs

	def get_swr2(self):
		"""
		Spectral wave data for r2.

		Returns
		-------

		specs : pandas dataframe
			Index is the date and the columns are the spectrum. Values in
			the table indicate how much energy is at each spectrum.
		"""

		params = 'swr2'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link,delim_whitespace=True,skiprows=1,
			header=None, parse_dates=[[0,1,2,3,4]], index_col=0)

		#convert the dates to datetimes
		df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

		specs = df.iloc[:,0::2]
		freqs = df.iloc[0,1::2]

		specs.columns=freqs

		#remove the parenthesis from the column index
		specs.columns = [cname.replace('(','').replace(')','') 
			for cname in specs.columns]

		return specs

	def get_txt(self):
		"""
		Retrieve standard Meteorological data. NDBC seems to be updating
		the data with different column names, so this metric can return 
		two possible data frames with different column names:

		Returns
		-------

		df : pandas dataframe
			Index is the date and the columns can be:

			['WDIR','WSPD','GST','WVHT','DPD','APD','MWD',
			'PRES','ATMP','WTMP','DEWP','VIS','PTDY','TIDE']

			or

			['WD','WSPD','GST','WVHT','DPD','APD','MWD','BARO',
			'ATMP','WTMP','DEWP','VIS','PTDY','TIDE']

		"""

		params = 'txt'
		base = 'http://www.ndbc.noaa.gov/data/realtime2/'
		link = base + str(self.buoy) + '.' + params

		#combine the first five date columns YY MM DD hh mm and make index
		df = pd.read_csv(link, delim_whitespace=True, na_values='MM', 
			parse_dates=[[0,1,2,3,4]], index_col=0)

		try:
			#first column is units, so drop it
			df.drop(df.index[0], inplace=True)
			#convert the dates to datetimes
			df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

			#convert to floats
			cols = ['WDIR','WSPD','GST','WVHT','DPD','APD','MWD',
			'PRES','ATMP','WTMP','DEWP','VIS','PTDY','TIDE']
			df[cols] = df[cols].astype(float)
		except:

			#convert the dates to datetimes
			df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

			#convert to floats
			cols = ['WD','WSPD','GST','WVHT','DPD','APD','MWD','BARO',
			'ATMP','WTMP','DEWP','VIS','PTDY','TIDE']
			df[cols] = df[cols].astype(float)
		return df

################################################
################################################

class historic_data:

	def __init__(self, buoy, year,year_range=None):
		self.buoy = buoy
		self.year = year
		self.year_range=year_range

	def get_stand_meteo(self,link = None):
		'''
		Standard Meteorological Data. Data header was changed in 2007. Thus
		the need for the if statement below.



		WDIR	Wind direction (degrees clockwise from true N)
		WSPD	Wind speed (m/s) averaged over an eight-minute period 
		GST		Peak 5 or 8 second gust speed (m/s) 
		WVHT	Significant wave height (meters) is calculated as 
				the average of the highest one-third of all of the 
				wave heights during the 20-minute sampling period. 
		DPD		Dominant wave period (seconds) is the period with the maximum wave energy.
		APD		Average wave period (seconds) of all waves during the 20-minute period. 
		MWD		The direction from which the waves at the dominant period (DPD) are coming. 
				(degrees clockwise from true N)
		PRES	Sea level pressure (hPa). 
		ATMP	Air temperature (Celsius). 
		WTMP	Sea surface temperature (Celsius). 
		DEWP	Dewpoint temperature 
		VIS		Station visibility (nautical miles). 
		PTDY	Pressure Tendency 
		TIDE	The water level in feet above or below Mean Lower Low Water (MLLW).
		'''


		if not link:
			base = 'http://www.ndbc.noaa.gov/view_text_file.php?filename='
			link = base + str(self.buoy) + 'h' + str(self.year) + '.txt.gz&dir=data/historical/stdmet/'

		#combine the first five date columns YY MM DD hh and make index
		df = pd.read_csv(link,delim_whitespace=True,na_values=[99,999,9999,99.,999.,9999.])

		#2007 and on format
		if df.iloc[0,0] =='#yr':


			df = df.rename(columns={'#YY': 'YY'}) #get rid of hash

			#make the indices
			date_str = df.YY + ' ' + df.MM+ ' ' + df.DD + ' ' + df.hh + ' ' + df.mm
			df.drop(0,inplace=True) #first row is units, so drop them
			ind = pd.to_datetime(date_str.drop(0),format="%Y %m %d %H %M")

			df.index = ind

			#drop useless columns and rename the ones we want
			df.drop(['YY','MM','DD','hh','mm'],axis=1,inplace=True)
			df.columns = ['WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD', 'PRES',
				'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']


		#before 2006 to 2000
		else:
			date_str = df.YYYY.astype('str') + ' ' + df.MM.astype('str') + \
				' ' + df.DD.astype('str') + ' ' + df.hh.astype('str')

			ind = pd.to_datetime(date_str,format="%Y %m %d %H")

			df.index = ind

			#drop useless columns and rename the ones we want
			#######################
			'''FIX MEEEEE!!!!!!!
			Get rid of the try except
			some have minute column'''

			#this is hacky and bad
			try:
				df.drop(['YYYY','MM','DD','hh','mm'],axis=1,inplace=True)
				df.columns = ['WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD', 'PRES',
				'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']

			except:
				df.drop(['YYYY','MM','DD','hh'],axis=1,inplace=True)
				df.columns = ['WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD', 'PRES',
				'ATMP', 'WTMP', 'DEWP', 'VIS', 'TIDE']


		# all data should be floats
		df = df.astype('float')
		nvals = [99,999,9999,99.0,999.0,9999.0]
		df.replace(nvals,np.nan,inplace=True)

		return df

	def get_all_stand_meteo(self):
		"""
		Retrieves all the standard meterological data. Calls get_stand_meteo.
		It also checks to make sure that the years that were requested are
		available. Data is not available for the same years at all the buoys.

		Returns
		-------
		df : pandas dataframe
			Contains all the data from all the years that were specified
			in year_range.
		"""

		start,stop = self.year_range

		#see what is on the NDBC so we only pull the years that are available
		links = []
		for ii in range(start,stop+1):

			base = 'http://www.ndbc.noaa.gov/view_text_file.php?filename='
			end = '.txt.gz&dir=data/historical/stdmet/'
			link = base + str(self.buoy) + 'h' + str(ii) + end

			try:
				urllib2.urlopen(link)
				links.append(link)

			except:
				print(str(ii) + ' not in records')

		#need to also retrieve jan, feb, march, etc.
		month = ['Jan','Feb','Mar','Apr','May','Jun',
			'Jul','Aug','Sep','Oct','Nov','Dec']
		k = [1,2,3,4,5,6,7,8,9,'a','b','c'] #for the links

		for ii in range(len(month)):
			mid = '.txt.gz&dir=data/stdmet/'
			link = base + str(self.buoy) + str(k[ii]) + '2015' + mid + str(month[ii]) +'/'

			try:
				urllib2.urlopen(link)
				links.append(link)

			except:
				print(str(month[ii]) + '2015' + ' not in records')
				print link


		# start grabbing some data
		df=pd.DataFrame() #initialize empty df

		for L in links:

			new_df = self.get_stand_meteo(link=L)
			print 'Link : ' + L
			df = df.append(new_df)

		return df


class write_data(historic_data):

	def __init__(self, buoy, year, year_range,db_name = 'buoydata.db'):
		self.buoy = buoy
		self.year = year
		self.year_range=year_range
		self.db_name = db_name

	def write_all_stand_meteo(self):
		"""
		Write the standard meteological data to the database. See get_all_stand_meteo
		for a discription of the data. Which is in the historic data class.

		Returns
		-------
		df : pandas dataframe (date, frequency)
			data frame containing the raw spectral data. index is the date
			and the columns are each of the frequencies

		"""

		#hist = self.historic_data(self.buoy,self.year,year_range=self.year_range)
		df = self.get_all_stand_meteo()

		#write the df to disk
		disk_engine = create_engine('sqlite:///' + self.db_name)

		table_name = str(self.buoy) + '_buoy'
		df.to_sql(table_name,disk_engine,if_exists='append')
		sql = disk_engine.execute("""DELETE FROM wave_data 
			WHERE rowid not in 
			(SELECT max(rowid) FROM wave_data GROUP BY date)""")

		print(str(self.buoy) + 'written to database : ' + str(self.db_name))


		return True 


class read_data:
	"""
	Reads the data from the setup database
	"""

	def __init__(self, buoy, year_range=None):
		self.buoy = buoy
		self.year_range = year_range
		self.disk_eng = 'sqlite:///buoydata.db'


	def get_stand_meteo(self):

		disk_engine = create_engine(self.disk_eng)

		
		df = pd.read_sql_query(" SELECT * FROM " + "'" + str(self.buoy) + '_buoy' + "'", disk_engine)

		#give it a datetime index since it was stripped by sqllite
		df.index = pd.to_datetime(df['index'])
		df.index.name='date'
		df.drop('index',axis=1,inplace=True)

		if self.year_range:
			print("""this is not implemented in SQL. Could be slow. 
					Get out while you can!!!""" )
			
			start,stop = (self.year_range)
			begin = df.index.searchsorted(datetime.datetime(start, 1, 1))
			end = df.index.searchsorted(datetime.datetime(stop, 12, 31))
			df = df.ix[begin:end]

		

		return df












