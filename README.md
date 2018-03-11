# quickCPM
GMC-320 Radiation Detector Python Utility
![quickCPM](https://github.com/abitowhit/quickCPM/blob/master/gauge2.png)

## Overview
Stand-Alone, Non-GUI Single python script which reads the CPM data from a Geiger-Counter GMC-3xx (_GQelectronics_) via USB.
Stores CPM and Temperature into (per day) csv log file for analysis. (stamp,value)  
Creates a bar graph and gauge html file for viewing current status in a browser.
Written as a simple interface on Raspberry Pi to be included in home monitoring.

## Device

GMC-3xx (GMC-300, GMC-320) is a hand held geiger counter. Is is build around a M4011-Geigertube.

 * Length of tube about 100mm, 
 * Background counts around 20 count per minute. 
 * Size of memory: 64k. 

## Software Options

* Per second loop time adjustment argument.
* CLI Only, no GUI

## Software structure

The program is  written in Python 2.7
Python Data retrieval and serial calls referenced from GMC-3xx Datalogger (see references)
May work with other GMC models, only tested on gmc-320+
CLI output is:
     03/11/2018 07:30:00 24 (Peak:32) -Time
     22.6c - 63.64f -Temp in C and F
     23 chars written to logs/gmc_20180311_cpm.csv   -CSV output files CPM
     31 chars written to logs/gmc_20180311_temp.csv  -CSV output files Temperature
     1959 chars written to index.html                -Bar graph html output file html
     4513 chars written to gauges.html               -Gauge graph output file html


## Installation

Requirements:

* Python 2.7 (will possibly work with other versions) and following libraries:
* datetime
* struct
* time
* os
* serial   
 
(Unzip) Save files below in a directory and start:
In terminal session in that directory run:
    $ python quickcpm.py 60
Where 60 is optional time per second you want it to loop the connection.
Default is 300 which is 5 minutes

[247Coding.com] (http://247coding.com/drupal/?q=quickCPM)
    
Files:
* quickcpm.py    # main python program
* /logs           # directory where csv logs are saved
* gauge.min.js    # gauge builder referenced in html script reference.
https://canvas-gauges.com/

## License

GNU General Public License version 3.0 (GPLv3) (https://www.gnu.org/licenses/gpl-3.0.de.html)

## Limitations
Script is written without much exception validation due to time constraints.
Your mileage may very.

Four solutions:

* Output to terminal.
* You may use the software only for accessing memory data and waive the live data option.
* You may use the CLI version (without live data option).
* You may use the _Complete GUI Python Script_, see references.


## References:
 * [gqmc](https://sourceforge.net/projects/gqgmc/files/gqgmc/): C-program, ICD and other documentations
 * [ullix](https://sourceforge.net/projects/geigerlog/) Basic I/O Python routines
 * [GQelectronics GMC Manual](https://www.gqelectronicsllc.com/comersus/store/download.asp)
 * [GQelectronics GMC Forum](https://www.gqelectronicsllc.com/forum/forum.asp?FORUM_ID=14)
 * [Complete GUI Python script by Ullix](https://sourceforge.net/projects/geigerlog/)
 * [Canvas Gauges](https://canvas-gauges.com/documentation/user-guide/ )
 * [247Coding.com] (https://247coding.com/drupal/?q=quickCPM) Site Link


