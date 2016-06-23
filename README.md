
buoypy
========

Functions to query the [NDBC](http://www.ndbc.noaa.gov/).

Returns pandas dataframes for the wave parameters.

Data descriptions - [Link][http://www.ndbc.noaa.gov/measdes.shtml]


# Real Time - Last 45 Days

The real time data for all of their buoys can be found at:
http://www.ndbc.noaa.gov/data/realtime2/

The realtime data provided is :

|File					|Description
|-------------|-----------------------
|.data_spec		|	Raw Spectral Wave Data
|.spec				|	Spectral Wave Summary Data
|.swdir				|	Spectral Wave Data (alpha1)
|.swdir2			|	Spectral Wave Data (alpha2)
|.swr1				|	Spectral Wave Data (r1)
|.swr2				|	Spectral Wave Data (r2)
|.txt					|	Standard Meteorological Data

The data headers for each of the files are provided below.

##### .data_spec

|YY	|MM	|DD	|hh	|mm	|Sep_Freq	|spec_1	|(freq_1)	|spec_2	|(freq_2)	|spec_3	|(freq_3)	|...
|---|---|---|---|---|---------|-------|---------|-------|---------|-------|---------|---

##### .spec

|YY	|MM	|DD	|hh	|mm	|WVHT	|SwH	|SwP	|WWH	|WWP	|SwD	|WWD	|STEEPNESS	|APD	|MWD
|---|---|---|---|---|-----|-----|-----|-----|-----|-----|-----|-----------|-----|---
|yr	|mo	|dy	|hr	|mn	|m		|m		|sec 	|m		|sec 	|-		|degT	| -					|sec	|degT

##### .swdir

|YY	|MM	|DD	|hh	|mm	|alpha1_1	|(freq_1)	|alpha1_2	|(freq_2)	|alpha1_3	|(freq_3)	|...
|---|---|---|---|---|---------|---------|---------|---------|---------|---------|---

##### .swdir2

|YY	|MM	|DD	|hh	|mm	|alpha2_1	|(freq_1)	|alpha2_2	|(freq_2)	|alpha2_3	|(freq_3)	|...
|---|---|---|---|---|---------|---------|---------|---------|---------|---------|---

##### .swr1

|YY	|MM	|DD	|hh	|mm	|r1_1	|(freq_1)	|r1_2	|(freq_2)	|r1_3	|(freq_3)	|...
|---|---|---|---|---|-----|---------|-----|---------|-----|---------|---

##### .swr2

|YY	|MM	|DD	|hh	|mm	|r2_1	|(freq_1)	|r2_2	|(freq_2)	|r2_3	|(freq_3)	|...
|---|---|---|---|---|-----|---------|-----|---------|-----|---------|---


##### .txt

|YY	|MM	|DD	|hh	|mm	|WDIR	|WSPD	|GST	|WVHT	|DPD	|APD	|MWD	|PRES	|ATMP	|WTMP	|DEWP	|VIS	|PTDY	|TIDE
|---|---|---|---|---|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|----
|yr	|mo	|dy	|hr	|mn	|degT	|m/s	|m/s 	|m		|sec 	|sec	|degT	|hPa	|degC	|degC	|degC	|nmi	|hPa	|ft



| Method			| Description                   |
| ----------- |------------------------------ |
| data_spec 	| raw spectral wave data 				|
| get_spec 		| spectral wave summaries				|
| get_swdir 	| spectral wave data (alpha1) 	|
| get_swdir2 	| spectral wave data (alpha2) 	|
| get_swr1 		| spectral wave data (r1) 			|
| get_swr2 		| spectral wave data (r2) 			|
| get_txt			| standard meteorological data  |


#Examples

```python
import buoypy as bp

buoy = 41108 #wilmington harbor
B = bp.realtime(buoy) #wilmington harbor

df = B.txt()

# plotting
fig,ax = plt.subplots(2,sharex=True)
df.WVHT.plot(ax=ax[0])
ax[0].set_ylabel('Wave Height (m)',fontsize=14)

df.DPD.plot(ax=ax[1])
ax[1].set_ylabel('Dominant Period (sec)',fontsize=14)
ax[1].set_xlabel('')
sns.despine()
```

![bouypy realtime](/figures/realtime.png)


# Historic Data - All information from a buoy

All buoys have different years that they are online. This aims to grab all the available data. Currently only grabbing the standard Meteorological data is implemented.

The historic data provided is:

|Description
|-----------------------
|	Standard Meteorological Data


|YY	|MM	|DD	|hh	|mm	|WDIR	|WSPD	|GST	|WVHT	|DPD	|APD	|MWD	|PRES	|ATMP	|WTMP	|DEWP	|VIS	|TIDE
|---|---|---|---|---|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|----
|yr	|mo	|dy	|hr	|mn	|degT	|m/s	|m/s 	|m		|sec 	|sec	|degT	|hPa	|degC	|degC	|degC	|nmi	|ft



```python
import buoypy as bp

buoy = 41108
year = 2014

H = bp.historic_data(buoy,year)
df = H.get_stand_meteo()

# plotting
fig,ax = plt.subplots(2,sharex=True)
df.WVHT.plot(ax=ax[0])
ax[0].set_ylabel('Wave Height (m)',fontsize=14)

df.DPD.plot(ax=ax[1])
ax[1].set_ylabel('Dominant Period (sec)',fontsize=14)
ax[1].set_xlabel('')
sns.despine()
```

![bouypy historic](/figures/historic.png)

Notice that the buoy went offline from the end of April, 2014 to mid August, 2014.


# Historic Range - Grab data from a range of years

```python

import buoypy as bp
buoy = 41108
year = np.NAN
year_range = (2010,2018)

H = bp.historic_data(buoy,year,year_range)
X = H.get_all_stand_meteo()

#plotting
fig,ax = plt.subplots(2,sharex=True)
X.WVHT.plot(ax=ax[0])
ax[0].set_ylabel('Wave Height (m)',fontsize=14)
X.DPD.plot(ax=ax[1])
ax[1].set_ylabel('Dominant Period (sec)',fontsize=14)
ax[1].set_xlabel('')
sns.despine()
```

![bouypy historic range](/figures/historic_range.png)
