"""
By Nick Cortale
nickc1.github.io

Functions to query the NDBC (http://www.ndbc.noaa.gov/).

The realtime data for all of their buoys can be found at:
http://www.ndbc.noaa.gov/data/realtime2/

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


"""

import pandas as pd


def get_spec(buoy):
	"""
	Get the spectral wave data from the ndbc

	parameters
	----------
	buoy : string
		Buoy number ex: '41013' is off wilmington, nc

	Returns
	-------
	df : pandas dataframe
		data frame containing the spectral data

	Notes
	-----
	The data frame columns are:

	WVHT          meters
	SwH           meters
	SwP           seconds
	WWH           meters
	WWP           seconds
	SwD           -
	WWD           degT
	STEEPNESS     -
	APD           sec
	MWD           degT


	"""



	params = 'spec'
	base = 'http://www.ndbc.noaa.gov/data/realtime2/'
	link = base + str(buoy) + '.' + params

	#combine the first five date columns YY MM DD hh mm and make index
	df = pd.read_csv(link, delim_whitespace=True, parse_dates=[[0,1,2,3,4]], index_col=0)

	#units are in the second row drop them
	df.columns = df.columns + '('+ df.iloc[0] + ')'
	df.drop(df.index[0], inplace=True)

	#convert the dates to datetimes
	df.index = pd.to_datetime(df.index,format="%Y %m %d %H %M")

	return df















