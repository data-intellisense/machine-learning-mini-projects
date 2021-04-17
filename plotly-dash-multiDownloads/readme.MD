## Problem to solve:
'Download' module from dash_extensions allows only one download when each callback is triggers. This script shows how to download multiple files automatically on plotly dash through using dcc.Intervals module.

## How:
It achieves the goal by triggering each download using 'n_intervals' of dcc.Interval and stop the downloading by setting the 'max_intervals' = number of files. 

## Limitations:
Each download needs to be completed within 'interval' (in milliseconds) time span of dcc.Interval or else the download will be skipped. You can increase 'interval' to avoid such limitations. Another solution is by manipulating the 'disabled' property. 

## Extensions:
You can apply the same concept to trigger one callback multiple times

## Notes:
To run the script successfully, you need to install the library imported, whose versions are outlined in 'requirements.txt'
