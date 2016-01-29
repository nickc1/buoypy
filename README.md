
buoypy - a work in progress 
========

Functions to query the [NDBC](http://www.ndbc.noaa.gov/).

Returns pandas dataframes for the wave parameters.

Currently only realtime data is implemented.



The real time data for all of their buoys can be found at:
http://www.ndbc.noaa.gov/data/realtime2/

An explanation of the data can be found at:
http://www.ndbc.noaa.gov/docs/ndbc_web_data_guide.pdf


Each buoy has the data:


| Method			| Parameters                    |
| ----------------- |------------------------------ |
| get_txt			| standard meteorological data  |
| get_spec 			| spectral wave summaries		|
| data_spec 		| raw spectral wave data 		|
| get_swdir 		| spectral wave data (alpha1) 	|
| get_swdir2 		| spectral wave data (alpha2) 	|
| get_swr1 			| spectral wave data (r1) 		|
| get_swr2 			| spectral wave data (r2) 		|
| get_ocean 		| oceanographic data 			|
| get_supl 			| Supplementary data 			|


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

![Image of Yaktocat](/figures/realtime.png)


