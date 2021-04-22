## Problem to solve:

How to download multiple files on Plotly Dash automatically?

Each 'Download' module from dash_extensions allows only one download when each callback is triggers. Two solutions presented here to download multiple files automatically.

## How:

Method 1: using dcc.Intervals module. It achieves the goal by triggering the same 'Download' module using 'n_intervals' of dcc.Interval and stop the downloading by setting the 'max_intervals' = number of files. This works well when downloading small files. Demonstrated in 'multiDownloads.py'.

Method 2: building and call for multiple 'Download' modules. Demonstrated in 'multiDownloads2.py'.

## Limitations:

The limitations of Method 1 is that each download needs to be completed within 'interval' (in milliseconds) time span of dcc.Interval or else the download will be skipped. You can increase 'interval' to mitigate such limitations.

Method 2 avoids the limitation of Method 1. However, it builds more 'Download' module than what we usually need so it may not be the most efficient way. Overall it's a better and sufficiently efficient solution.

## Extensions:

You can apply the same concept of Method 1 using dcc.Interval to trigger one callback multiple times and stop when necessary.

## Notes:

To run the script successfully, you need to install the library imported, whose versions are outlined in 'requirements.txt'
