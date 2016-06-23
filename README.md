
buoypy - a work in progress
========

Functions to query the [NDBC](http://www.ndbc.noaa.gov/).

Returns pandas dataframes for the wave parameters.

Currently only realtime data is implemented.



The real time data for all of their buoys can be found at:
http://www.ndbc.noaa.gov/data/realtime2/

An explanation of the data can be found at:
http://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf


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

rt = bp.realtime(41013) #Frying pan shoals

ocean_data = rt.get_ocean()
wave_data = rt.get_spec()

# plotting
fig,ax = plt.subplots(2,1,figsize = (10,10),sharex=True)

ocean_data['OTMP'].plot(ax=ax[0])
sns.despine()
wave_data['WVHT'].plot(ax=ax[1])
sns.despine()

ax[0].set_ylabel('Ocean Temperature ($^\circ C$)')
ax[1].set_ylabel('Wave Height ($m$)')

plt.savefig('../figures/realtime.png',bbox_inches='tight')
```

![bouypy plots](/figures/realtime.png)
